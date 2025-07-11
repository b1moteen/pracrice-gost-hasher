#!/usr/bin/env python3
import unittest
import subprocess
import tempfile
import os
import shutil
import sys

if sys.platform == 'win32':
    BINARY_NAME = 'ConsoleApplication2.exe'
else:
    BINARY_NAME = 'ConsoleApplication2'

CONSOLE_EXE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'x64', 'Debug', BINARY_NAME))
SISIY_PDF = 'sisiy.pdf'

class TestConsoleApplication2(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.orig_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.orig_cwd)
        shutil.rmtree(self.test_dir)

    def run_console(self):
        exe_path = os.path.join(self.test_dir, BINARY_NAME)
        shutil.copy(CONSOLE_EXE_PATH, exe_path)
        if sys.platform != 'win32':
            os.chmod(exe_path, 0o755)
        result = subprocess.run([exe_path], capture_output=True, text=True)
        return result

    def test_known_file_hash(self):
        data = b"test data for gost hash"
        with open(SISIY_PDF, 'wb') as f:
            f.write(data)
        result = self.run_console()
        self.assertEqual(result.returncode, 0)
        self.assertIn('Stribog-512 hash of sisiy.pdf:', result.stdout)
        lines = result.stdout.splitlines()
        hash_line = None
        for l in lines:
            if l and not l.startswith('Stribog-512') and len(l.strip()) == 128:
                hash_line = l.strip()
                break
        self.assertIsNotNone(hash_line)
        if hash_line is not None:
            self.assertEqual(len(hash_line), 128)

    def test_file_not_found(self):
        result = self.run_console()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Error:', result.stderr)
        self.assertIn('Cannot open file', result.stderr)

    def test_empty_file(self):
        with open(SISIY_PDF, 'wb') as f:
            pass
        result = self.run_console()
        self.assertEqual(result.returncode, 0)
        self.assertIn('Stribog-512 hash of sisiy.pdf:', result.stdout)
        lines = result.stdout.splitlines()
        hash_line = None
        for l in lines:
            if l and not l.startswith('Stribog-512') and len(l.strip()) == 128:
                hash_line = l.strip()
                break
        self.assertIsNotNone(hash_line)
        if hash_line is not None:
            self.assertEqual(len(hash_line), 128)

    def test_non_ascii_file(self):
        data = bytes([0xFF, 0x00, 0xAB, 0xCD, 0xEF, 0x7F, 0x80, 0x81])
        with open(SISIY_PDF, 'wb') as f:
            f.write(data)
        result = self.run_console()
        self.assertEqual(result.returncode, 0)
        self.assertIn('Stribog-512 hash of sisiy.pdf:', result.stdout)
        lines = result.stdout.splitlines()
        hash_line = None
        for l in lines:
            if l and not l.startswith('Stribog-512') and len(l.strip()) == 128:
                hash_line = l.strip()
                break
        self.assertIsNotNone(hash_line)
        if hash_line is not None:
            self.assertEqual(len(hash_line), 128)

    def test_large_file(self):
        data = b'A' * (1024 * 1024)
        with open(SISIY_PDF, 'wb') as f:
            f.write(data)
        result = self.run_console()
        self.assertEqual(result.returncode, 0)
        self.assertIn('Stribog-512 hash of sisiy.pdf:', result.stdout)
        lines = result.stdout.splitlines()
        hash_line = None
        for l in lines:
            if l and not l.startswith('Stribog-512') and len(l.strip()) == 128:
                hash_line = l.strip()
                break
        self.assertIsNotNone(hash_line)
        if hash_line is not None:
            self.assertEqual(len(hash_line), 128)

    def test_one_byte_file(self):
        data = b'Z'
        with open(SISIY_PDF, 'wb') as f:
            f.write(data)
        result = self.run_console()
        self.assertEqual(result.returncode, 0)
        self.assertIn('Stribog-512 hash of sisiy.pdf:', result.stdout)
        lines = result.stdout.splitlines()
        hash_line = None
        for l in lines:
            if l and not l.startswith('Stribog-512') and len(l.strip()) == 128:
                hash_line = l.strip()
                break
        self.assertIsNotNone(hash_line)
        if hash_line is not None:
            self.assertEqual(len(hash_line), 128)

    def test_repeated_bytes_file(self):
        data = b'\xAB' * 100
        with open(SISIY_PDF, 'wb') as f:
            f.write(data)
        result = self.run_console()
        self.assertEqual(result.returncode, 0)
        self.assertIn('Stribog-512 hash of sisiy.pdf:', result.stdout)
        lines = result.stdout.splitlines()
        hash_line = None
        for l in lines:
            if l and not l.startswith('Stribog-512') and len(l.strip()) == 128:
                hash_line = l.strip()
                break
        self.assertIsNotNone(hash_line)
        if hash_line is not None:
            self.assertEqual(len(hash_line), 128)

    def test_file_with_null_byte(self):
        data = b'abc\x00def'
        with open(SISIY_PDF, 'wb') as f:
            f.write(data)
        result = self.run_console()
        self.assertEqual(result.returncode, 0)
        self.assertIn('Stribog-512 hash of sisiy.pdf:', result.stdout)
        lines = result.stdout.splitlines()
        hash_line = None
        for l in lines:
            if l and not l.startswith('Stribog-512') and len(l.strip()) == 128:
                hash_line = l.strip()
                break
        self.assertIsNotNone(hash_line)
        if hash_line is not None:
            self.assertEqual(len(hash_line), 128)

if __name__ == '__main__':
    print('Запуск тестов ConsoleApplication2...')
    unittest.main() 