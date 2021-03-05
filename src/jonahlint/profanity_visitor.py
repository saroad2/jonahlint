import ast
from typing import Any

from jonahlint.profanity_ast_checker import (
    AssignmentChecker,
    ClassChecker,
    ConstantChecker,
    FunctionChecker,
    ImportChecker,
)
from jonahlint.profanity_checker import ProfanityChecker


class ProfanityVisitor(ast.NodeVisitor):
    def __init__(self, profanity_checker: ProfanityChecker):
        self.reports_list = []
        self.function_checker = FunctionChecker(profanity_checker=profanity_checker)
        self.class_checker = ClassChecker(profanity_checker=profanity_checker)
        self.assignment_checker = AssignmentChecker(profanity_checker=profanity_checker)
        self.constant_checker = ConstantChecker(profanity_checker=profanity_checker)
        self.import_checker = ImportChecker(profanity_checker=profanity_checker)
        super().__init__()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.reports_list.extend(self.function_checker.check(node))
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        self.reports_list.extend(self.function_checker.check(node))
        return self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.reports_list.extend(self.class_checker.check(node))
        return self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> Any:
        self.reports_list.extend(self.assignment_checker.check(node))
        return self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> Any:
        self.reports_list.extend(self.constant_checker.check(node))
        return self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> Any:
        self.reports_list.extend(self.import_checker.check(node))
        return self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        self.reports_list.extend(self.import_checker.check(node))
        return self.generic_visit(node)
