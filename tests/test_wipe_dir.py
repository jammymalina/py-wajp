import os
import shutil
import unittest

from wajp import wipe_directory


class TestWipeDirectory(unittest.TestCase):
    def setUp(self):
        self.test_dir_name = "test_wipe_dir"
        self.test_dir_path = os.path.join(os.getcwd(), self.test_dir_name)

        if os.path.exists(self.test_dir_path):
            shutil.rmtree(self.test_dir_path)

        os.makedirs(self.test_dir_path)

        self.file1_path = os.path.join(self.test_dir_path, "file1.txt")
        self.file2_path = os.path.join(self.test_dir_path, "file2.log")
        self.subdir1_path = os.path.join(self.test_dir_path, "subdir1")
        self.subdir2_path = os.path.join(self.test_dir_path, "subdir2")
        self.subfile1_path = os.path.join(self.subdir1_path, "subfile1.csv")

        with open(self.file1_path, "w") as f:
            f.write("content1")
        with open(self.file2_path, "w") as f:
            f.write("content2")

        os.makedirs(self.subdir1_path)
        with open(self.subfile1_path, "w") as f:
            f.write("subcontent1")

        os.makedirs(self.subdir2_path)  # Empty subdirectory

        print(f"\n[setUp] Created test directory: {self.test_dir_path}")
        print(f"[setUp] Initial contents: {os.listdir(self.test_dir_path)}")

    def tearDown(self):
        if os.path.exists(self.test_dir_path):
            shutil.rmtree(self.test_dir_path)
            print(f"[tearDown] Removed test directory: {self.test_dir_path}")

    def test_wipe_existing_directory_contents(self):
        """
        It should remove all files and subdirectories, but the main directory remains
        """
        # Assert initial state
        self.assertTrue(os.path.exists(self.file1_path))
        self.assertTrue(os.path.exists(self.subdir1_path))
        self.assertTrue(os.path.exists(self.test_dir_path))  # Main directory exists

        wipe_directory(self.test_dir_path)

        # Assert final state: main directory exists, but its contents are gone
        self.assertTrue(os.path.exists(self.test_dir_path))
        self.assertFalse(os.path.exists(self.file1_path))
        self.assertFalse(os.path.exists(self.file2_path))
        self.assertFalse(os.path.exists(self.subdir1_path))
        self.assertFalse(os.path.exists(self.subfile1_path))  # Check sub-sub-content
        self.assertFalse(os.path.exists(self.subdir2_path))

        # Check that the directory is empty
        self.assertEqual(len(os.listdir(self.test_dir_path)), 0)

    def test_wipe_non_existent_directory(self):
        """
        It should handle a non-existent directory gracefully and not raise an error
        """
        non_existent_dir = os.path.join(os.getcwd(), "non_existent_dir_12345")
        self.assertFalse(os.path.exists(non_existent_dir))

        # We expect no errors to be raised
        wipe_directory(non_existent_dir)

        # Assert that the directory still doesn't exist and nothing was created
        self.assertFalse(os.path.exists(non_existent_dir))

    def test_wipe_empty_directory(self):
        """
        It should not do anything when the directory is empty - no errors, remains empty
        """
        empty_dir_path = os.path.join(self.test_dir_path, "already_empty")
        os.makedirs(empty_dir_path)
        self.assertTrue(os.path.exists(empty_dir_path))
        self.assertEqual(len(os.listdir(empty_dir_path)), 0)

        wipe_directory(empty_dir_path)

        self.assertTrue(os.path.exists(empty_dir_path))
        self.assertEqual(len(os.listdir(empty_dir_path)), 0)
