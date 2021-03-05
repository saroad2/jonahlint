from dataclasses import dataclass
from io import BytesIO
from tokenize import COMMENT, tokenize
from typing import List


@dataclass
class CommentData:

    line_number: int
    content: str


class CommentsGetter:
    @classmethod
    def get_comments(cls, source: str) -> List[CommentData]:
        comments = []
        for token in tokenize(BytesIO(source.encode("utf-8")).readline):
            if token.type == COMMENT:
                comments.append(
                    CommentData(
                        line_number=token.start[0],
                        content=cls.normalize_comment(token.string),
                    )
                )
        return comments

    @classmethod
    def normalize_comment(cls, comment: str):
        return comment[1:].strip()
