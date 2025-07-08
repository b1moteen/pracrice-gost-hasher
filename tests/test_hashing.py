import unittest
import io
from unittest.mock import patch

# from hashing import gost_hash, compare_hashes  # Предполагаемые функции

def gost_hash(file_like):
    raise NotImplementedError

def compare_hashes(hash1, hash2):
    raise NotImplementedError

class TestGostHashing(unittest.TestCase):
    def test_hash_known_data(self):
        # Проверка корректности хеша для известных данных (заглушка)
        data = b"test data"
        expected_hash = "mocked_hash_value"  # Подставить реальный эталон после реализации
        with patch("hashing.gost_hash", return_value=expected_hash):
            result = gost_hash(io.BytesIO(data))
            self.assertEqual(result, expected_hash)

    def test_hash_empty_file(self):
        # Проверка хеша для пустого файла
        data = b""
        expected_hash = "mocked_empty_hash"
        with patch("hashing.gost_hash", return_value=expected_hash):
            result = gost_hash(io.BytesIO(data))
            self.assertEqual(result, expected_hash)

    def test_hash_large_file(self):
        # Проверка обработки большого файла (например, 10 МБ)
        data = b"A" * 10_000_000
        expected_hash = "mocked_large_hash"
        with patch("hashing.gost_hash", return_value=expected_hash):
            result = gost_hash(io.BytesIO(data))
            self.assertEqual(result, expected_hash)

    def test_file_not_found(self):
        # Проверка обработки ошибки "файл не найден"
        with self.assertRaises(FileNotFoundError):
            gost_hash("nonexistent_file.txt")

    def test_invalid_file_type(self):
        # Проверка обработки ошибки при неверном типе файла
        with self.assertRaises(TypeError):
            gost_hash(12345)  # Некорректный тип

    def test_compare_hashes_equal(self):
        # Проверка совпадения хеша с эталоном
        hash1 = "abc123"
        hash2 = "abc123"
        self.assertTrue(compare_hashes(hash1, hash2))

    def test_compare_hashes_not_equal(self):
        # Проверка несовпадения хеша с эталоном
        hash1 = "abc123"
        hash2 = "def456"
        self.assertFalse(compare_hashes(hash1, hash2))

if __name__ == "__main__":
    unittest.main() 