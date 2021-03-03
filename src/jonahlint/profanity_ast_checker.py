"""
Groups of checkers:

    Functions and Methods: 100
    Classes: 200
    Variables: 300
    Constants: 400
    Comments: 500
    Imports: 600
"""
import re
from abc import ABC, abstractmethod
import ast
from itertools import chain
from typing import List, Iterator, Union

from jonahlint.profanity_checker import ProfanityChecker
from jonahlint.profanity_report import ProfanityReport


class ProfanityASTChecker(ABC):
    ERROR_PREFIX = "JON"
    SNAKE_CASE = r"^[a-zA-Z0-9]+(_+[A-Za-z0-9]+)+$"
    CAMEL_CASE = r"^([A-Z][a-z0-9]*)+$"

    def __init__(self, profanity_checker: ProfanityChecker, code: int):
        self.profanity_checker = profanity_checker
        self.code = code

    def check(self, node: ast.AST) -> List[ProfanityReport]:
        return [
            self.build_report(
                node=node, profanity=profanity, line_number=node.lineno
            )
            for profanity in self.get_profanities(node)
        ]

    def build_report(
        self, node: ast.AST, profanity: str, line_number: int
    ) -> ProfanityReport:
        return ProfanityReport(
            error_id=self.build_error_id(),
            line_number=line_number,
            message=self.build_message(node=node, profanity=profanity),
        )

    def build_error_id(self):
        return f"{self.ERROR_PREFIX}{self.code}"

    @abstractmethod
    def build_message(self, node: ast.AST, profanity: str) -> str:
        ...  # pragma: no cover

    @abstractmethod
    def get_profanities(self, node: ast.AST) -> List[str]:
        ...  # pragma: no cover

    @classmethod
    def name_to_words_list(cls, name: str) -> List[str]:
        if re.match(cls.SNAKE_CASE, name):
            return re.split("_+", name)
        if re.match(cls.CAMEL_CASE, name):
            return cls.split_camel_case(name)
        return re.split(r"[ \t\n]+", name)

    @classmethod
    def split_camel_case(cls, name: str) -> List[str]:
        upper_indices = [i for i, character in enumerate(name) if character.isupper()]
        if len(upper_indices) < 2:
            return [name]
        return [
            name[i: j] for i, j in zip(upper_indices, upper_indices[1:])
        ]


# Functions: 100


class FunctionNameChecker(ProfanityASTChecker):
    CODE = 101

    def __init__(self, profanity_checker: ProfanityChecker):
        super().__init__(
            profanity_checker=profanity_checker, code=self.CODE
        )

    def build_message(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef],  profanity: str
    ) -> str:
        return (
            "Function names should not include profanities. "
            f'Found "{profanity}" in function name.'
        )

    def get_profanities(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> List[str]:
        return self.profanity_checker.get_profane_words(
            self.name_to_words_list(node.name)
        )


class FunctionParameterNameChecker(ProfanityASTChecker):
    CODE = 102

    def __init__(self, profanity_checker: ProfanityChecker):
        super().__init__(
            profanity_checker=profanity_checker, code=self.CODE
        )

    def build_message(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef],  profanity: str
    ) -> str:
        return (
            "Function parameter names should not include profanities. "
            f'Found "{profanity}" in the name of a parameter '
            f'of the function "{node.name}".'
        )

    def get_profanities(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> List[str]:
        return list(
            chain.from_iterable(
                [
                    self.profanity_checker.get_profane_words(
                        self.name_to_words_list(argname.arg)
                    )
                    for argname in self.get_arguments(node.args)
                ]
            )
        )

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


# Classes: 200


class ClassNameChecker(ProfanityASTChecker):
    CODE = 201

    def __init__(self, profanity_checker: ProfanityChecker):
        super().__init__(
            profanity_checker=profanity_checker, code=self.CODE
        )

    def build_message(self, node: ast.AST,  profanity: str) -> str:
        return (
            "Class names should not include profanities. "
            f'Found "{profanity}" in class name.'
        )

    def get_profanities(self, node: ast.AST) -> List[str]:
        return self.profanity_checker.get_profane_words(
            self.name_to_words_list(node.name)
        )


# Assignments: 300


class AssignmentChecker(ProfanityASTChecker):
    CODE = 301

    def __init__(self, profanity_checker: ProfanityChecker):
        super().__init__(
            profanity_checker=profanity_checker, code=self.CODE
        )

    def build_message(self, node: ast.Assign,  profanity: str) -> str:
        return (
            "Variable name should include profanities. "
            f'Found "{profanity}" in a variable name.'
        )

    def get_profanities(self, node: ast.Assign) -> List[str]:
        assigned_vars = list(
            chain.from_iterable(
                [self.get_names_from_target(target) for target in node.targets]
            )
        )
        return self.profanity_checker.get_profane_words(assigned_vars)

    def get_names_from_target(self, node: ast.AST):
        if isinstance(node, ast.Name):
            return self.name_to_words_list(node.id)
        if isinstance(node, (ast.Tuple, ast.List)):
            return list(
                chain.from_iterable(
                    [self.get_names_from_target(target) for target in node.elts]
                )
            )
        return []


# Constants: 400


class ConstantChecker(ProfanityASTChecker):
    CODE = 401

    def __init__(self, profanity_checker: ProfanityChecker):
        super().__init__(
            profanity_checker=profanity_checker, code=self.CODE
        )

    def build_message(self, node: ast.Constant,  profanity: str) -> str:
        return (
            "Constant value should not include profanities. "
            f'Found "{profanity}" in constant "{node.value}".'
        )

    def get_profanities(self, node: ast.Constant) -> List[str]:
        value = node.value
        if not isinstance(value, str):
            return []
        return self.profanity_checker.get_profane_words(
            self.name_to_words_list(value)
        )
