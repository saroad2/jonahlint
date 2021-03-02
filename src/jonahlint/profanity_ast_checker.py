import re
from abc import ABC, abstractmethod
import ast
from typing import List

from jonahlint.profanity_checker import ProfanityChecker
from jonahlint.profanity_report import ProfanityReport


class ProfanityASTChecker(ABC):
    ERROR_PREFIX = "JON"
    SNAKE_CASE = r"[a-zA-Z0-9]+(_+[A-Za-z0-9]+)*"
    CAMEL_CASE = r"([A-Z][a-z0-9]+)+"

    def __init__(self, profanity_checker: ProfanityChecker, code: int):
        self.profanity_checker = profanity_checker
        self.code = code

    def check(self, node: ast.AST) -> List[ProfanityReport]:
        return [
            self.build_report(
                profanity=profanity, line_number=node.lineno
            )
            for profanity in self.get_profanities(node)
        ]

    def build_report(self, profanity: str, line_number: int) -> ProfanityReport:
        return ProfanityReport(
            error_id=self.build_error_id(),
            line_number=line_number,
            message=self.build_message(profanity),
        )

    def build_error_id(self):
        return f"{self.ERROR_PREFIX}{self.code}"

    @abstractmethod
    def build_message(self, profanity: str) -> str:
        ...

    @abstractmethod
    def get_profanities(self, node: ast.AST) -> List[str]:
        ...

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
        if 0 not in upper_indices:
            upper_indices.insert(0, 0)
        if len(upper_indices) < 2:
            return [name]
        return [
            name[i: j] for i, j in zip(upper_indices, upper_indices[1:])
        ]


class FunctionNameChecker(ProfanityASTChecker):
    CODE = 101

    def __init__(self, profanity_checker: ProfanityChecker):
        super().__init__(
            profanity_checker=profanity_checker,
            code=self.CODE,
        )

    def build_message(self, profanity: str) -> str:
        return (
            "Function names should not include profanities. "
            f'Found "{profanity}" in function name.'
        )

    def get_profanities(self, node: ast.AST) -> List[str]:
        return self.profanity_checker.get_profane_words(
            self.name_to_words_list(node.name)
        )
