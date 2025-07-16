#!/usr/bin/env python3
import unittest
import subprocess
import tempfile
import os
import shutil
import sys
import threading
import time
import pytest
try:
    from gostcrypto.gosthash.gost_34_11_2012 import GOST34112012
    HAS_GOSTCRYPTO = True
except ImportError:
    HAS_GOSTCRYPTO = False

if sys.platform == 'win32':
    BINARY_NAME = 'ConsoleApplication2.exe'
else:
    BINARY_NAME = 'ConsoleApplication2'

# Используем актуальный путь к бинарнику
CONSOLE_EXE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ConsoleApplication2', BINARY_NAME))
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
        try:
            result = subprocess.run([exe_path], capture_output=True, text=True, timeout=5)
        except subprocess.TimeoutExpired as e:
            print("TimeoutExpired! STDOUT:", e.stdout)
            print("TimeoutExpired! STDERR:", e.stderr)
            raise
        return result

    def get_console_hash(self, data):
        with open(SISIY_PDF, 'wb') as f:
            f.write(data)
        result = self.run_console()
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        self.assertEqual(result.returncode, 0)
        lines = result.stdout.splitlines()
        hash_line = None
        for l in lines:
            if l and not l.startswith('Stribog-512') and len(l.strip()) == 128:
                hash_line = l.strip()
                break
        if hash_line is None:
            raise RuntimeError(f"Hash line not found!\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        return hash_line

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

    def test_compare_with_reference(self):
        data = b"test data for gost hash"
        reference_hash = "d4743a69cb73e7ed25dea17258c355eac94b361231c2b2fc61c45b7390fc3aa92c4bb9e5382174e200f8649ea0e63309ba78e3d8a6083c0eb9233406502dcb61"
        hash_console = self.get_console_hash(data)
        print(f"hash_console: {hash_console}\nreference:    {reference_hash}")
        self.assertEqual(hash_console.lower(), reference_hash.lower())

    def run_console_with_arg(self, filename, timeout=10):
        exe_path = os.path.join(self.test_dir, BINARY_NAME)
        shutil.copy(CONSOLE_EXE_PATH, exe_path)
        if sys.platform != 'win32':
            os.chmod(exe_path, 0o755)
        fname_only = os.path.basename(filename)
        try:
            result = subprocess.run(
                [exe_path, fname_only],
                capture_output=True, text=True, timeout=timeout,
                cwd=self.test_dir
            )
        except subprocess.TimeoutExpired as e:
            print("TimeoutExpired! STDOUT:", e.stdout)
            print("TimeoutExpired! STDERR:", e.stderr)
            raise
        return result

    def test_cli_argument(self):
        data = b'cli test'
        fname = 'cli_file.bin'
        with open(fname, 'wb') as f:
            f.write(data)
        result = self.run_console_with_arg(fname)
        print('ARGS:', result.args)
        print('STDOUT:', result.stdout)
        print('STDERR:', result.stderr)
        self.assertEqual(result.returncode, 0)
        self.assertIn(f'Stribog-512 hash of {fname}:', result.stdout)

    def test_directory_instead_of_file(self):
        os.mkdir('testdir')
        result = self.run_console_with_arg('testdir')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Error:', result.stderr)

    def test_long_filename(self):
        fname = 'a' * 200 + '.bin'
        with open(fname, 'wb') as f:
            f.write(b'longname')
        result = self.run_console_with_arg(fname)
        self.assertEqual(result.returncode, 0)
        self.assertIn(f'Stribog-512 hash of {fname}:', result.stdout)

    def test_file_no_read_permission(self):
        fname = 'noread.bin'
        with open(fname, 'wb') as f:
            f.write(b'no read')
        os.chmod(fname, 0o000)
        try:
            result = self.run_console_with_arg(fname)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Error:', result.stderr)
        finally:
            os.chmod(fname, 0o644)

    def test_exact_block_size(self):
        data = os.urandom(64)
        fname = 'block64.bin'
        with open(fname, 'wb') as f:
            f.write(data)
        result = self.run_console_with_arg(fname)
        self.assertEqual(result.returncode, 0)
        self.assertIn(f'Stribog-512 hash of {fname}:', result.stdout)

    def test_just_below_and_above_block(self):
        for size in [63, 65]:
            data = os.urandom(size)
            fname = f'block{size}.bin'
            with open(fname, 'wb') as f:
                f.write(data)
            result = self.run_console_with_arg(fname)
            self.assertEqual(result.returncode, 0)
            self.assertIn(f'Stribog-512 hash of {fname}:', result.stdout)

    def test_exact_buffer_size(self):
        data = os.urandom(4096)
        fname = 'buffer4096.bin'
        with open(fname, 'wb') as f:
            f.write(data)
        result = self.run_console_with_arg(fname)
        self.assertEqual(result.returncode, 0)
        self.assertIn(f'Stribog-512 hash of {fname}:', result.stdout)

    def test_large_file_10mb(self):
        data = os.urandom(10 * 1024 * 1024)
        fname = 'large10mb.bin'
        with open(fname, 'wb') as f:
            f.write(data)
        result = self.run_console_with_arg(fname, timeout=60)
        self.assertEqual(result.returncode, 0)
        self.assertIn(f'Stribog-512 hash of {fname}:', result.stdout)

    def test_large_file_100mb(self):
        fname = 'large100mb.bin'
        with open(fname, 'wb') as f:
            f.write(os.urandom(100 * 1024 * 1024))
        result = self.run_console_with_arg(fname, timeout=60)
        self.assertEqual(result.returncode, 0)
        self.assertIn(f'Stribog-512 hash of {fname}:', result.stdout)

    def test_output_format(self):
        data = b'format test'
        fname = 'format.bin'
        with open(fname, 'wb') as f:
            f.write(data)
        result = self.run_console_with_arg(fname)
        lines = result.stdout.splitlines()
        hash_line = None
        for l in lines:
            if l and not l.startswith('Stribog-512') and len(l.strip()) == 128:
                hash_line = l.strip()
                break
        self.assertIsNotNone(hash_line)
        if hash_line is not None:
            self.assertEqual(len(hash_line), 128)
            self.assertTrue(all(c in '0123456789abcdefABCDEF' for c in hash_line))

    def test_error_message_on_empty_arg(self):
        result = self.run_console_with_arg('')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Error:', result.stderr)

    import pytest
    @pytest.mark.xfail(reason='gostcrypto hash does not match reference Stribog-512')
    def test_compare_with_python_gostcrypto(self):
        if not HAS_GOSTCRYPTO:
            self.skipTest('gostcrypto not installed')
        data = b'python gostcrypto'
        fname = 'pygost.bin'
        with open(fname, 'wb') as f:
            f.write(data)
        result = self.run_console_with_arg(fname)
        self.assertEqual(result.returncode, 0)
        lines = result.stdout.splitlines()
        hash_line = None
        for l in lines:
            if l and not l.startswith('Stribog-512') and len(l.strip()) == 128:
                hash_line = l.strip()
                break
        self.assertIsNotNone(hash_line)
        if hash_line is not None:
            py_hash = GOST34112012('streebog512', bytearray(data)).hexdigest()
            self.assertEqual(hash_line.lower(), py_hash.lower())

# --- Нестандартные edge/stress тесты ---
def test_long_path():
    base = tempfile.mkdtemp()
    long_name = 'a' * 240 + '.bin'
    path = os.path.join(base, long_name)
    with open(path, 'wb') as f:
        f.write(b'longpath')
    exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ConsoleApplication2', BINARY_NAME))
    result = subprocess.run([exe, path], capture_output=True, text=True, timeout=20)
    shutil.rmtree(base)
    assert result.returncode == 0

def test_unicode_filename():
    with tempfile.TemporaryDirectory() as d:
        fname = os.path.join(d, 'тест_файл_😀.bin')
        with open(fname, 'wb') as f:
            f.write(b'unicode')
        exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ConsoleApplication2', BINARY_NAME))
        result = subprocess.run([exe, fname], capture_output=True, text=True, timeout=20)
        assert result.returncode == 0

def test_special_chars_filename():
    with tempfile.TemporaryDirectory() as d:
        fname = os.path.join(d, 'file !@#$%^&()[]{}.bin')
        with open(fname, 'wb') as f:
            f.write(b'special')
        exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ConsoleApplication2', BINARY_NAME))
        result = subprocess.run([exe, fname], capture_output=True, text=True, timeout=20)
        assert result.returncode == 0

def test_symlink_to_file():
    with tempfile.TemporaryDirectory() as d:
        target = os.path.join(d, 'target.bin')
        link = os.path.join(d, 'link.bin')
        with open(target, 'wb') as f:
            f.write(b'symlink')
        os.symlink(target, link)
        exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ConsoleApplication2', BINARY_NAME))
        result = subprocess.run([exe, link], capture_output=True, text=True, timeout=20)
        assert result.returncode == 0

def test_write_only_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b'writeonly')
        fname = f.name
    os.chmod(fname, 0o222)
    exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ConsoleApplication2', BINARY_NAME))
    try:
        result = subprocess.run([exe, fname], capture_output=True, text=True, timeout=20)
        assert result.returncode != 0
    finally:
        os.chmod(fname, 0o644)
        os.unlink(fname)

def test_file_with_bom():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b'\xef\xbb\xbfBOMtest')
        fname = f.name
    exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ConsoleApplication2', BINARY_NAME))
    result = subprocess.run([exe, fname], capture_output=True, text=True, timeout=20)
    os.unlink(fname)
    assert result.returncode == 0

def test_file_changing_during_hash():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b'A' * 1024 * 1024)
        fname = f.name
    exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ConsoleApplication2', BINARY_NAME))
    def writer():
        with open(fname, 'ab') as wf:
            for _ in range(10):
                wf.write(b'B' * 1024)
                wf.flush()
                time.sleep(0.05)
    t = threading.Thread(target=writer)
    t.start()
    result = subprocess.run([exe, fname], capture_output=True, text=True, timeout=20)
    t.join()
    os.unlink(fname)
    assert result.returncode == 0 or result.returncode == 1  # допускаем ошибку

def test_large_nonblock_size():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(os.urandom(10_000_001))
        fname = f.name
    exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ConsoleApplication2', BINARY_NAME))
    result = subprocess.run([exe, fname], capture_output=True, text=True, timeout=60)
    os.unlink(fname)
    assert result.returncode == 0

@pytest.mark.skipif(os.name != 'posix', reason='immutable/append-only only on Linux')
def test_immutable_file():
    import subprocess as sp
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b'immutable')
        fname = f.name
    sp.run(['sudo', 'chattr', '+i', fname])
    exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ConsoleApplication2', BINARY_NAME))
    try:
        result = subprocess.run([exe, fname], capture_output=True, text=True, timeout=20)
        assert result.returncode == 0
    finally:
        sp.run(['sudo', 'chattr', '-i', fname])
        os.unlink(fname)

@pytest.mark.skipif(os.name != 'posix', reason='append-only only on Linux')
def test_append_only_file():
    import subprocess as sp
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b'appendonly')
        fname = f.name
    sp.run(['sudo', 'chattr', '+a', fname])
    exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ConsoleApplication2', BINARY_NAME))
    try:
        result = subprocess.run([exe, fname], capture_output=True, text=True, timeout=20)
        assert result.returncode == 0
    finally:
        sp.run(['sudo', 'chattr', '-a', fname])
        os.unlink(fname)

def test_parallel_hashing():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(os.urandom(1024 * 1024))
        fname = f.name
    exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ConsoleApplication2', BINARY_NAME))
    def run():
        return subprocess.run([exe, fname], capture_output=True, text=True, timeout=20)
    threads = [threading.Thread(target=run) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    os.unlink(fname)

if __name__ == '__main__':
    print('Запуск тестов ConsoleApplication2...')
    unittest.main() 