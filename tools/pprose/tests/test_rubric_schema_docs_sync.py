"""rubric_schema.yaml must match the canonical guidelines doc (questions and rule counts).

The guidelines, rubric, and README carry the dimension questions cell-for-cell
identical; rubric_schema.yaml is the machine-readable fourth copy that feeds
validation and the rendered HTML payload. This locks it to the bundled guidelines
mirror (itself locked to docs/ by test_resources_sync) so wording or rule-list
changes cannot drift silently again.
"""

from __future__ import annotations

import re
from pathlib import Path

from pprose import rubric_schema as rs

GUIDELINES_MD = (
    Path(rs.__file__).resolve().parent
    / "resources"
    / "guidelines"
    / "practical-prose-guidelines.md"
)


def _doc_questions(text: str) -> dict[str, str]:
    """Parse the Six Groups, Twenty Dimensions table: label -> question."""
    rows = re.findall(r"^\|[^|]*\|\s*[PEFRGJ]\d+\.\s*(\w+)\s*\|\s*(.*?)\s*\|$", text, flags=re.M)
    return dict(rows)


def _doc_rule_counts(text: str) -> dict[str, int]:
    """Count numbered rules under each dimension's **Rules:** block: label -> count."""
    counts: dict[str, int] = {}
    sections = re.findall(r"^### [PEFRGJ]\d+\. (\w+)\n(.*?)(?=^### |^## )", text, flags=re.M | re.S)
    for label, body in sections:
        rules_at = body.find("**Rules:**")
        assert rules_at != -1, f"no **Rules:** block under dimension {label}"
        counts[label] = len(re.findall(r"^\d+\.\s+\*\*", body[rules_at:], flags=re.M))
    return counts


def test_schema_questions_match_guidelines_table() -> None:
    text = GUIDELINES_MD.read_text(encoding="utf-8")
    doc_q = _doc_questions(text)
    assert len(doc_q) == 20, f"expected 20 table rows, parsed {len(doc_q)}"
    mismatches = {}
    for group in rs.GROUPS:
        for dim in group.dimensions:
            yaml_q = re.sub(r"\s+", " ", dim.question.strip())
            if doc_q.get(dim.label) != yaml_q:
                mismatches[dim.label] = (yaml_q, doc_q.get(dim.label))
    assert not mismatches, (
        "rubric_schema.yaml questions drifted from the guidelines table "
        "(yaml, docs): " + repr(mismatches)
    )


def test_schema_rule_counts_match_guidelines_rules() -> None:
    text = GUIDELINES_MD.read_text(encoding="utf-8")
    doc_counts = _doc_rule_counts(text)
    assert len(doc_counts) == 20
    mismatches = {}
    for group in rs.GROUPS:
        for dim in group.dimensions:
            yaml_count = len(dim.rules)
            if doc_counts.get(dim.label) != yaml_count:
                mismatches[dim.label] = (yaml_count, doc_counts.get(dim.label))
    assert not mismatches, (
        "rubric_schema.yaml rule lists drifted from the guidelines **Rules:** blocks "
        "(yaml, docs): " + repr(mismatches)
    )
