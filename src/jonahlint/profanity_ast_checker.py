from abc import ABC, abstractmethod
import ast
from itertools import chain, product
from typing import List, Union, Tuple

from jonahlint.constants import (
    ERROR_PREFIX,
    FUNCTIONS_AND_METHODS_CODE,
    CLASSES_CODE,
    ASSIGNMENTS_CODE,
    CONSTANTS_CODE, IMPORTS_CODE,
)
from jonahlint.profanity_checker import ProfanityChecker
from jonahlint.profanity_report import ProfanityReport
from jonahlint.words_splitter import WordsSplitter


class ProfanityASTChecker(ABC):

    def __init__(self, profanity_checker: ProfanityChecker):
        self.profanity_checker = profanity_checker

    def check(self, node: ast.AST) -> List[ProfanityReport]:
        return [
            self.build_report(
                node=node, code=code, profanity=profanity, line_number=node.lineno
            )
            for code, profanity in self.get_profanities(node)
        ]

    def build_report(
        self, node: ast.AST, code: int, profanity: str, line_number: int
    ) -> ProfanityReport:
        return ProfanityReport(
            error_id=self.build_error_id(code=code),
            line_number=line_number,
            message=self.build_message(node=node, code=code, profanity=profanity),
        )

    @abstractmethod
    def build_message(self, node: ast.AST, code: int, profanity: str) -> str:
        ...  # pragma: no cover

    @abstractmethod
    def get_profanities(self, node: ast.AST) -> List[Tuple[int, str]]:
        ...  # pragma: no cover

    @classmethod
    def build_error_id(cls, code):
        return f"{ERROR_PREFIX}{code}"

    @classmethod
    def create_code_and_profanities_tuple(
        cls, code: int, profanities: List[str]
    ) -> List[Tuple[int, str]]:
        return [(code, word) for word in profanities]


class FunctionChecker(ProfanityASTChecker):
    FUNCTION_NAME_CODE = FUNCTIONS_AND_METHODS_CODE + 1
    FUNCTION_PARAMETER_CODE = FUNCTIONS_AND_METHODS_CODE + 2

    def build_message(
        self,
        node: Union[ast.FunctionDef, ast.AsyncFunctionDef],
        code: int,
        profanity: str,
    ) -> str:
        if code == self.FUNCTION_NAME_CODE:
            return (
                "Function names should not include profanities. "
                f'Found "{profanity}" in function name.'
            )
        return (
            "Function parameter names should not include profanities. "
            f'Found "{profanity}" in the name of a parameter '
            f'of the function "{node.name}".'
        )

    def get_profanities(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> List[Tuple[int, str]]:
        profanities = []
        profanities.extend(
            self.create_code_and_profanities_tuple(
                self.FUNCTION_NAME_CODE,
                self.profanity_checker.get_profane_words(
                    WordsSplitter.split_to_words_list(node.name)
                ),
            )
        )
        profanities.extend(
            self.create_code_and_profanities_tuple(
                self.FUNCTION_PARAMETER_CODE,
                list(
                    chain.from_iterable(
                        [
                            self.profanity_checker.get_profane_words(
                                WordsSplitter.split_to_words_list(argname.arg)
                            )
                            for argname in self.get_arguments(node.args)
                        ]
                    )
                )
            )
        )
        return profanities

    @classmethod
    def get_arguments(cls, node: ast.arguments):
        arguments = (
            node.posonlyargs
            + node.args
            + node.kw_defaults
            + node.kwonlyargs
            + [node.vararg, node.kwarg]
        )
        return [arg for arg in arguments if arg is not None]


class ClassChecker(ProfanityASTChecker):
    CLASS_NAME_CODE = CLASSES_CODE + 1

    def build_message(self, node: ast.ClassDef, code: int, profanity: str) -> str:
        return (
            "Class names should not include profanities. "
            f'Found "{profanity}" in class name.'
        )

    def get_profanities(self, node: ast.ClassDef) -> List[Tuple[int, str]]:
        return self.create_code_and_profanities_tuple(
            self.CLASS_NAME_CODE,
            self.profanity_checker.get_profane_words(
                WordsSplitter.split_to_words_list(node.name)
            )
        )


class AssignmentChecker(ProfanityASTChecker):
    CODE = ASSIGNMENTS_CODE + 1

    def build_message(self, node: ast.Assign, code: int, profanity: str) -> str:
        return (
            "Variable name should include profanities. "
            f'Found "{profanity}" in a variable name.'
        )

    def get_profanities(self, node: ast.Assign) -> List[Tuple[int, str]]:
        assigned_vars = list(
            chain.from_iterable(
                [self.get_names_from_target(target) for target in node.targets]
            )
        )
        return self.create_code_and_profanities_tuple(
            self.CODE, self.profanity_checker.get_profane_words(assigned_vars)
        )

    def get_names_from_target(self, node: ast.AST):
        if isinstance(node, ast.Name):
            return WordsSplitter.split_to_words_list(node.id)
        if isinstance(node, (ast.Tuple, ast.List)):
            return list(
                chain.from_iterable(
                    [self.get_names_from_target(target) for target in node.elts]
                )
            )
        return []


class ConstantChecker(ProfanityASTChecker):
    CODE = CONSTANTS_CODE + 1

    def build_message(self, node: ast.Constant, code: int, profanity: str) -> str:
        return (
            "Constant value should not include profanities. "
            f'Found "{profanity}" in constant "{node.value}".'
        )

    def get_profanities(self, node: ast.Constant) -> List[Tuple[int, str]]:
        value = node.value
        if not isinstance(value, str):
            return []
        return self.create_code_and_profanities_tuple(
            self.CODE,
            self.profanity_checker.get_profane_words(
                WordsSplitter.split_to_words_list(value)
            )
        )


class ImportChecker(ProfanityASTChecker):
    PACKAGE_OR_MODULE_CODE = IMPORTS_CODE + 1
    IMPORTED_OBJECT_CODE = IMPORTS_CODE + 2
    ALIAS_CODE = IMPORTS_CODE + 3

    def build_message(
        self, node: Union[ast.Import, ast.ImportFrom], code: int, profanity: str
    ) -> str:
        if code == self.PACKAGE_OR_MODULE_CODE:
            return (
                "Module import should not include profanities. "
                f'Found "{profanity}" in import.'
            )
        if code == self.IMPORTED_OBJECT_CODE:
            return (
                "Imported object should not include profanities. "
                f'Found "{profanity}" in import.'
            )
        return (
            "Import alias should not include profanities. "
            f'Found "{profanity}" in import.'
        )

    def get_profanities(
        self, node: Union[ast.Import, ast.ImportFrom]
    ) -> List[Tuple[int, str]]:
        profanities = []
        if isinstance(node, ast.Import):
            names, aliases = self.split_names_and_aliases(node.names)
            profanities.extend(
                self.create_code_and_profanities_tuple(
                    self.PACKAGE_OR_MODULE_CODE,
                    self.profanity_checker.get_profane_words(
                        WordsSplitter.inner_split(names)
                    )
                )
            )
            profanities.extend(self.get_aliases_profanities(aliases))
        if isinstance(node, ast.ImportFrom):
            profanities.extend(
                self.create_code_and_profanities_tuple(
                    self.PACKAGE_OR_MODULE_CODE,
                    self.profanity_checker.get_profane_words(
                        WordsSplitter.split_to_words_list(node.module)
                    )
                )
            )
            names, aliases = self.split_names_and_aliases(node.names)
            profanities.extend(
                self.create_code_and_profanities_tuple(
                    self.IMPORTED_OBJECT_CODE,
                    self.profanity_checker.get_profane_words(
                        WordsSplitter.inner_split(names)
                    )
                )
            )
            profanities.extend(self.get_aliases_profanities(aliases))
        return profanities

    def get_aliases_profanities(self, aliases):
        return self.create_code_and_profanities_tuple(
            self.ALIAS_CODE,
            self.profanity_checker.get_profane_words(
                WordsSplitter.inner_split(aliases)
            )
        )

    @classmethod
    def split_names_and_aliases(
        cls, nodes: List[ast.AST]
    ) -> Tuple[List[str], List[str]]:
        names = []
        aliases = []
        for node in nodes:
            if isinstance(node, ast.alias):
                names.append(node.name)
                if node.asname is not None:
                    aliases.append(node.asname)
        return names, aliases
