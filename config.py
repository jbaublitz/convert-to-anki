"""
Handle parsing TOML entries.
"""

from tomllib import load
from typing import Self


class Entry:
    """
    A single entry in the TOML file.
    """

    #  pylint: disable=too-many-arguments
    #  pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        word: str,
        definition: str,
        gender: str | None,
        aspect: str | None,
        usage: str | None,
        part_of_speech: str | None,
        charts: list[list[list[str]]] | None,
    ):
        self.word = word
        self.definition = definition
        self.gender = gender
        self.aspect = aspect
        self.usage = usage
        self.part_of_speech = part_of_speech
        self.charts = charts

    def get_word(self) -> str:
        """
        Get word.
        """
        return self.word

    def get_definition(self) -> str:
        """
        Get definition.
        """
        return self.definition

    def get_gender(self) -> str | None:
        """
        Get gender.
        """
        return self.gender

    def get_aspect(self) -> str | None:
        """
        Get aspect.
        """
        return self.aspect

    def get_usage(self) -> str | None:
        """
        Get usage.
        """
        return self.usage

    def get_part_of_speech(self) -> str | None:
        """
        Get part of speech.
        """
        return self.part_of_speech

    def get_charts(self) -> list[list[list[str]]] | None:
        """
        Get charts.
        """
        return self.charts


class Config:
    """
    Generic config data structure.
    """

    def __init__(self, set_name: str, lang: str | None, entries: list[Entry]):
        self.set_name = set_name
        self.lang = lang
        self.words = entries

    def __iter__(self):
        return iter(self.words)

    def __len__(self) -> int:
        return len(self.words)

    def get_set_name(self) -> str:
        """
        Get the language for the set.
        """
        return self.set_name

    def get_lang(self) -> str | None:
        """
        Get the language for the set.
        """
        return self.lang

    def get_words(self) -> list[Entry]:
        """
        Get a list of all words in the TOML file.
        """
        return self.words

    def extend(self, config: Self):
        """
        Extend a TOML config with another TOML config.
        """
        if self.lang != config.lang:
            raise RuntimeError(
                "Languages differ across sets that are attempting to be merged"
            )

        self.words += config.words
        return self


class TomlConfig(Config):
    """
    All entries in the TOML file.
    """

    def __init__(self, file_path: str):
        try:
            with open(file_path, "rb") as file_handle:
                toml = load(file_handle)
                lang = toml.get("lang", None)
                words = [
                    Entry(
                        dct["word"],
                        dct["definition"],
                        dct.get("gender", None),
                        dct.get("aspect", None),
                        dct.get("usage", None),
                        dct.get("part_of_speech", None),
                        dct.get("charts", None),
                    )
                    for dct in toml["words"]
                ]
                super().__init__(file_path, lang, words)
        except KeyError as err:
            raise RuntimeError(f"Key {err} not found") from err
