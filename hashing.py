"""
Модуль для вычисления хеша по ГОСТ 34.11-2012 и сравнения хешей.
"""

def gost_hash(file_like_or_path):
    """Вычисляет хеш файла по ГОСТ 34.11-2012. Принимает путь к файлу или file-like объект."""
    raise NotImplementedError

def compare_hashes(hash1, hash2):
    """Сравнивает два хеша, возвращает True/False."""
    raise NotImplementedError 