"""Tests for pprose.metrics. All fixtures are local; no network access."""

from __future__ import annotations

from pathlib import Path

import pytest

from pprose import metrics as pwm

FIXTURES = Path(__file__).resolve().parent / "test_fixtures" / "practical_prose_metrics"


def _measure(name: str) -> pwm.Metrics:
    return pwm.measure(FIXTURES / name)


# ---------------------------------------------------------------------------
# P0-1: Frontmatter and code blocks must not inflate prose counts
# ---------------------------------------------------------------------------


class TestP0_1_ProseExclusion:
    def test_code_block_excluded_from_word_count(self):
        m = _measure("frontmatter_and_code.md")
        # The fixture has ~2 short prose paragraphs and a large code block.
        # If code were counted, words would be >> 100. Prose alone is ~20-30.
        assert m.words < 50, f"Code block inflated word count: {m.words}"

    def test_frontmatter_excluded_from_word_count(self):
        _measure("frontmatter_and_code.md")
        # Frontmatter has 'title', 'description', etc. — those words must not count.
        # The word "frontmatter" appears only in the YAML block.
        stripped = pwm.strip_code_and_frontmatter(
            (FIXTURES / "frontmatter_and_code.md").read_text()
        )
        assert "frontmatter" not in stripped.lower()

    def test_empty_doc(self):
        m = _measure("empty.md")
        assert m.words == 0
        assert m.sentences == 0
        assert m.paragraphs == 0


# ---------------------------------------------------------------------------
# P0-2: bracket_tags renamed, no longer claims "citations"
# ---------------------------------------------------------------------------


class TestP0_2_BracketTags:
    def test_bracket_tags_in_prose_counted(self):
        m = _measure("bracket_tags_in_code.md")
        # Prose has [VERIFIED], [DERIVED], [UNVERIFIED] = 3 tags
        assert m.bracket_tags == 3

    def test_bracket_tags_in_code_excluded(self):
        m = _measure("bracket_tags_in_code.md")
        # [SHOULD NOT COUNT] and [ALSO EXCLUDED] are inside a code fence
        # [NOT COUNTED] is inside inline code
        # None of those should appear in examples
        for ex in m.bracket_tag_examples:
            assert "SHOULD NOT COUNT" not in ex
            assert "ALSO EXCLUDED" not in ex
            assert "NOT COUNTED" not in ex


# ---------------------------------------------------------------------------
# P1-3: links_total documentation (structural, not a code fix — verify formula)
# ---------------------------------------------------------------------------


class TestP1_3_LinksTotalFormula:
    def test_total_equals_inline_plus_autolink_plus_ref_use(self):
        m = _measure("links_mixed.md")
        assert m.links_total == m.links_inline + m.links_autolink + m.links_reference_use

    def test_ref_definitions_not_in_total(self):
        m = _measure("links_mixed.md")
        assert m.links_reference_definitions > 0
        # Total should NOT include ref definitions
        assert m.links_total == m.links_inline + m.links_autolink + m.links_reference_use


# ---------------------------------------------------------------------------
# P1-4: Setext headings counted
# ---------------------------------------------------------------------------


class TestP1_4_SetextHeadings:
    def test_setext_h1(self):
        m = _measure("setext_only.md")
        assert m.headings["h1"] == 1, f"Expected 1 setext h1, got {m.headings['h1']}"

    def test_setext_h2(self):
        m = _measure("setext_only.md")
        assert m.headings["h2"] == 2, f"Expected 2 setext h2, got {m.headings['h2']}"

    def test_all_heading_levels(self):
        m = _measure("all_headings.md")
        assert m.headings["h1"] == 2  # 1 ATX + 1 setext
        assert m.headings["h2"] == 2  # 1 ATX + 1 setext
        assert m.headings["h3"] == 1
        assert m.headings["h4"] == 1
        assert m.headings["h5"] == 1
        assert m.headings["h6"] == 1
        assert m.headings_total == 8


# ---------------------------------------------------------------------------
# P1-6: REF_LINK_DEF_RE tightened
# ---------------------------------------------------------------------------


class TestP1_6_RefLinkDefTightened:
    def test_note_like_pattern_not_matched(self):
        m = _measure("ref_link_false_positive.md")
        # [Note]: this is important — not a URL, should not match
        # [TBD]: needs work — not a URL, should not match
        # [real-ref]: https://example.com/real — real ref def, should match
        assert m.links_reference_definitions == 1

    def test_real_ref_def_still_matches(self):
        m = _measure("links_mixed.md")
        # [ref-id]: https://ref.example.com  and  [another-ref]: https://another.example.com
        assert m.links_reference_definitions == 2


# ---------------------------------------------------------------------------
# P2-7: Bare URLs
# ---------------------------------------------------------------------------


class TestP2_7_BareUrls:
    def test_bare_urls_counted_excluding_inline_and_autolinks(self):
        # Two plain URLs in prose. The fixture also has an inline link
        # [..](https://inline.example.com) and an autolink <https://auto.example.com>,
        # neither of which counts as bare.
        m = _measure("bare_urls.md")
        assert m.bare_urls == 2


# ---------------------------------------------------------------------------
# P2-8: Tables and code blocks
# ---------------------------------------------------------------------------


class TestP2_8_TablesAndCodeBlocks:
    def test_tables_counted(self):
        m = _measure("tables_and_code.md")
        assert m.tables == 2

    def test_code_blocks_counted(self):
        m = _measure("tables_and_code.md")
        assert m.code_blocks == 2


# ---------------------------------------------------------------------------
# P2-10: Words per page configurable
# ---------------------------------------------------------------------------


class TestP2_10_WordsPerPage:
    def test_custom_words_per_page(self):
        m250 = pwm.measure(FIXTURES / "frontmatter_and_code.md", words_per_page=250)
        m300 = pwm.measure(FIXTURES / "frontmatter_and_code.md", words_per_page=300)
        # Same words, different pages
        assert m250.words == m300.words
        if m250.words > 0:
            assert m250.pages >= m300.pages


# ---------------------------------------------------------------------------
# Footnotes (P2-9 golden fixture)
# ---------------------------------------------------------------------------


class TestFootnotes:
    def test_footnote_refs(self):
        m = _measure("footnotes.md")
        # [^1], [^long-note], [^3] in text = 3 refs
        # Plus [^1]:, [^long-note]:, [^3]: in defs also match the ref pattern = 6 total
        assert m.footnote_references == 6

    def test_footnote_defs(self):
        m = _measure("footnotes.md")
        assert m.footnote_definitions == 3


# ---------------------------------------------------------------------------
# Links (P2-9 golden fixture)
# ---------------------------------------------------------------------------


class TestLinks:
    def test_inline_links(self):
        m = _measure("links_mixed.md")
        assert m.links_inline == 2  # two [text](url) links

    def test_autolinks(self):
        m = _measure("links_mixed.md")
        assert m.links_autolink == 1

    def test_ref_uses(self):
        m = _measure("links_mixed.md")
        assert m.links_reference_use == 1

    def test_images(self):
        m = _measure("links_mixed.md")
        assert m.images == 1

    def test_total(self):
        m = _measure("links_mixed.md")
        assert m.links_total == 4  # 2 inline + 1 autolink + 1 ref use

    def test_classify_url_external(self):
        for url in ("https://x.y", "http://x", "ftp://x", "mailto:a@b", "tel:+15551234"):
            assert pwm.classify_url(url) == "external"

    def test_classify_url_internal(self):
        for url in ("../path.md", "./local.md", "data/file.md", "/abs/path", "#anchor"):
            assert pwm.classify_url(url) == "internal"

    def test_external_internal_split_in_mixed(self):
        # links_mixed.md uses all https targets, so all 4 links are external.
        m = _measure("links_mixed.md")
        assert m.links_external == 4
        assert m.links_internal == 0

    def test_internal_paths_classified_correctly(self):
        # links_internal_paths.md: relative paths and anchors only.
        m = _measure("links_internal_paths.md")
        assert m.links_external == 0
        assert m.links_internal == 3
        assert m.links_total == 3


# ---------------------------------------------------------------------------
# B1: banned-register linter (Clarity Rule 4)
# ---------------------------------------------------------------------------


class TestB1_BannedRegister:
    def test_banned_words_in_prose_counted(self):
        m = _measure("banned_register.md")
        # Prose contains: incontrovertibly, paradigm-shifting, crushing it, monumental
        assert m.banned_register_hits == 4

    def test_banned_words_in_code_excluded(self):
        m = _measure("banned_register.md")
        # "incontrovertibly" appears once in code-block, once in prose; only prose counts.
        # "monumental" appears once in inline code, once in prose; only prose counts.
        # If the linter counted code-block content, hits would be > 4.
        assert m.banned_register_hits == 4

    def test_examples_lowercased_unique(self):
        m = _measure("banned_register.md")
        assert "incontrovertibly" in m.banned_register_examples
        assert "monumental" in m.banned_register_examples
        # Examples are lowercased and deduplicated
        assert all(e == e.lower() for e in m.banned_register_examples)
        assert len(m.banned_register_examples) == len(set(m.banned_register_examples))

    def test_clean_doc_has_zero_hits(self):
        m = _measure("all_headings.md")
        assert m.banned_register_hits == 0

    def test_word_boundaries_respected(self):
        # "dominant" is on the banned list. Make sure "predominantly" doesn't match.
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("Predominantly cloudy weather. Domination is not the goal.\n")
            tmp_path = Path(f.name)
        try:
            m = pwm.measure(tmp_path)
            assert m.banned_register_hits == 0
        finally:
            tmp_path.unlink()

    def test_custom_banned_words(self):
        custom_re = pwm._compile_banned_words(("crushing it",))
        m = pwm.measure(FIXTURES / "banned_register.md", banned_re=custom_re)
        assert m.banned_register_hits == 1
        assert m.banned_register_examples == ["crushing it"]

    def test_empty_word_list_matches_nothing(self):
        empty_re = pwm._compile_banned_words(())
        m = pwm.measure(FIXTURES / "banned_register.md", banned_re=empty_re)
        assert m.banned_register_hits == 0


# ---------------------------------------------------------------------------
# B14: reproducibility regression for metrics output
# ---------------------------------------------------------------------------
#
# Fixture-locked metrics YAML: when flexdoc/flowmark or our own heuristics
# change behavior, this test fails loudly so the maintainer must either bless
# the new output or pin the upstream version.
#
# To bless a new output (intentional change): regenerate the expected YAML via
#   uv run pprose metrics \
#     tests/test_fixtures/practical_prose_metrics/<fixture>.md --format=yaml \
#     > tests/test_fixtures/practical_prose_metrics/expected/<fixture>.yaml
# and inspect the diff before committing.
#
# Fixtures are chosen to cover the main heuristic surfaces — headings, links,
# prose extraction, and the banned-register linter. Pinning every fixture is
# unnecessary; pinning a representative few catches drift early.


class TestB14_ReproducibilityRegression:
    @pytest.mark.parametrize(
        "fixture_name",
        ["all_headings", "links_mixed", "frontmatter_and_code", "banned_register"],
    )
    def test_metrics_output_matches_pinned_expected(self, fixture_name: str):
        from dataclasses import asdict

        import yaml

        expected_path = FIXTURES / "expected" / f"{fixture_name}.yaml"
        if not expected_path.is_file():
            pytest.fail(
                f"missing expected YAML: {expected_path}\n"
                f"regenerate via: uv run pprose metrics "
                f"{FIXTURES / f'{fixture_name}.md'} --format=yaml > {expected_path}"
            )

        actual = asdict(_measure(f"{fixture_name}.md"))
        actual.pop("file", None)  # path is environment-dependent

        expected_list = yaml.safe_load(expected_path.read_text(encoding="utf-8"))
        assert isinstance(expected_list, list) and len(expected_list) == 1
        expected = expected_list[0]
        expected.pop("file", None)

        assert actual == expected, (
            f"metrics output drift for {fixture_name}; "
            f"if intentional, regenerate expected YAML (see test docstring)"
        )


# ---------------------------------------------------------------------------
# JSON / human output format smoke tests
# ---------------------------------------------------------------------------


class TestOutputFormats:
    def test_format_human_runs(self):
        m = _measure("all_headings.md")
        out = pwm.format_human(m)
        assert "Headings" in out
        assert "Bracket tags" in out
        assert "bare URLs" in out

    def test_format_summary_table_runs(self):
        m1 = _measure("all_headings.md")
        m2 = _measure("footnotes.md")
        out = pwm.format_summary_table([m1, m2])
        assert "btags" in out

    def test_json_roundtrip(self):
        import json
        from dataclasses import asdict

        m = _measure("links_mixed.md")
        d = asdict(m)
        j = json.dumps(d)
        loaded = json.loads(j)
        assert loaded["links_total"] == m.links_total
        assert loaded["bracket_tags"] == m.bracket_tags


# ---------------------------------------------------------------------------
# CLI argv path (main): --format dispatch, multi-file summary, --banned-words-file.
# The other tests call measure()/format_* directly; these drive main(argv).
# ---------------------------------------------------------------------------


class TestCliArgvPath:
    def test_yaml_single_file_emits_one_element_list(self, capsys: pytest.CaptureFixture[str]):
        rc = pwm.main([str(FIXTURES / "all_headings.md"), "--format", "yaml"])
        out = capsys.readouterr().out
        assert rc == 0
        # YAML sequence even for a single file (leading "- ", one "file:" entry).
        assert out.startswith("- ")
        assert out.count("\n- file:") + out.startswith("- file:") == 1

    def test_json_single_file_is_list_of_one(self, capsys: pytest.CaptureFixture[str]):
        import json

        rc = pwm.main([str(FIXTURES / "all_headings.md"), "--format", "json"])
        assert rc == 0
        loaded = json.loads(capsys.readouterr().out)
        assert isinstance(loaded, list)
        assert len(loaded) == 1
        assert "headings" in loaded[0]

    def test_multi_file_renders_summary_table(self, capsys: pytest.CaptureFixture[str]):
        rc = pwm.main([str(FIXTURES / "all_headings.md"), str(FIXTURES / "links_mixed.md")])
        out = capsys.readouterr().out
        assert rc == 0
        # The >1-file branch uses format_summary_table (one row per file).
        assert "all_headings" in out and "links_mixed" in out

    def test_nonexistent_file_warns_and_exits_1(self, capsys: pytest.CaptureFixture[str]):
        rc = pwm.main([str(FIXTURES / "does_not_exist.md")])
        assert rc == 1
        assert "not a file" in capsys.readouterr().err

    def test_banned_words_file_replaces_default_list(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ):
        import json

        doc = tmp_path / "doc.md"
        # "monumental" is in the default banned list; "frobnicate" is not.
        doc.write_text("This is a monumental and frobnicate result.\n", encoding="utf-8")
        words = tmp_path / "words.txt"
        words.write_text("# custom list\nfrobnicate\n\n", encoding="utf-8")

        rc = pwm.main([str(doc), "--banned-words-file", str(words), "--format", "json"])
        assert rc == 0
        m = json.loads(capsys.readouterr().out)[0]
        assert "frobnicate" in m["banned_register_examples"]
        assert "monumental" not in m["banned_register_examples"]
