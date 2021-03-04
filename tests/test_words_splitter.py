from pytest_cases import parametrize_with_cases

from jonahlint.words_splitter import WordsSplitter


def case_lower_case_single_word():
    word = "word"
    splitted = ["word"]
    return word, splitted


def case_upper_case_single_word():
    word = "WORD"
    splitted = ["WORD"]
    return word, splitted


def case_upper_case_single_word_and_number():
    word = "WORD2"
    splitted = ["WORD"]
    return word, splitted


def case_lower_snake_case():
    word = "this_is_snake_case"
    splitted = ["this", "is", "snake", "case"]
    return word, splitted


def case_upper_snake_case():
    word = "THIS_IS_SNAKE_CASE"
    splitted = ["THIS", "IS", "SNAKE", "CASE"]
    return word, splitted


def case_lower_module_path():
    word = "this.is.snake.case"
    splitted = ["this", "is", "snake", "case"]
    return word, splitted


def case_upper_module_path():
    word = "THIS.IS.SNAKE.CASE"
    splitted = ["THIS", "IS", "SNAKE", "CASE"]
    return word, splitted


def case_upper_camel_case():
    word = "ThisIsCamelCase"
    splitted = ["This", "Is", "Camel", "Case"]
    return word, splitted


def case_lower_camel_case():
    word = "thisIsCamelCase"
    splitted = ["this", "Is", "Camel", "Case"]
    return word, splitted


def case_lower_case_sentence():
    word = "this is a sentence"
    splitted = ["this", "is", "a", "sentence"]
    return word, splitted


def case_upper_case_sentence():
    word = "THIS IS A SENTENCE"
    splitted = ["THIS", "IS", "A", "SENTENCE"]
    return word, splitted


def case_camel_case_in_a_sentence():
    word = "You can detect CamelCase inside a sentence"
    splitted = ["You", "can", "detect", "Camel", "Case", "inside", "a", "sentence"]
    return word, splitted


def case_snake_case_in_a_sentence():
    word = "You can detect snake_case inside a sentence"
    splitted = ["You", "can", "detect", "snake", "case", "inside", "a", "sentence"]
    return word, splitted


def case_snake_camel_combo():
    word = "there_is_a_CamelCase_in_this_snake"
    splitted = ["there", "is", "a", "Camel", "Case", "in", "this", "snake"]
    return word, splitted


@parametrize_with_cases(argnames=["word", "splitted"], cases=".")
def test_words_splitter(word, splitted):
    assert WordsSplitter.split_to_words_list(word) == splitted
