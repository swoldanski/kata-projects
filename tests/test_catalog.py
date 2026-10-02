"""Tests for kata-projects catalog structure."""

from pathlib import Path
import pytest


KATA_ROOT = Path(__file__).parent.parent

COLLECTIONS = [
    "dave-thomas-codekata",
    "gaurav-arora-tdd-katas",
    "wonderland-clojure-katas",
    "sensiolabs-poledev-katas",
]

# Accept common variations for requirements section
REQUIREMENTS_VARIANTS = [
    "## Requirements",
    "## Goals",
    "## Goal",
    "## Specification",
    "## Rules",
    "## Kata Questions",
    "## Exercises",
    "## Parts",
    "## Pricing",
    "## TDD Steps",
    "## Approaches",
    "## Algorithm",
    "## Variations",
    "## Features",
]

REQUIRED_SECTIONS = [
    "# ",
    "## Problem",
]


def test_all_collections_exist():
    """Each collection directory should exist."""
    for coll in COLLECTIONS:
        assert (KATA_ROOT / coll).is_dir(), f"Missing collection: {coll}"


def test_each_kata_has_readme():
    """Each kata directory should have a README.md."""
    for coll in COLLECTIONS:
        coll_path = KATA_ROOT / coll
        for kata_dir in coll_path.iterdir():
            if kata_dir.is_dir():
                readme = kata_dir / "README.md"
                assert readme.exists(), f"Missing README.md in {coll}/{kata_dir.name}"


def test_readme_has_required_sections():
    """Each README should have required sections."""
    for coll in COLLECTIONS:
        coll_path = KATA_ROOT / coll
        for kata_dir in coll_path.iterdir():
            if kata_dir.is_dir():
                readme = kata_dir / "README.md"
                content = readme.read_text()
                for section in REQUIRED_SECTIONS:
                    assert section in content, f"Missing '{section}' in {coll}/{kata_dir.name}/README.md"
                # Check for at least one requirements variant
                has_requirements = any(variant in content for variant in REQUIREMENTS_VARIANTS)
                assert has_requirements, f"Missing requirements section (tried: {REQUIREMENTS_VARIANTS}) in {coll}/{kata_dir.name}/README.md"


def test_no_duplicate_kata_names():
    """Kata names should be unique across all collections."""
    seen = {}
    for coll in COLLECTIONS:
        coll_path = KATA_ROOT / coll
        for kata_dir in coll_path.iterdir():
            if kata_dir.is_dir():
                name = kata_dir.name.lower()
                if name in seen:
                    pytest.fail(f"Duplicate kata name: {name} in {seen[name]} and {coll}")
                seen[name] = coll


def test_kata_count_matches_expected():
    """Verify expected kata counts per collection."""
    expected = {
        "dave-thomas-codekata": 21,
        "gaurav-arora-tdd-katas": 16,
        "wonderland-clojure-katas": 7,
        "sensiolabs-poledev-katas": 5,
    }
    for coll, exp_count in expected.items():
        coll_path = KATA_ROOT / coll
        actual = sum(1 for d in coll_path.iterdir() if d.is_dir())
        assert actual == exp_count, f"{coll}: expected {exp_count} katas, found {actual}"


def test_generated_template_files_exist():
    """Each kata should have generated Python template files."""
    for coll in COLLECTIONS:
        coll_path = KATA_ROOT / coll
        for kata_dir in coll_path.iterdir():
            if kata_dir.is_dir():
                # Check for implementation file
                py_files = list(kata_dir.glob("*.py"))
                impl_files = [f for f in py_files if not f.name.startswith("test_")]
                test_files = [f for f in py_files if f.name.startswith("test_")]
                
                assert len(impl_files) == 1, f"Expected 1 implementation file in {coll}/{kata_dir.name}, found {len(impl_files)}: {[f.name for f in impl_files]}"
                assert len(test_files) == 1, f"Expected 1 test file in {coll}/{kata_dir.name}, found {len(test_files)}: {[f.name for f in test_files]}"


def test_template_files_have_correct_structure():
    """Generated templates should have expected structure."""
    for coll in COLLECTIONS:
        coll_path = KATA_ROOT / coll
        for kata_dir in coll_path.iterdir():
            if kata_dir.is_dir():
                py_files = list(kata_dir.glob("*.py"))
                impl_files = [f for f in py_files if not f.name.startswith("test_")]
                test_files = [f for f in py_files if f.name.startswith("test_")]
                
                if impl_files:
                    content = impl_files[0].read_text()
                    # Check for DDD/CQRS markers
                    assert "from typing import" in content, f"Missing typing imports in {impl_files[0]}"
                
                if test_files:
                    content = test_files[0].read_text()
                    # Accept either template names (test_basic_case, test_edge_cases, test_tdd_progression)
                    # or implemented test names (test_* with descriptive names)
                    has_test_methods = any(name in content for name in [
                        "test_basic_case", "test_edge_cases", "test_tdd_progression",
                        "test_simple_pricing", "test_volume_pricing", "test_weight_pricing",
                        "test_buy_n_get_m", "test_tdd_step",
                        "test_estimate_bits", "test_town_records", "test_binary_tree",
                        "test_modem_transfer", "test_binary_search", "test_password",
                        "test_config_optimal", "test_bloom"
                    ])
                    assert has_test_methods, f"Missing test methods in {test_files[0]}"


def test_readme_format_consistency():
    """README files should follow consistent formatting."""
    for coll in COLLECTIONS:
        coll_path = KATA_ROOT / coll
        for kata_dir in coll_path.iterdir():
            if kata_dir.is_dir():
                readme = kata_dir / "README.md"
                content = readme.read_text()
                
                # Should have source link
                assert "Source:" in content or "source:" in content.lower(), f"Missing Source link in {coll}/{kata_dir.name}/README.md"
                
                # Should have code block or examples (unless design-only kata)
                is_design_only = "no coding" in content.lower() or "no code" in content.lower() or "design kata" in content.lower()
                has_code = "```" in content
                assert has_code or is_design_only, f"Missing code examples in {coll}/{kata_dir.name}/README.md"