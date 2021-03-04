import re
from typing import List
from string import ascii_letters
from itertools import chain


class WordsSplitter:
    CAMEL_CASE = r"^[a-z0-9]*[A-Z][a-z0-9]+([A-Z][a-z0-9]*)*$"

    @classmethod
    def split_to_words_list(cls, name: str) -> List[str]:
        if re.match(cls.CAMEL_CASE, name):
            splitted_name = cls.split_camel_case(name)
        else:
            splitted_name = cls.split_by_non_letters(name)
        if len(splitted_name) == 1:
            return splitted_name
        return cls.inner_split(splitted_name)

    @classmethod
    def inner_split(cls, words_list: List[str]) -> List[str]:
        return list(
            chain.from_iterable(
                [cls.split_to_words_list(word) for word in words_list]
            )
        )

    @classmethod
    def split_camel_case(cls, name: str) -> List[str]:
        upper_indices = [i for i, character in enumerate(name) if character.isupper()]
        if len(upper_indices) < 2:
            return [name]
        return cls.cut_word_in_indices(name=name, indices=upper_indices)

    @classmethod
    def split_by_non_letters(cls, name):
        non_asci_indices = [
            i for i, character in enumerate(name) if character not in ascii_letters
        ]
        if len(non_asci_indices) == 0:
            return [name]
        splitted_text = cls.cut_word_in_indices(
            name=name, indices=[index + 1 for index in non_asci_indices]
        )
        splitted_text = [cls.remove_non_letters(word) for word in splitted_text]
        splitted_text = [word for word in splitted_text if word != ""]
        return splitted_text

    @classmethod
    def cut_word_in_indices(cls, name: str, indices: List[int]) -> List[str]:
        if 0 not in indices:
            indices.insert(0, 0)
        splitted_words = [
            name[i: j] for i, j in zip(indices[:-1], indices[1:])
        ]
        splitted_words.append(name[indices[-1]:])
        return splitted_words

    @classmethod
    def remove_non_letters(cls, word: str) -> str:
        return "".join(character for character in word if character in ascii_letters)
