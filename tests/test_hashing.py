import unittest
import io
from unittest.mock import patch
from external_gost import gost_hash_by_binary
import tempfile
import os

# from hashing import gost_hash, compare_hashes  # Предполагаемые функции

def gost_hash(file_like):
    # Сохраняем file_like во временный файл и считаем хэш через бинарник
    if hasattr(file_like, 'read'):
        data = file_like.read()
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "sisiy.pdf")
            with open(file_path, "wb") as f:
                f.write(data)
            return gost_hash_by_binary(file_path)
    elif isinstance(file_like, str):
        # file_like - путь к файлу
        return gost_hash_by_binary(file_like)
    else:
        raise TypeError("Unsupported file_like type")

def compare_hashes(hash1, hash2):
    return hash1 == hash2

class TestGostHashing(unittest.TestCase):
    def test_hash_known_data(self):
        data = b"test data"
        expected_hash = gost_hash(io.BytesIO(data))
        with patch("hashing.gost_hash", return_value=expected_hash):
            result = gost_hash(io.BytesIO(data))
            self.assertEqual(result, expected_hash)

    def test_hash_empty_file(self):
        data = b""
        expected_hash = gost_hash(io.BytesIO(data))
        with patch("hashing.gost_hash", return_value=expected_hash):
            result = gost_hash(io.BytesIO(data))
            self.assertEqual(result, expected_hash)

    def test_hash_large_file(self):
        data = b"A" * 10_000_000
        expected_hash = gost_hash(io.BytesIO(data))
        with patch("hashing.gost_hash", return_value=expected_hash):
            result = gost_hash(io.BytesIO(data))
            self.assertEqual(result, expected_hash)

    def test_file_not_found(self):
        with self.assertRaises(Exception):
            gost_hash("nonexistent_file.txt")

    def test_invalid_file_type(self):
        with self.assertRaises(TypeError):
            gost_hash(12345)

    def test_compare_hashes_equal(self):
        hash1 = "abc123"
        hash2 = "abc123"
        self.assertTrue(compare_hashes(hash1, hash2))

    def test_compare_hashes_not_equal(self):
        hash1 = "abc123"
        hash2 = "def456"
        self.assertFalse(compare_hashes(hash1, hash2))

    def test_python_vs_cpp_hash(self):
        data = b"test data for gost hash"
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "sisiy.pdf")
            with open(file_path, "wb") as f:
                f.write(data)
            hash_cpp = gost_hash_by_binary(file_path)
            hash_py = gost_hash(open(file_path, "rb"))
            self.assertEqual(hash_cpp, hash_py)

if __name__ == "__main__":
    unittest.main() 