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


def read_data(amount_of_strings: int, amount_of_rows: int) -> list[list[str]]:
    matrix: list[list[str]] = [[]] * amount_of_strings

    string_index: int
    for string_index in range(amount_of_strings):
        raw_string: str = input().split()
        if len(raw_string) != amount_of_rows:
            raise ValueError
        elif not all(substring in "01" for substring in raw_string):
            raise TypeError
        matrix[string_index] = raw_string

    return matrix


def get_row(matrix: list[list[int]], row_index: int) -> list[int]:
    if row_index >= len(matrix[0]):
        raise ValueError
    return [matrix[i][row_index] for i in range(len(matrix))]


def rotate_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return [get_row(matrix, j) for j in range(len(matrix[0]))]


def find_horizontal_lines(matrix: list[list[str]]) -> list[int]:
    answer: list[int] = []
    for i, row in enumerate(matrix):
        if row.count("0") == 0:
            answer.append(i)

    return answer


def find_vertical_lines(matrix: list[list[str]]) -> list[int]:
    answer: list[int] = []
    for j, column in enumerate(rotate_matrix(matrix)):
        if not column.count("0"):
            answer.append(j)

    return answer


def find_distance(seq: list[int]) -> int:
    distance: int = seq[1] - seq[0] - 1 if len(seq) > 1 else 0
    for i in range(1, len(seq) - 1):
        if seq[i + 1] - seq[i] - 1 != distance:
            return -1
    return distance


def is_square(horizontal: list[int], vertical: list[int]) -> bool:
    if len(horizontal) == 1 and len(vertical) == 1:
        return True

    horizontal_distance: int = find_distance(horizontal)
    vertical_distance: int = find_distance(vertical)

    return (
        horizontal_distance > 0
        and vertical_distance > 0
        and horizontal_distance == horizontal_distance
        or horizontal_distance > 0
        and len(vertical) == 1
    )


def is_line(horizontal: list[int], vertical: list[int], width: int) -> bool:
    return not vertical and horizontal and width > find_distance(horizontal) > 0


def is_vertical_line(horizontal: list[int], vertical: list[int], height: int) -> bool:
    return vertical and not horizontal and height > find_distance(vertical) > 0


def define_type(matrix: list[list[str]]) -> str:
    horizontal: list[int] = find_horizontal_lines(matrix)
    vertical: list[int] = find_vertical_lines(matrix)

    if is_square(horizontal, vertical):
        return "Square"
    if is_line(horizontal, vertical, len(matrix[0])):
        return "Line"
    if is_vertical_line(horizontal, vertical, len(matrix)):
        return "Vertical line"
    return "?"


def main() -> None:
    amount_of_strings: int
    amount_of_rows: int
    amount_of_strings, amount_of_rows = read_amounts()
    matrix: list[list[int]] = read_data(amount_of_strings, amount_of_rows)

    print(define_type(matrix))


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

    @patch("builtins.input", return_value="0 0 0 0 0 0")
    def test_amount_of_rows_less_than_or_greater_input_rows(
        self, mock_input: MagicMock
    ) -> None:
        with self.assertRaises(ValueError):
            read_data(self.__amount_of_strings, self.__amount_of_rows)

    @patch("builtins.input", return_value="1 1 1 1 1")
    def test_correct(self, mock_input: MagicMock) -> None:
        self.assertEqual(
            read_data(self.__amount_of_strings, self.__amount_of_rows), [["1"] * 5] * 3
        )
        mock_input.assert_called()


class TestMatrix(TestCase):
    def setUp(self) -> None:
        self.__matrix: list[list[str]] = [["0"] * 5, ["1"] * 5, ["0"] * 5, ["1"] * 5]
        self.__horizontal: list[int] = find_horizontal_lines(self.__matrix)
        self.__vertical: list[int] = find_vertical_lines(self.__matrix)

    def test_rotate_matrix(self) -> None:
        self.assertEqual(
            rotate_matrix(self.__matrix),
            [["0", "1", "0", "1"]] * 5,
        )

    def test_get_row(self) -> None:
        self.assertEqual(get_row(self.__matrix, 1), ["0", "1", "0", "1"])

    def test_horizontal_lines(self) -> None:
        self.assertEqual(find_horizontal_lines(self.__matrix), [1, 3])

    def test_vertical_lines(self) -> None:
        self.assertEqual(find_vertical_lines(self.__matrix), [])

    def test_define_type(self) -> None:
        self.assertEqual(define_type(self.__matrix), "Line")

    def test_find_distance(self) -> None:
        self.assertEqual(find_distance([1, 3, 5, 7]), 1)

    def test_is_square(self) -> None:
        self.assertFalse(is_square(self.__horizontal, self.__vertical))

    def test_is_line(self) -> None:
        self.assertTrue(
            is_line(self.__horizontal, self.__vertical, len(self.__matrix[0]))
        )

    def test_is_vertical_line(self) -> None:
        self.assertFalse(
            is_vertical_line(self.__horizontal, self.__vertical, len(self.__matrix))
        )
