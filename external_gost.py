import subprocess
import sys
import os

def gost_hash_by_binary(file_path, binary_path=None):
    if binary_path is None:
        if sys.platform == 'win32':
            binary_name = 'ConsoleApplication2.exe'
        else:
            binary_name = 'ConsoleApplication2'
        binary_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'x64', 'Debug', binary_name))
    temp_dir = os.path.dirname(file_path)
    exe_path = os.path.join(temp_dir, os.path.basename(binary_path))
    if not os.path.exists(exe_path):
        import shutil
        shutil.copy(binary_path, exe_path)
        if sys.platform != 'win32':
            os.chmod(exe_path, 0o755)
    orig_cwd = os.getcwd()
    os.chdir(temp_dir)
    try:
        result = subprocess.run([exe_path], capture_output=True, text=True)
    finally:
        os.chdir(orig_cwd)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    lines = result.stdout.splitlines()
    for l in lines:
        if l and not l.startswith('Stribog-512') and len(l.strip()) == 128:
            return l.strip()
    raise ValueError('Hash not found in output') 