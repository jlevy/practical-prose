from __future__ import annotations

from devtools import check_release_version as crv
from pprose import install


def test_matching_tag_passes():
    # Both the bare version and a `v`-prefixed tag must validate against DISCOVERY_VERSION.
    assert crv.verify(install.DISCOVERY_VERSION) == []
    assert crv.verify(f"v{install.DISCOVERY_VERSION}") == []


def test_mismatched_tag_reports_discovery_version():
    problems = crv.verify("9.9.9", discovery_version="0.1.0")
    assert any("DISCOVERY_VERSION" in p for p in problems)


def test_dev_or_local_version_rejected():
    # A PEP 440 dev/local version can't be resolved by `uvx pprose@<pin>`.
    problems = crv.verify("0.1.0.dev3", discovery_version="0.1.0.dev3")
    assert any("not a plain PyPI release" in p for p in problems)


def test_leading_v_is_stripped():
    assert crv.normalize_tag("v1.2.3") == "1.2.3"
    assert crv.normalize_tag("1.2.3") == "1.2.3"


def test_empty_tag_reported():
    assert crv.verify("") == ["empty release tag"]


def test_committed_discovery_version_is_a_real_release():
    # The shipped fallback itself must always be exact-pinnable.
    assert install.is_pypi_release(install.DISCOVERY_VERSION)
