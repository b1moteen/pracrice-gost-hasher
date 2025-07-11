import unittest
from unittest.mock import patch, MagicMock

def process_file_and_compare(file_path, reference_hash):
    from gui import gost_hash, compare_hashes
    file_hash = gost_hash(file_path)
    is_match = compare_hashes(file_hash, reference_hash)
    return (file_hash, is_match)

class TestGuiLogic(unittest.TestCase):
    @patch("gui.gost_hash")
    @patch("gui.compare_hashes")
    def test_process_file_and_compare_success(self, mock_compare, mock_hash):
        mock_hash.return_value = "abc123"
        mock_compare.return_value = True
        result = process_file_and_compare("file.txt", "abc123")
        self.assertEqual(result, ("abc123", True))

    @patch("gui.gost_hash")
    @patch("gui.compare_hashes")
    def test_process_file_and_compare_mismatch(self, mock_compare, mock_hash):
        mock_hash.return_value = "abc123"
        mock_compare.return_value = False
        result = process_file_and_compare("file.txt", "def456")
        self.assertEqual(result, ("abc123", False))

    @patch("gui.gost_hash", side_effect=FileNotFoundError)
    def test_process_file_and_compare_file_not_found(self, mock_hash):
        with self.assertRaises(FileNotFoundError):
            process_file_and_compare("nofile.txt", "abc123")

    @patch("gui.gost_hash", side_effect=TypeError)
    def test_process_file_and_compare_invalid_file(self, mock_hash):
        with self.assertRaises(TypeError):
            process_file_and_compare(12345, "abc123")

if __name__ == "__main__":
    unittest.main() 