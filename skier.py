from unittest import TestCase


class Skier:
    def __init__(self, days: int, init_distance: int = 10) -> None:
        self.__current_day = 1
        self.__daily_distance = init_distance
        self.__days = days

    def go(self) -> None:
        self.__current_day += 1

    def update_distance(self, percent: int = 10) -> None:
        self.__daily_distance *= 1 + percent / 100

    def check_finished(self) -> bool:
        return self.__days == self.__current_day

    def get_distance(self) -> float:
        return self.__daily_distance


class ConsoleInputOutput:
    @staticmethod
    def get_user_input(raw_input: str | None = None) -> int:
        raw_input: str = input() if raw_input is None else raw_input
        if not raw_input.isdigit():
            raise TypeError
        num: int = int(raw_input)
        if not 1 <= num <= 120:
            raise IndexError
        return int(raw_input)

    @staticmethod
    def format_output(output: float) -> str:
        return f"{output:.6f}"


def main() -> None:
    amount_of_days: int = ConsoleInputOutput.get_user_input()
    skier: Skier = Skier(amount_of_days)

    while not skier.check_finished():
        skier.go()
        skier.update_distance()

    print(ConsoleInputOutput.format_output(skier.get_distance()))


if __name__ == "__main__":
    main()


class InputOutputTest(TestCase):
    def test_correct(self) -> None:
        self.assertEqual(ConsoleInputOutput.get_user_input("1"), 1)

    def test_non_numeric(self) -> None:
        with self.assertRaises(TypeError):
            ConsoleInputOutput.get_user_input("test")

    def test_not_in_range(self) -> None:
        with self.assertRaises(IndexError):
            ConsoleInputOutput.get_user_input("123")

    def test_output(self) -> None:
        self.assertEqual(ConsoleInputOutput.format_output(10), "10.000000")


class SkierTest(TestCase):
    def setUp(self) -> None:
        self.__skier = Skier(1)

    def test_go(self) -> None:
        self.assertTrue(self.__skier.check_finished())

    def test_update_distance(self) -> None:
        self.__skier.update_distance()
        self.assertEqual(self.__skier.get_distance(), 11)
