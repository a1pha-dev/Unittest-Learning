from unittest import TestCase
from unittest.mock import MagicMock, patch


def read_amounts() -> tuple[int, int]:
    raw_string: list[str] = input().split()
    if len(raw_string) != 2:
        raise ValueError
    elif not (raw_string[0].isdigit() and raw_string[1].isdigit()):
        raise TypeError
    return tuple(map(int, raw_string))


def read_data(amount_of_strings: int, amount_of_rows: int) -> list[list[int]]:
    matrix: list[list[int]] = [[]] * amount_of_strings

    string_index: int
    for string_index in range(amount_of_strings):
        raw_string: str = input().split()
        if len(raw_string) != amount_of_rows:
            raise ValueError
        elif not all(substring.isdigit() for substring in raw_string):
            raise TypeError
        matrix[string_index] = list(map(int, raw_string))

    return matrix


def find_max(matrix: list[list[int]]) -> int:
    if not sum(len(string) for string in matrix):
        raise ValueError
    return max(max(string) for string in matrix)


def get_row(matrix: list[list[int]], row_index: int) -> list[int]:
    if row_index >= len(matrix[0]):
        raise ValueError
    return [matrix[i][row_index] for i in range(len(matrix))]


def rotate_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return [get_row(matrix, j) for j in range(len(matrix[0]))]


def find_row_with_max(matrix: list[list[int]]) -> list[list[int]]:
    return list(filter(lambda row: find_max(matrix) in row, rotate_matrix(matrix)))


def main() -> None:
    amount_of_strings: int
    amount_of_rows: int
    amount_of_strings, amount_of_rows = read_amounts()
    matrix: list[list[int]] = read_data(amount_of_strings, amount_of_rows)

    for row in find_row_with_max(matrix):
        print(*row)


if __name__ == "__main__":
    main()


class TestInputAmounts(TestCase):
    @patch("builtins.input", return_value="123 123 123")
    def test_too_many_values(self, mock_input: MagicMock) -> None:
        with self.assertRaises(ValueError):
            read_amounts()
        mock_input.assert_called_once_with()

    @patch("builtins.input", return_value="abc def")
    def test_incorrect_types(self, mock_input: MagicMock) -> None:
        with self.assertRaises(TypeError):
            read_amounts()
        mock_input.assert_called_once_with()

    @patch("builtins.input", return_value="123 123")
    def test_correct(self, mock_input: MagicMock) -> None:
        self.assertEqual(read_amounts(), (123, 123))
        mock_input.assert_called_once_with()


class TestInputData(TestCase):
    def setUp(self):
        self.__amount_of_strings: int = 3
        self.__amount_of_rows: int = 5

    @patch("builtins.input", return_value="1 2 3 4 5 6")
    def test_amount_of_rows_less_than_or_greater_input_rows(
        self, mock_input: MagicMock
    ) -> None:
        with self.assertRaises(ValueError):
            read_data(self.__amount_of_strings, self.__amount_of_rows)

    @patch("builtins.input", return_value="1 1 1 1 1")
    def test_correct(self, mock_input: MagicMock) -> None:
        self.assertEqual(
            read_data(self.__amount_of_strings, self.__amount_of_rows), [[1] * 5] * 3
        )
        mock_input.assert_called()


class TestMatrix(TestCase):
    def setUp(self) -> None:
        self.__matrix: list[list[int]] = [
            [123, 121, 120, 119],
            [457, 121, 222, 119],
            [123, 321, 120, 542],
        ]

    def test_find_max(self) -> None:
        self.assertEqual(find_max(self.__matrix), 542)

    def test_rotate_matrix(self) -> None:
        self.assertEqual(
            rotate_matrix(self.__matrix),
            [[123, 457, 123], [121, 121, 321], [120, 222, 120], [119, 119, 542]],
        )

    def test_get_row(self) -> None:
        self.assertEqual(get_row(self.__matrix, 1), [121, 121, 321])

    def test_find_row_with_max(self) -> None:
        self.assertEqual(
            find_row_with_max(self.__matrix),
            [
                [119, 119, 542],
            ],
        )
