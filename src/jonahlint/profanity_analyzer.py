import ast
import re
from pathlib import Path
from typing import List

from jonahlint.constants import COMMENTS_CODE, ERROR_PREFIX
from jonahlint.profanity_checker import ProfanityChecker
from jonahlint.profanity_report import ProfanityReport
from jonahlint.comments_getter import CommentsGetter
from jonahlint.profanity_visitor import ProfanityVisitor
from jonahlint.words_splitter import WordsSplitter


class ProfanityAnalyzer:

    @classmethod
    def analyze_source(cls, source: str, profanity_checker: ProfanityChecker):
        profanity_visitor = ProfanityVisitor(profanity_checker)
        profanity_visitor.visit(ast.parse(source))
        reports_list = profanity_visitor.reports_list
        for comment in CommentsGetter.get_comments(source):
            if comment.content.startswith("noqa:"):
                ignored_ids = cls.get_ignored_ids(comment.content)
                reports_list = [
                    report
                    for report in reports_list
                    if not cls.report_is_ignored(
                        report=report,
                        ignored_ids=ignored_ids,
                        line_number=comment.line_number,
                    )
                ]
            comment_profane_words = profanity_checker.get_profane_words(
                WordsSplitter.split_to_words_list(comment.content)
            )
            reports_list.extend(
                [
                    ProfanityReport(
                        error_id=f"{ERROR_PREFIX}{COMMENTS_CODE + 1}",
                        line_number=comment.line_number,
                        message=(
                            "Comments should not contain profanities. "
                            f'Found "{profane_word}" in a comment.'
                        )
                    )
                    for profane_word in comment_profane_words
                ]
            )
        return reports_list

    @classmethod
    def analyze_file(cls, path: Path, profanity_checker: ProfanityChecker):
        with open(path, mode="r") as pd:
            source = pd.read()
        return cls.analyze_source(source, profanity_checker)

    @classmethod
    def get_ignored_ids(cls, noqa_string: str) -> List[str]:
        return re.split(",[ \t]*", noqa_string.replace("noqa:", "").strip())

    @classmethod
    def report_is_ignored(
        cls, report: ProfanityReport, ignored_ids: List[str], line_number: int
    ) -> bool:
        if report.line_number != line_number:
            return False
        if report.error_id not in ignored_ids:
            return False
        return True
