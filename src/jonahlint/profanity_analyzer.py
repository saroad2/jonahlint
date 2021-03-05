import ast
from dataclasses import dataclass, field
import re
from pathlib import Path
from typing import List, Optional

from jonahlint.constants import COMMENTS_CODE, ERROR_PREFIX
from jonahlint.profanity_checker import ProfanityChecker
from jonahlint.profanity_report import ProfanityReport
from jonahlint.comments_getter import CommentsGetter
from jonahlint.profanity_visitor import ProfanityVisitor
from jonahlint.words_splitter import WordsSplitter


@dataclass
class ProfanityAnalyzer:

    profanity_checker: ProfanityChecker
    ignored_ids: List[str] = field(default_factory=list)

    def analyze_source(self, source: str):
        profanity_visitor = ProfanityVisitor(self.profanity_checker)
        profanity_visitor.visit(ast.parse(source))
        reports_list = profanity_visitor.reports_list
        for comment in CommentsGetter.get_comments(source):
            if comment.content.startswith("noqa:"):
                ignored_ids = self.get_ignored_ids(comment.content)
                reports_list = self.remove_ignored_ids(
                    reports_list,
                    ignored_ids=ignored_ids,
                    line_number=comment.line_number,
                )
            comment_profane_words = self.profanity_checker.get_profane_words(
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
        reports_list = self.remove_ignored_ids(
            reports_list, ignored_ids=self.ignored_ids
        )
        return reports_list

    def analyze_file(self, path: Path):
        with open(path, mode="r") as pd:
            source = pd.read()
        return self.analyze_source(source)

    def remove_ignored_ids(
        self,
        reports_list: List[ProfanityReport],
        ignored_ids: List[str],
        line_number: Optional[int] = None
    ):
        return [
            report
            for report in reports_list
            if not self.report_is_ignored(
                report=report,
                ignored_ids=ignored_ids,
                line_number=line_number,
            )
        ]

    @classmethod
    def get_ignored_ids(cls, noqa_string: str) -> List[str]:
        return re.split(",[ \t]*", noqa_string.replace("noqa:", "").strip())

    @classmethod
    def report_is_ignored(
        cls,
        report: ProfanityReport,
        ignored_ids: List[str],
        line_number: Optional[int] = None
    ) -> bool:
        if line_number is not None and report.line_number != line_number:
            return False
        return report.error_id in ignored_ids
