import ast
import re
from pathlib import Path
from typing import List

from jonahlint.profanity_checker import ProfanityChecker
from jonahlint.profanity_report import ProfanityReport
from jonahlint.comments_getter import CommentsGetter
from jonahlint.profanity_visitor import ProfanityVisitor


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
