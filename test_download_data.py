""" test_download_data.py

Copyright 2025, Cornell University

Cornell University asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including online repositories
such as Github.

Sharing solutions with current or future students of ENMGT5400 is
prohibited and subject to being investigated as a Code of Academic Integrity violation.

-----do not edit anything above this line---
"""

import unittest
import re
from download_data import list_gdelt_files


class TestGDELTFiles(unittest.TestCase):

    def setUp(self):
        self.gdelt_files = list_gdelt_files(year=2024)

    def test_1(self):
        # Check there are 366 files for 2024 (Leap year!)
        self.assertEqual(
            len(self.gdelt_files),
            366,
            f"Expected 366 files, found {len(self.gdelt_files)}",
        )

    def test_2(self):
        # Check data types and content of a specific file
        expected_item = {
            "md5": "25a40689f2626584f6135e095e238a4e",
            "filesize": "8.1",
            "url": "http://data.gdeltproject.org/events/20240103.export.CSV.zip",
        }
        self.assertIn("20240103", self.gdelt_files, "20240103 file not found")
        actual_item = self.gdelt_files["20240103"]

        self.assertEqual(actual_item["md5"], expected_item["md5"], "Incorrect MD5 hash")
        self.assertEqual(
            actual_item["filesize"], expected_item["filesize"], "Incorrect file size"
        )
        self.assertEqual(actual_item["url"], expected_item["url"], "Incorrect URL")

    def test_3(self):
        # Check for correct data types
        for date, info in self.gdelt_files.items():
            # Dict key
            self.assertIsInstance(date, str, f"Date '{date}' is not a string")
            self.assertTrue(
                re.match(r"^\d{8}$", date), f"Date '{date}' is not in YYYYMMDD format"
            )
            # Dict value
            self.assertIsInstance(info, dict, f"Info for '{date}' is not a dictionary")

            # Filesize
            self.assertIsInstance(
                info["filesize"], str, f"Filesize for '{date}' is not a string"
            )

            # Hash
            self.assertIsInstance(info["md5"], str, f"MD5 for '{date}' is not a string")
            self.assertTrue(
                info["md5"].isalnum(), f"MD5 for '{date}' is not alphanumeric"
            )

            # URL
            self.assertIsInstance(info["url"], str, f"URL for '{date}' is not a string")


if __name__ == "__main__":
    unittest.main()
