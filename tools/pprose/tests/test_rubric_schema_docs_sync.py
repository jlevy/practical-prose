"""Keep rubric questions and ordered rule identities aligned across all four copies.

The guidelines, rubric, and README carry the dimension questions cell-for-cell
identical; rubric_schema.yaml is the machine-readable fourth copy that feeds
validation and the rendered HTML payload. This locks it to the bundled guidelines
mirror (itself locked to docs/ by test_resources_sync), the bundled rubric, and the
bundled README so wording, rule identity, or rule order cannot drift silently again.
"""

from __future__ import annotations

import re
from pathlib import Path

from pprose import rubric_schema as rs

PACKAGE_ROOT = Path(rs.__file__).resolve().parent
GUIDELINES_MD = PACKAGE_ROOT / "resources" / "guidelines" / "practical-prose-guidelines.md"
QUESTION_DOCS = {
    "guidelines": GUIDELINES_MD,
    "rubric": PACKAGE_ROOT / "resources" / "guidelines" / "practical-prose-rubric.md",
    "README": PACKAGE_ROOT / "resources" / "about" / "readme.md",
}


def _doc_questions(text: str) -> dict[str, str]:
    """Parse either documented dimension-table shape: label -> question."""
    questions: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 3 and re.fullmatch(r"[PEFRGJ]\d+\.\s*\w+", cells[1]):
            label = cells[1].split(maxsplit=1)[1]
            questions[label] = cells[2]
        elif len(cells) == 4 and cells[0].isdigit() and re.fullmatch(r"\w+", cells[2]):
            questions[cells[2]] = cells[3]
    return questions


def _normalize_rule(text: str) -> str:
    """Normalize prose wrapping and non-semantic terminal punctuation."""
    normalized = re.sub(r"\s+", " ", text.strip()).replace("’", "'")
    return normalized.removesuffix(".")


def _doc_rules(text: str) -> dict[str, list[str]]:
    """Parse ordered bold rule titles under each dimension's **Rules:** block."""
    rules: dict[str, list[str]] = {}
    sections = re.findall(r"^### [PEFRGJ]\d+\. (\w+)\n(.*?)(?=^### |^## )", text, flags=re.M | re.S)
    for label, body in sections:
        rules_at = body.find("**Rules:**")
        assert rules_at != -1, f"no **Rules:** block under dimension {label}"
        titles = re.findall(
            r"^\d+\.\s+\*\*(.*?)\*\*",
            body[rules_at:],
            flags=re.M | re.S,
        )
        rules[label] = [_normalize_rule(title) for title in titles]
    return rules


def test_schema_questions_match_all_document_tables() -> None:
    for doc_name, path in QUESTION_DOCS.items():
        doc_q = _doc_questions(path.read_text(encoding="utf-8"))
        assert len(doc_q) == 20, f"expected 20 table rows in {doc_name}, parsed {len(doc_q)}"
        mismatches = {}
        for group in rs.GROUPS:
            for dim in group.dimensions:
                yaml_q = re.sub(r"\s+", " ", dim.question.strip())
                if doc_q.get(dim.label) != yaml_q:
                    mismatches[dim.label] = (yaml_q, doc_q.get(dim.label))
        assert not mismatches, (
            f"rubric_schema.yaml questions drifted from the {doc_name} table "
            "(yaml, docs): " + repr(mismatches)
        )


def test_schema_ordered_rules_match_guidelines_rules() -> None:
    text = GUIDELINES_MD.read_text(encoding="utf-8")
    doc_rules = _doc_rules(text)
    assert len(doc_rules) == 20
    mismatches = {}
    for group in rs.GROUPS:
        for dim in group.dimensions:
            yaml_rules = [_normalize_rule(rule) for rule in dim.rules]
            expected_titles = doc_rules.get(dim.label, [])
            identities_match = len(yaml_rules) == len(expected_titles) and all(
                yaml_rule.startswith(title)
                for yaml_rule, title in zip(yaml_rules, expected_titles, strict=True)
            )
            if not identities_match:
                mismatches[dim.label] = (yaml_rules, expected_titles)
    assert not mismatches, (
        "rubric_schema.yaml rule identities or order drifted from the guidelines "
        "(yaml, docs): " + repr(mismatches)
    )
