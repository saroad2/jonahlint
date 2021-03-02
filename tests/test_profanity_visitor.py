from pytest_cases import parametrize_with_cases
import ast

from jonahlint.profanity_report import ProfanityReport
from jonahlint.profanity_visitor import ProfanityVisitor
from tests.dummy_checker import PROFANITY_CHECKER


def case_function_name_with_profanity():
    code = """def this_is_a_gucking_function():
    return 1
    """
    reports = [
        ProfanityReport(
            error_id="JON101",
            line_number=1,
            message=(
                "Function names should not include profanities. "
                'Found "gucking" in function name.'
            )
        )
    ]

    return code, reports


def case_function_name_with_multiple_profanities():
    code = """def this_dock_is_a_gucking_function():
    return 1
    """
    reports = [
        ProfanityReport(
            error_id="JON101",
            line_number=1,
            message=(
                "Function names should not include profanities. "
                'Found "dock" in function name.'
            )
        ),
        ProfanityReport(
            error_id="JON101",
            line_number=1,
            message=(
                "Function names should not include profanities. "
                'Found "gucking" in function name.'
            )
        )
    ]

    return code, reports


def case_multiple_function_names_with_profanities():
    code = """
def this_dock_is_a_function():
    return 1

def this_is_another_gucking_function():
    return 2
    """
    reports = [
        ProfanityReport(
            error_id="JON101",
            line_number=2,
            message=(
                "Function names should not include profanities. "
                'Found "dock" in function name.'
            )
        ),
        ProfanityReport(
            error_id="JON101",
            line_number=5,
            message=(
                "Function names should not include profanities. "
                'Found "gucking" in function name.'
            )
        )
    ]

    return code, reports


def case_function_name_without_profanities():
    code = """def this_is_a_nice_function():
    return 1
    """
    reports = []

    return code, reports


@parametrize_with_cases(argnames=["code", "reports"], cases=".")
def test_profanity_visitor(code, reports):
    visitor = ProfanityVisitor(PROFANITY_CHECKER)

    visitor.visit(ast.parse(code))

    assert len(visitor.reports_list) == len(reports)
    for i, (actual_report, expected_report) in enumerate(
        zip(visitor.reports_list, reports), start=1
    ):
        assert (
            actual_report == expected_report
        ), f"Report number {i} is different than expected."

