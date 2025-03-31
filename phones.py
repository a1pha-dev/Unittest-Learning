from unittest import TestCase


class Descriptor:
    @staticmethod
    def remove_lines(string: str) -> str:
        return string.replace("-", "")

    @staticmethod
    def remove_branches(string: str) -> str:
        return string.replace("(", "").replace(")", "")

    @staticmethod
    def remove_plus(string: str) -> str:
        return string.replace("+", "")

    @staticmethod
    def simplify(string: str) -> str:
        return Descriptor.remove_plus(
            Descriptor.remove_branches(Descriptor.remove_lines(string))
        )

    @staticmethod
    def divide(string: str, default_code: str = "495") -> list[str]:
        if len(string) == 11:
            return [string[1:4], string[4:]]
        elif len(string) == 10:
            return [string[:3], string[3:]]
        elif len(string) == 7:
            return [default_code, string]
        else:
            raise TypeError


class PhoneNumber:
    def __init__(self, code: str, number: str) -> None:
        self.code: str = code
        self.number: str = number

    def __eq__(self, value: "PhoneNumber") -> bool:
        return self.code == value.code and self.number == value.number


def main() -> None:
    new_raw_number: str = input()
    current_raw_numbers: list[str] = [input() for _ in range(3)]

    new_number: PhoneNumber = PhoneNumber(
        *Descriptor.divide(Descriptor.simplify(new_raw_number))
    )
    current_numbers: list[PhoneNumber] = list(
        map(
            lambda raw_number: PhoneNumber(
                *Descriptor.divide(Descriptor.simplify(raw_number))
            ),
            current_raw_numbers,
        )
    )

    for number in current_numbers:
        print("YES" if number == new_number else "NO")


class TestPhoneNumber(TestCase):
    def setUp(self):
        self.__test_code: str = "917"
        self.__test_number: str = "1234567"
        self.__test_phone_number: PhoneNumber = PhoneNumber(
            self.__test_code, self.__test_number
        )

    def test_equals(self) -> None:
        another_test_phone_number: PhoneNumber = PhoneNumber("917", "1234567")
        self.assertTrue(self.__test_phone_number == another_test_phone_number)

    def test_not_equal(self) -> None:
        another_test_phone_number: PhoneNumber = PhoneNumber("123", "1231231")
        self.assertFalse(self.__test_phone_number == another_test_phone_number)


if __name__ == "__main__":
    main()
