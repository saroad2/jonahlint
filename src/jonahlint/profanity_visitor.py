import ast
from typing import Any

from jonahlint.profanity_checker import ProfanityChecker
from jonahlint.profanity_ast_checker import (
    FunctionNameChecker, FunctionVariableNameChecker
)


class ProfanityVisitor(ast.NodeVisitor):

    def __init__(self, profanity_checker: ProfanityChecker):
        self.reports_list = []
        self.function_name_checker = FunctionNameChecker(
            profanity_checker=profanity_checker
        )
        self.function_variable_name_checker = FunctionVariableNameChecker(
            profanity_checker=profanity_checker
        )
        super().__init__()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.reports_list.extend(self.function_name_checker.check(node))
        self.reports_list.extend(self.function_variable_name_checker.check(node))
        for inner_node in node.body:
            return self.generic_visit(inner_node)

    def clear_reports_list(self):
        self.reports_list.clear()
