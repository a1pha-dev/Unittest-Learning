from unittest import TestCase
from unittest.mock import MagicMock, patch
from sys import stdin


def get_input_value() -> str:
    return stdin.read()


class SymbolStat:
    def __init__(self, symbol: str, amount: int) -> None:
        self.__symbol: str = symbol
        self.__amount: int = amount

    def get_stat(self) -> tuple[str, int]:
        return (self.__symbol, self.__amount)


class SymbolStatsBuilder:
    def __init__(self, string: str) -> None:
        self.__string: str = string
        self.__letters: list[str]
        self.__amounts: list[int]
        self.__data: list[SymbolStat]

    def __remove_spaces(self) -> None:
        self.__string = self.__string.replace(" ", "").replace("\n", "")

    def __define_letters(self) -> None:
        self.__letters = list(set(self.__string))

    def __define_amounts(self) -> None:
        self.__amounts = list(map(lambda letter: self.__string.count(letter), self.__letters))

    def __define_stats(self) -> None:
        self.__data = [SymbolStat(self.__letters[i], self.__amounts[i]) for i in range(len(self.__letters))]

    def __sort_stats(self) -> None:
        self.__data.sort(key=lambda item: item.get_stat()[0])

    def define_values(self) -> None:
        self.__remove_spaces()
        self.__define_letters()
        self.__define_amounts()
        self.__define_stats()
        self.__sort_stats()

    def build_symbol_stats(self) -> dict[str, int]:
        new_data: dict[str, int] = {}
        item: SymbolStat
        for item in self.__data:
            item_data: tuple[str, int] = item.get_stat()
            new_data[item_data[0]] = item_data[1]

        return new_data


class HistogramBuilder:
    def __init__(self, symbol_stats: dict[str, int]):
        self.__symbol_stats: dict[str, int] = symbol_stats
        self.__build_table()

    def __build_table(self):
        raw_table: list[list[str]] = []
        max_width: int = max([item[1] for item in self.__symbol_stats.items()])
        item: tuple[str, int]
        for item in self.__symbol_stats.items():
            record: list[str] = [item[0]]
            record.extend(list(item[1] * "#" + (max_width - item[1]) * " "))
            raw_table.append(record)

        self.__table: list[list[str]] = self.__rotate_table(raw_table, max_width)
        self.__table.reverse()

    def __rotate_table(self, raw_table: list[list[str]], max_width: int) -> list[list[str]]:
        table: list[list[str]] = [[None] * len(raw_table)] * (max_width + 1)
        for i in range(len(table)):
            record: list[str] = []
            for j in range(len(raw_table)):
                record.append(raw_table[j][i])
            table[i] = record

        return table

    def __str__(self):
        return "\n".join("".join(row) for row in self.__table)


def main() -> None:

    string: str = get_input_value()

    stats: SymbolStatsBuilder = SymbolStatsBuilder(string)
    stats.define_values()

    histogram: HistogramBuilder = HistogramBuilder(stats.build_symbol_stats())
    print(str(histogram))


class TestSymbolStat(TestCase):
    def setUp(self) -> None:
        self.__test_symbol_stat: SymbolStat = SymbolStat("a", 10)

    def test_get_stat(self) -> None:
        self.assertEqual(self.__test_symbol_stat.get_stat(), ("a", 10))


class TestSymbolStatBuilder(TestCase):
    def setUp(self) -> None:
        self.__builder: SymbolStatsBuilder = SymbolStatsBuilder("test string")
        self.__builder.define_values()

    def test_building(self) -> None:
        self.assertEqual(
            self.__builder.build_symbol_stats(),
            {"t": 3, "e": 1, "s": 2, "r": 1, "i": 1, "n": 1, "g": 1},
        )


class TestHistogramBuilder(TestCase):
    def setUp(self):
        self.__builder: HistogramBuilder = HistogramBuilder({"e": 1, "g": 1, "i": 1, "n": 1, "r": 1, "s": 2, "t": 3})

    def test_histogram(self):
        self.assertEqual(str(self.__builder), "      #\n     ##\n#######\neginrst")


class TestInput(TestCase):
    @patch("sys.stdin.read", return_value="test test test test\n     test\n\n")
    def test_get_input(self, input_mock: MagicMock) -> None:
        self.assertEqual(get_input_value(), "test test test test\n     test\n\n")
        input_mock.assert_called_once_with()


if __name__ == "__main__":
    main()
