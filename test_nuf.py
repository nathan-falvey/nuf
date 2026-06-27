import sys
import unittest

# Ensure the src directory is in the path
sys.path.insert(0, 'src')

import nuf

class TestNUF(unittest.TestCase):
    def test_core(self):
        self.assertEqual(nuf.core.core_func(), "Hello from core")

    def test_file_utils(self):
        self.assertEqual(nuf.file_utils.file_func(), "Hello from file_utils")
        # Test existence check
        self.assertTrue(nuf.file_utils.check_file_exists("pyproject.toml"))
        self.assertFalse(nuf.file_utils.check_file_exists("nonexistent_file.txt"))
        self.assertTrue(nuf.file_utils.check_dir_exists("src"))
        self.assertFalse(nuf.file_utils.check_dir_exists("nonexistent_dir"))
        self.assertGreater(nuf.file_utils.get_file_size("pyproject.toml"), 0)

        # Test PathNotFoundError
        with self.assertRaises(nuf.file_utils.PathNotFoundError):
            nuf.file_utils.get_file_size("nonexistent_file_test.txt")

        # Test file/directory creation and write operations
        test_dir = "test_temp_dir"
        test_file = f"{test_dir}/temp_test_file.txt"

        # Create dir
        self.assertTrue(nuf.file_utils.create_dir(test_dir))
        
        # Create file
        self.assertTrue(nuf.file_utils.create_file(test_file))
        
        # Write lines
        self.assertTrue(nuf.file_utils.write_line_to_file(test_file, "Line 1"))
        self.assertTrue(nuf.file_utils.write_line_to_file(test_file, "Line 2"))

        # Read lines
        lines = nuf.file_utils.return_lines_from_file(test_file)
        self.assertEqual(lines, ["Line 1\n", "Line 2\n"])

        # Test non-empty directory deletion failure
        with self.assertRaises(nuf.file_utils.DirectoryNotEmptyError):
            nuf.file_utils.delete_dir(test_dir, recursive=False)

        # Clean up recursively
        self.assertTrue(nuf.file_utils.delete_dir(test_dir, recursive=True))
        
        # Verify cleaned up
        self.assertFalse(nuf.file_utils.check_dir_exists(test_dir))

    def test_message_utils(self):
        self.assertEqual(nuf.message_utils.message_func(), "Hello from message_utils")
        # Verify colorama message formatting functions run successfully
        nuf.message_utils.print_success("Success message")
        nuf.message_utils.print_error("Error message")
        nuf.message_utils.print_warning("Warning message")

    def test_format_utils(self):
        self.assertEqual(nuf.format_utils.format_func(), "Hello from format_utils")
        # Test bytes formatting
        self.assertEqual(nuf.format_utils.format_bytes(0), "0 B")
        self.assertEqual(nuf.format_utils.format_bytes(512), "512.00 B")
        self.assertEqual(nuf.format_utils.format_bytes(1024), "1.00 KB")
        self.assertEqual(nuf.format_utils.format_bytes(1048576), "1.00 MB")
        self.assertEqual(nuf.format_utils.format_bytes(1073741824, decimal_places=1), "1.0 GB")
        with self.assertRaises(ValueError):
            nuf.format_utils.format_bytes(-1)

if __name__ == '__main__':
    unittest.main()
