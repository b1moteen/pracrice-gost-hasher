import unittest

def is_valid_hash(hash_str):
    if not isinstance(hash_str, str):
        return False
    if len(hash_str) != 64:
        return False
    try:
        int(hash_str, 16)
        return True
    except ValueError:
        return False

def parse_reference_hash(input_str):
    if not isinstance(input_str, str):
        return ""
    return input_str.strip()

class TestUtils(unittest.TestCase):
    def test_is_valid_hash_correct(self):
        valid = "a" * 64
        self.assertTrue(is_valid_hash(valid))

    def test_is_valid_hash_incorrect_length(self):
        invalid = "a" * 63
        self.assertFalse(is_valid_hash(invalid))

    def test_is_valid_hash_non_hex(self):
        invalid = "g" * 64
        self.assertFalse(is_valid_hash(invalid))

    def test_parse_reference_hash_strip(self):
        input_str = "  abcd1234\n"
        self.assertEqual(parse_reference_hash(input_str), "abcd1234")

    def test_parse_reference_hash_empty(self):
        input_str = "   "
        self.assertEqual(parse_reference_hash(input_str), "")

if __name__ == "__main__":
    unittest.main() 