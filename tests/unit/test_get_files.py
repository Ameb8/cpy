import unittest
from unittest.mock import patch, MagicMock
from cpy.get_files import read_files, evaluate_path, INVALID_PATH_ERR
from pathlib import Path

PATCH_PATH = "cpy.get_files.Path"

class TestReadFiles(unittest.TestCase):

    @patch("cpy.get_files.glob.glob")
    @patch("cpy.get_files.Path")
    def test_read_files_with_star_pattern(self, mock_path_cls, mock_glob):
        mock_glob.return_value = ["file1.py", "file2.py"]

        mock_path_instances = []
        for filename in mock_glob.return_value:
            mock_path = MagicMock(spec=Path)
            mock_path.is_file.return_value = True
            mock_path.read_text.return_value = f"content of {filename}"
            mock_path.__str__.return_value = filename
            mock_path_instances.append(mock_path)

        # Side effect to return mock path for each file name
        mock_path_cls.side_effect = lambda f: dict(zip(mock_glob.return_value, mock_path_instances))[f]

        file_map, errors = read_files("*.py")

        self.assertEqual(len(file_map), 2)
        self.assertIn("file1.py", file_map)
        self.assertEqual(errors, [])

    @patch("cpy.get_files.glob.glob")
    @patch("cpy.get_files.Path")
    def test_read_files_with_double_star_pattern(self, mock_path_cls, mock_glob):
        mock_glob.return_value = ["dir1/file1.py", "dir2/sub/file2.py"]

        mock_path_instances = []
        for filename in mock_glob.return_value:
            mock_path = MagicMock(spec=Path)
            mock_path.is_file.return_value = True
            mock_path.read_text.return_value = f"recursive content of {filename}"
            mock_path.__str__.return_value = filename
            mock_path_instances.append(mock_path)

        mock_path_cls.side_effect = lambda f: dict(zip(mock_glob.return_value, mock_path_instances))[f]

        file_map, errors = read_files("**/*.py")

        self.assertEqual(len(file_map), 2)
        self.assertIn("dir1/file1.py", file_map)
        self.assertIn("dir2/sub/file2.py", file_map)
        self.assertEqual(errors, [])

    @patch("cpy.get_files.glob.glob")
    @patch("cpy.get_files.Path")
    def test_mixed_file_types(self, mock_path_cls, mock_glob):
        mock_glob.return_value = ["file1.py", "file2.txt"]

        mock_path_instances = []
        for filename in mock_glob.return_value:
            mock_path = MagicMock(spec=Path)
            mock_path.is_file.return_value = True
            mock_path.read_text.return_value = f"content of {filename}"
            mock_path.__str__.return_value = filename
            mock_path_instances.append(mock_path)

        mock_path_cls.side_effect = lambda f: dict(zip(mock_glob.return_value, mock_path_instances))[f]

        file_map, errors = read_files("*.*")

        self.assertEqual(len(file_map), 2)
        self.assertIn("file1.py", file_map)
        self.assertIn("file2.txt", file_map)
        self.assertEqual(errors, [])

    @patch("cpy.get_files.glob.glob")
    @patch("cpy.get_files.Path")
    def test_ignore_directories(self, mock_path_cls, mock_glob):
        mock_glob.return_value = ["dir/", "file.py"]

        dir_mock = MagicMock(spec=Path)
        dir_mock.is_file.return_value = False

        file_mock = MagicMock(spec=Path)
        file_mock.is_file.return_value = True
        file_mock.read_text.return_value = "file content"
        file_mock.__str__.return_value = "file.py"

        mock_path_cls.side_effect = lambda f: {
            "dir/": dir_mock,
            "file.py": file_mock
        }[f]

        file_map, errors = read_files("*")

        self.assertEqual(file_map, {"file.py": "file content"})
        self.assertEqual(errors, [])

    @patch("cpy.get_files.glob.glob")
    @patch("cpy.get_files.Path")
    def test_unicode_decode_error(self, mock_path_cls, mock_glob):
        mock_glob.return_value = ["file_bad.txt"]

        mock_path = MagicMock(spec=Path)
        mock_path.is_file.return_value = True
        mock_path.read_text.side_effect = UnicodeDecodeError("utf-8", b"", 0, 1, "invalid start byte")
        mock_path.__str__.return_value = "file_bad.txt"

        mock_path_cls.return_value = mock_path

        file_map, errors = read_files("file_bad.txt")

        self.assertEqual(file_map, {})
        self.assertEqual(len(errors), 1)
        self.assertIn("file_bad.txt", errors[0][0])
        self.assertIsInstance(errors[0][1], UnicodeDecodeError)

    @patch("cpy.get_files.glob.glob")
    @patch("cpy.get_files.Path")
    def test_no_matching_files(self, mock_path_cls, mock_glob):
        mock_glob.return_value = []
        mock_path_cls.return_value = MagicMock()  # not actually used

        file_map, errors = read_files("*.md")

        self.assertEqual(file_map, {})
        self.assertEqual(errors, [])

    @patch("cpy.get_files.glob.glob")
    @patch("cpy.get_files.Path")
    def test_exact_max_files_hit(self, mock_path_cls, mock_glob):
        mock_glob.return_value = [f"file{i}.txt" for i in range(3)]
        mock_path_instances = []

        for name in mock_glob.return_value:
            mock_path = MagicMock(spec=Path)
            mock_path.is_file.return_value = True
            mock_path.read_text.return_value = f"content of {name}"
            mock_path.__str__.return_value = name
            mock_path_instances.append(mock_path)

        mock_path_cls.side_effect = lambda f: dict(zip(mock_glob.return_value, mock_path_instances))[f]

        file_map, errors = read_files("*.txt", max_files=3)

        self.assertEqual(len(file_map), 3)
        self.assertEqual(errors, [])

    @patch("cpy.get_files.glob.glob")
    @patch("cpy.get_files.Path")
    def test_file_read_oserror(self, mock_path_cls, mock_glob):
        mock_glob.return_value = ["badfile.txt"]

        mock_path = MagicMock(spec=Path)
        mock_path.is_file.return_value = True
        mock_path.read_text.side_effect = OSError("disk failure")
        mock_path.__str__.return_value = "badfile.txt"

        mock_path_cls.return_value = mock_path

        file_map, errors = read_files("badfile.txt")

        self.assertEqual(file_map, {})
        self.assertEqual(len(errors), 1)
        self.assertIn("badfile.txt", errors[0][0])
        self.assertIsInstance(errors[0][1], OSError)

class TestEvaluatePath(unittest.TestCase):
    def test_evaluate_path_invalid_input(self):
        result, error = evaluate_path("   --split:  ")
        self.assertIsNone(result)
        self.assertEqual(error, INVALID_PATH_ERR)

    @patch(PATCH_PATH)
    def test_evaluate_path_valid_file_no_delimiter(self, mock_read_files):
        mock_read_files.return_value = ({"file.txt": "hello"}, [])

        result, error = evaluate_path("file.txt")
        
        self.assertEqual(result, "hello")
        self.assertIsNone(error)

    @patch("cpy.get_files.resolve_command")
    @patch(PATCH_PATH)
    def test_evaluate_path_valid_with_split(self, mock_read_files, mock_resolve_command):
        mock_read_files.return_value = ({"file.txt": "a", "file2.txt": "b"}, [])
        mock_resolve_command.return_value = ("::", None)

        result, error = evaluate_path("file*.txt --split: custom_delim")

        self.assertEqual(result, "a::b")
        self.assertIsNone(error)
        mock_resolve_command.assert_called_with("custom_delim")

    @patch(PATCH_PATH)
    def test_evaluate_path_read_files_errors(self, mock_read_files):
        mock_read_files.return_value = ({}, [("file.txt", OSError("oops"))])

        result, error = evaluate_path("file.txt")
        
        self.assertIsNone(result)
        self.assertIn("file.txt", error)
        self.assertIn("oops", error)

    @patch(PATCH_PATH)
    def test_evaluate_path_no_files(self, mock_read_files):
        mock_read_files.return_value = ({}, [])

        result, error = evaluate_path("nofile.txt")
        
        self.assertIsNone(result)
        self.assertEqual(error, INVALID_PATH_ERR)


    if __name__ == "__main__":
        unittest.main()


