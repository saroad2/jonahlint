from jonahlint.profanity_checker import ProfanityChecker

CHECKER = ProfanityChecker(["googs", "guck", "nitch", "dock", "lussy"])


def test_is_profane_true():
    assert CHECKER.is_profane("googs")


def test_is_profane_false():
    assert not CHECKER.is_profane("goods")


def test_is_profane_uppercase_true():
    assert CHECKER.is_profane("NITCH")


def test_is_profane_uppercase_false():
    assert not CHECKER.is_profane("NITCHE")


def test_get_profane_words():
    assert CHECKER.get_profane_words(
        ["guck", "is", "a", "bad", "word", "just", "like", "dock"]
    ) == ["guck", "dock"]
