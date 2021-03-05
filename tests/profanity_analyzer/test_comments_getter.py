from pytest_cases import parametrize_with_cases
from jonahlint.comments_getter import CommentData, CommentsGetter


def case_standalone_comment():
    code = """a = 2 
# This is a comment
print(min(1, 2, 3))
    """
    expected_comments = [CommentData(line_number=2, content="This is a comment")]
    return code, expected_comments


def case_comment_in_assignment():
    code = "a = 2  # This is a comment"
    expected_comments = [CommentData(line_number=1, content="This is a comment")]
    return code, expected_comments


def case_multiple_comments():
    code = """class A:  # This class is awesome 

    def __init__():  # I am a constructor
        pass
    # I'm a barrier
    
    def f():
        return None  # Nothing is returned!
    """
    expected_comments = [
        CommentData(line_number=1, content="This class is awesome"),
        CommentData(line_number=3, content="I am a constructor"),
        CommentData(line_number=5, content="I'm a barrier"),
        CommentData(line_number=8, content="Nothing is returned!"),
    ]
    return code, expected_comments


@parametrize_with_cases(argnames=["code", "expected_comments"], cases=".")
def test_comments_getter(code, expected_comments):
    assert CommentsGetter.get_comments(code) == expected_comments
