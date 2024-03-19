import os
from collections import namedtuple
import argparse
import unittest

FileInfo = namedtuple('FileInfo', ['name', 'extension', 'is_directory', 'parent_directory'])

# Функция для получения информации о файлах в указанной директории
def get_file_info(path):
    files_info = []
    parent_dir = os.path.basename(os.path.abspath(path))
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        is_directory = os.path.isdir(item_path)
        if is_directory:
            name = item
            extension = ''
        else:
            name, extension = os.path.splitext(item)
        files_info.append(FileInfo(name, extension, is_directory, parent_dir))
    return files_info

# Определение класса для тестирования функции get_file_info
class TestFileInfo(unittest.TestCase):

    # Подготовка тестовой среды перед каждым тестом
    def setUp(self):
        self.test_dir = os.path.join(os.getcwd(), 'test_directory')
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'subdir'), exist_ok=True)
        open(os.path.join(self.test_dir, 'test_file.jpg'), 'w').close()
        open(os.path.join(self.test_dir, 'test_file.txt'), 'w').close()
        open(os.path.join(self.test_dir, 'test_file.docx'), 'w').close()

    # Тест проверяет наличие поддиректории 'subdir'
    def test_directory_existence(self):
        files_info = get_file_info(self.test_dir)
        directories = [file_info.name for file_info in files_info if file_info.is_directory]
        self.assertIn('subdir', directories)

    # Тест проверяет наличие файла с расширением '.jpg'
    def test_jpg_file_existence(self):
        files_info = get_file_info(self.test_dir)
        jpg_files = [file_info.name for file_info in files_info if not file_info.is_directory and file_info.extension == '.jpg']
        self.assertIn('test_file', jpg_files)

    # Тест проверяет наличие файла с расширением '.txt'
    def test_txt_file_existence(self):
        files_info = get_file_info(self.test_dir)
        txt_files = [file_info.name for file_info in files_info if not file_info.is_directory and file_info.extension == '.txt']
        self.assertIn('test_file', txt_files)

    # Тест проверяет наличие файла с расширением '.docx'
    def test_docx_file_existence(self):
        files_info = get_file_info(self.test_dir)
        docx_files = [file_info.name for file_info in files_info if not file_info.is_directory and file_info.extension == '.docx']
        self.assertIn('test_file', docx_files)

    # Тест проверяет общее количество файлов (не считая каталога) в директории
    def test_total_file_count(self):
        files_info = get_file_info(self.test_dir)
        files_count = sum(1 for file_info in files_info if not file_info.is_directory)
        self.assertEqual(files_count, 3)

    # Очистка тестовой среды после выполнения каждого теста
    def tearDown(self):
        os.remove(os.path.join(self.test_dir, 'test_file.jpg'))
        os.remove(os.path.join(self.test_dir, 'test_file.txt'))
        os.remove(os.path.join(self.test_dir, 'test_file.docx'))
        os.rmdir(os.path.join(self.test_dir, 'subdir'))
        os.rmdir(self.test_dir)

if __name__ == "__main__":
    # Создание парсера аргументов командной строки
    parser = argparse.ArgumentParser(description='Get file information')
    parser.add_argument('directory_path', type=str, help='Path to the directory')
    args = parser.parse_args()

    # Получение информации о файлах в указанной директории
    files_info = get_file_info(args.directory_path)
    for file_info in files_info:
        print(file_info)

    unittest.main(argv=[''], exit=False)