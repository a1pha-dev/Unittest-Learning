from unittest import TestCase
from unittest.mock import MagicMock, patch


def read_amounts() -> tuple[int, int]:
    raw_string: list[str] = input().split()
    if len(raw_string) != 2:
        raise ValueError
    elif not (raw_string[0].isdigit() and raw_string[1].isdigit()):
        raise TypeError
    else:
        return tuple(map(int, raw_string))


def read_boarders() -> tuple[int, int, int, int]:
    raw_string: list[str] = input().split()
    if len(raw_string) != 4:
        raise ValueError
    elif not all(substring.isdigit() for substring in raw_string):
        raise TypeError
    else:
        return tuple(map(lambda num: int(num) - 1, raw_string))


def read_data(amount_of_strings: int, amount_of_rows: int) -> list[list[str]]:
    matrix: list[list[str]] = [[]] * amount_of_strings

    string_index: int
    for string_index in range(amount_of_strings):
        raw_string: str = input().split()
        if len(raw_string) != amount_of_rows:
            raise ValueError
        else:
            matrix[string_index] = raw_string

    return matrix


def slice_matrix(
    matrix: list[list[str]],
    row_start: int,
    column_start: int,
    row_end: int,
    column_end: int,
) -> list[list[str]]:
    if (
        row_start >= len(matrix)
        or row_end >= len(matrix)
        or column_start >= len(matrix[0])
        or column_end >= len(matrix[0])
    ):
        raise IndexError
    return [
        matrix[i][column_start : column_end + 1] for i in range(row_start, row_end + 1)
    ]


def find_security_in_matrix(matrix: list[list[str]]) -> int:
    return "".join("".join(row) for row in matrix).count("S")


def main() -> None:
    amount_of_strings: int
    amount_of_rows: int
    amount_of_strings, amount_of_rows = read_amounts()

    matrix: list[list[str]] = read_data(amount_of_strings, amount_of_rows)
    boarders: tuple[int, int, int, int] = read_boarders()

    print(find_security_in_matrix(slice_matrix(matrix, *boarders)))


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

    @patch("builtins.input", return_value="123 123 123 123 123")
    def test_too_many_values(self, mock_input: MagicMock) -> None:
        with self.assertRaises(ValueError):
            read_boarders()
        mock_input.assert_called_once_with()

    @patch("builtins.input", return_value="abc def gfh jkl")
    def test_incorrect_types(self, mock_input: MagicMock) -> None:
        with self.assertRaises(TypeError):
            read_boarders()
        mock_input.assert_called_once_with()

    @patch("builtins.input", return_value="123 123 123 123")
    def test_correct(self, mock_input: MagicMock) -> None:
        self.assertEqual(read_boarders(), (123, 123, 123, 123))
        mock_input.assert_called_once_with()


class TestInputData(TestCase):
    def setUp(self):
        self.__amount_of_strings: int = 3
        self.__amount_of_rows: int = 5

    @patch("builtins.input", return_value="a b c d e f")
    def test_amount_of_rows_less_than_or_greater_input_rows(
        self, mock_input: MagicMock
    ) -> None:
        with self.assertRaises(ValueError):
            read_data(self.__amount_of_strings, self.__amount_of_rows)

    @patch("builtins.input", return_value="a b c d e")
    def test_correct(self, mock_input: MagicMock) -> None:
        self.assertEqual(
            read_data(self.__amount_of_strings, self.__amount_of_rows),
            [["a", "b", "c", "d", "e"]] * 3,
        )
        mock_input.assert_called()


class TestMatrix(TestCase):
    def setUp(self):
        self.__matrix: list[list[str]] = [
            ["N", "M", "b", "1", "R", "L", "N", "K", "S"],
            ["N", "m", "N", "O", "R", "2", "P", "M", "N"],
            ["2", "K", "L", "S", "M", "U", "L", "a", "P"],
            ["S", "U", "s", "s", "R", "Q", "L", "K", "L"],
            ["P", "j", "R", "O", "U", "T", "O", "0", "Q"],
        ]

    def test_slice_huge_borders(self) -> None:
        with self.assertRaises(IndexError):
            slice_matrix(self.__matrix, 20, 20, 30, 30)

    def test_slice(self) -> None:
        self.assertEqual(
            slice_matrix(self.__matrix, 1, 2, 4, 6),
            [
                ["N", "O", "R", "2", "P"],
                ["L", "S", "M", "U", "L"],
                ["s", "s", "R", "Q", "L"],
                ["R", "O", "U", "T", "O"],
            ],
        )

    def test_find_security(self) -> None:
        self.assertEqual(find_security_in_matrix(self.__matrix), 3)
