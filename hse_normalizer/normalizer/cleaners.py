import re


class Cleaner:
    __INITIAL_PATTERN = re.compile(r',[^0-9]\s*')
    __YANDEX_PATTERN = re.compile(r'-\s+|\+')
    __FINAL_PATTERN = re.compile(r'[^А-ЯЁа-яё0-9]+')
    __SEPARATOR_PATTERN = re.compile(r'[А-ЯЁа-яё]+\-\d+')

    def __init__(self, line: str) -> None:
        self.__line = line

    def initial_cleaning(self) -> str:
        for match in re.finditer(self.__SEPARATOR_PATTERN, self.__line):
            a, b = match.group().split('-')
            self.__line = self.__line.replace(match.group(), " ".join((a, b)))
        return " ".join(re.sub(self.__INITIAL_PATTERN, ' ', self.__line).split())

    def yandex_markings_cleaning(self) -> str:
        return " ".join(re.sub(self.__YANDEX_PATTERN, ' ', self.__line).split())

    def final_cleaning(self) -> str:
        return " ".join(re.sub(self.__FINAL_PATTERN, ' ', self.__line).split()).lower()
