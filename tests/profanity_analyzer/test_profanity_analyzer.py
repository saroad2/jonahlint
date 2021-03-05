import importlib
import pkgutil
from pathlib import Path

from pytest_cases import parametrize_with_cases

from jonahlint.profanity_analyzer import ProfanityAnalyzer
from tests.dummy_checker import PROFANITY_CHECKER

cases_path = Path(__file__).parent / "cases"
cases_list = [
    importlib.import_module(f"tests.profanity_analyzer.cases.{name}")
    for _, name, _ in pkgutil.iter_modules([cases_path])
]


def assert_reports(actual_reports, expected_reports):
    assert len(actual_reports) == len(expected_reports)
    for i, (actual_report, expected_report) in enumerate(
        zip(actual_reports, expected_reports), start=1
    ):
        assert (
            actual_report == expected_report
        ), f"Report number {i} is different than expected."


@parametrize_with_cases(argnames=["code", "expected_reports"], cases=cases_list)
def test_analyze_source(code, expected_reports):
    profanity_analyzer = ProfanityAnalyzer(profanity_checker=PROFANITY_CHECKER)
    actual_reports = profanity_analyzer.analyze_source(code)
    assert_reports(actual_reports=actual_reports, expected_reports=expected_reports)


@parametrize_with_cases(argnames=["code", "expected_reports"], cases=cases_list)
def test_analyze_file(code, expected_reports, tmpdir_factory):
    path = Path(tmpdir_factory.mktemp("bla")) / "code.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, mode="w") as pd:
        pd.write(code)
    profanity_analyzer = ProfanityAnalyzer(profanity_checker=PROFANITY_CHECKER)
    actual_reports = profanity_analyzer.analyze_file(path)
    assert_reports(actual_reports=actual_reports, expected_reports=expected_reports)


@parametrize_with_cases(argnames=["code", "expected_reports"], cases=cases_list)
def test_analyze_source_ignore_code(code, expected_reports):
    error_ids = {report.error_id for report in expected_reports}
    for error_id in error_ids:
        profanity_analyzer = ProfanityAnalyzer(
            profanity_checker=PROFANITY_CHECKER, ignored_ids=[error_id]
        )
        actual_reports = profanity_analyzer.analyze_source(code)
        assert_reports(
            actual_reports=actual_reports,
            expected_reports=[
                report for report in expected_reports if report.error_id != error_id
            ],
        )
