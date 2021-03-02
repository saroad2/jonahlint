from tests.dummy_checker import PROFANITY_CHECKER


def test_is_profane_true():
    assert PROFANITY_CHECKER.is_profane("googs")


def test_is_profane_false():
    assert not PROFANITY_CHECKER.is_profane("goods")


def test_is_profane_uppercase_true():
    assert PROFANITY_CHECKER.is_profane("NITCH")


def test_is_profane_uppercase_false():
    assert not PROFANITY_CHECKER.is_profane("NITCHE")


def test_get_profane_words():
    assert PROFANITY_CHECKER.get_profane_words(
        ["guck", "is", "a", "bad", "word", "just", "like", "dock"]
    ) == ["guck", "dock"]
