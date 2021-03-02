from pathlib import Path

from pytest_cases import parametrize_with_cases

from jonahlint.profanity_analyzer import ProfanityAnalyzer
from tests.dummy_checker import PROFANITY_CHECKER
from tests.profanity_analyzer import (
    case_function_name, case_function_variable_name, case_class_name
)

cases = [case_function_name, case_function_variable_name, case_class_name]


def assert_reports(actual_reports, expected_reports):
    assert len(actual_reports) == len(expected_reports)
    for i, (actual_report, expected_report) in enumerate(
            zip(actual_reports, expected_reports), start=1
    ):
        assert (
                actual_report == expected_report
        ), f"Report number {i} is different than expected."


@parametrize_with_cases(argnames=["code", "expected_reports"], cases=cases)
def test_analyze_source(code, expected_reports):
    actual_reports = ProfanityAnalyzer.analyze_source(
        code, profanity_checker=PROFANITY_CHECKER
    )
    assert_reports(actual_reports=actual_reports, expected_reports=expected_reports)


@parametrize_with_cases(argnames=["code", "expected_reports"], cases=cases)
def test_analyze_file(code, expected_reports, tmpdir_factory):
    path = Path(tmpdir_factory.mktemp("bla")) / "code.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, mode="w") as pd:
        pd.write(code)
    actual_reports = ProfanityAnalyzer.analyze_file(
        path, profanity_checker=PROFANITY_CHECKER
    )
    assert_reports(actual_reports=actual_reports, expected_reports=expected_reports)