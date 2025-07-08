import unittest

# from utils import is_valid_hash, parse_reference_hash  # Предполагаемые функции

def is_valid_hash(hash_str):
    raise NotImplementedError

def parse_reference_hash(input_str):
    raise NotImplementedError

class TestUtils(unittest.TestCase):
    def test_is_valid_hash_correct(self):
        # Корректный хеш (строка из 64 hex-символов)
        valid = "a" * 64
        self.assertTrue(is_valid_hash(valid))

    def test_is_valid_hash_incorrect_length(self):
        # Некорректная длина
        invalid = "a" * 63
        self.assertFalse(is_valid_hash(invalid))

    def test_is_valid_hash_non_hex(self):
        # Некорректные символы
        invalid = "g" * 64
        self.assertFalse(is_valid_hash(invalid))

    def test_parse_reference_hash_strip(self):
        # Проверка обработки ввода с пробелами и переводами строк
        input_str = "  abcd1234\n"
        self.assertEqual(parse_reference_hash(input_str), "abcd1234")

    def test_parse_reference_hash_empty(self):
        # Пустой ввод
        input_str = "   "
        self.assertEqual(parse_reference_hash(input_str), "")

if __name__ == "__main__":
    unittest.main() 