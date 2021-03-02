import ast

from pytest_cases import parametrize_with_cases

from jonahlint.profanity_visitor import ProfanityVisitor
from tests.dummy_checker import PROFANITY_CHECKER
from tests.profanity_visitor import case_function_name, case_function_variable_name


@parametrize_with_cases(
    argnames=["code", "reports"],
    cases=[case_function_name, case_function_variable_name]
)
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
