from typing import Union
from unittest import TestCase


class Converter:
    @staticmethod
    def process(raw_num: int) -> str:
        return bin(raw_num)[2:]


class Descriptor:
    def __init__(self, string: str) -> None:
        self.__string: str = string
        self.__substrings: list[Union[str, int]]

    def divide(self) -> None:
        self.__substrings = []

        num: str = ""
        string: str = ""
        for i in range(len(self.__string)):
            if self.__string[i].isdigit():
                num += self.__string[i]
                if string:
                    self.__substrings.append(string)
                    string = ""
            else:
                string += self.__string[i]
                if num:
                    self.__substrings.append(num)
                    num = ""
        if num:
            self.__substrings.append(num)
        if string:
            self.__substrings.append(string)

    def find_nums(self) -> None:
        self.__substrings = [
            int(substring) if substring.isdigit() else substring
            for substring in self.__substrings
        ]

    def convert_nums(self) -> None:
        self.__substrings = [
            Converter.process(substring) if isinstance(substring, int) else substring
            for substring in self.__substrings
        ]

    def build_string(self) -> str:
        return "".join(self.__substrings)

    def get_current_result(self) -> list[Union[str, int]]:
        return self.__substrings


def main() -> None:
    descriptor: Descriptor = Descriptor(input())
    descriptor.divide()
    descriptor.find_nums()
    descriptor.convert_nums()
    print(descriptor.build_string())


if __name__ == "__main__":
    main()


class ConverterTest(TestCase):
    def test_conversation(self) -> None:
        self.assertEqual(Converter.process(4), "100")


class DescriptorTest(TestCase):
    def setUp(self) -> None:
        self.__test_string: str = "121 test test 121"
        self.__descriptor: Descriptor = Descriptor(self.__test_string)

    def test_dividing(self) -> None:
        self.__descriptor.divide()
        self.assertEqual(
            self.__descriptor.get_current_result(), ["121", " test test ", "121"]
        )

    def test_finding_nums(self) -> None:
        self.__descriptor.divide()
        self.__descriptor.find_nums()
        self.assertEqual(
            self.__descriptor.get_current_result(), [121, " test test ", 121]
        )

    def test_converting(self) -> None:
        self.__descriptor.divide()
        self.__descriptor.find_nums()
        self.__descriptor.convert_nums()
        self.assertEqual(
            self.__descriptor.get_current_result(),
            ["1111001", " test test ", "1111001"],
        )

    def test_building_string(self) -> None:
        self.__descriptor.divide()
        self.__descriptor.find_nums()
        self.__descriptor.convert_nums()
        self.assertEqual(self.__descriptor.build_string(), "1111001 test test 1111001")
