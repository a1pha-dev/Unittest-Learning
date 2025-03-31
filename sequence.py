from unittest import TestCase
from unittest.mock import MagicMock, patch


def read_length() -> int:
    raw_num: str = input()
    if not raw_num.isdigit():
        raise TypeError
    return int(raw_num)


def read_seq(length: int) -> list[int]:
    raw_seq: list[str] = input().split()

    if not all(substring.replace("-", "").isdigit() for substring in raw_seq):
        raise TypeError
    if len(raw_seq) != length:
        raise ValueError

    return list(map(int, raw_seq))


def choose_elements(seq: list[int]) -> list[int]:
    return seq[1::2]


def main() -> None:
    print(*choose_elements(read_seq(read_length())))


if __name__ == "__main__":
    main()


class TestLengthInput(TestCase):
    @patch("builtins.input", return_value="abc")
    def test_length_input_incorrect(self, mock_input: MagicMock) -> None:
        with self.assertRaises(TypeError):
            read_length()
        mock_input.assert_called_once_with()

    @patch("builtins.input", return_value="123")
    def test_length_input_correct(self, mock_input: MagicMock) -> None:
        self.assertEqual(read_length(), 123)
        mock_input.assert_called_once_with()


class TestSeqInput(TestCase):
    def setUp(self):
        self.__length: int = 5

    @patch("builtins.input", return_value="a b c d e")
    def test_seq_input_incorrect_types(self, mock_input: MagicMock) -> None:
        with self.assertRaises(TypeError):
            read_seq(self.__length)
        mock_input.assert_called_once_with()

    @patch("builtins.input", return_value="123")
    def test_seq_input_incorrect_length_not_equal_input_length(self, mock_input: MagicMock) -> None:
        with self.assertRaises(ValueError):
            read_seq(self.__length)
        mock_input.assert_called_once_with()

    @patch("builtins.input", return_value="1 2 3 4 5")
    def test_seq_input_correct(self, mock_input: MagicMock) -> None:
        self.assertEqual(read_seq(self.__length), [1, 2, 3, 4, 5])
        mock_input.assert_called_once_with()

    @patch("builtins.input", return_value="-1 -2 -3 -4 -5")
    def test_seq_input_correct_negative_nums(self, mock_input: MagicMock) -> None:
        self.assertEqual(read_seq(self.__length), [-1, -2, -3, -4, -5])
        mock_input.assert_called_once_with()


class TestSeq(TestCase):
    def test_choose_1(self) -> None:
        seq: list[int] = [100, 20, 4, 318]
        self.assertEqual(choose_elements(seq), [20, 318])

    def test_choose_2(self) -> None:
        seq: list[int] = [42, 7, 59, 7, 212, 47, 777, 66, 89, 6]
        self.assertEqual(choose_elements(seq), [7, 7, 47, 66, 6])

    def test_choose_3(self) -> None:
        seq: list[int] = [74, 83, 150, 70, 1, 86, 2, 11, 76, 72, 2]
        self.assertEqual(choose_elements(seq), [83, 70, 86, 11, 72])
