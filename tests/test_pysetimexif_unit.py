import os
import unittest
import unittest.mock as mock

from pysetimexif import pysetimexif


class PysetimexifUnitTests(unittest.TestCase):
    data_path = os.path.join(os.path.dirname(__file__), "data")
    test_data_file = os.path.join(data_path, "20250109_121037.jpg")
    test_data_time_seconds = 1736421037  # Thu Jan 09 2025 11:10:37 GMT+0000
    test_data_time_string = "2025:01:09 12:10:37"
    test_data_time_offset = "+01:00"
    test_data_no_exif_file = os.path.join(data_path, "no-exif-data.jpg")

    def setUp(self):
        """Set and validate that 'test_data_file' has a 'modified timestamp' of 1970-01-01"""
        self.assertTrue(os.path.exists(self.test_data_file))
        os.utime(self.test_data_file, times=(0, 0))
        modification_time = os.path.getmtime(self.test_data_file)
        self.assertEqual(modification_time, 0.0)

    def test_set_utime(self):
        """Check that the files 'modified timestamp' is set as expected"""
        pysetimexif.set_utime(self.test_data_file)
        modification_time = os.path.getmtime(self.test_data_file)
        self.assertEqual(modification_time, self.test_data_time_seconds)

    def test_read_exif_time_tags(self):
        """Check that expected timestamp and offset strings are returned"""
        timestamp, offset = pysetimexif.read_exif_time_tags(self.test_data_file)
        self.assertEqual(timestamp, self.test_data_time_string)
        self.assertEqual(offset, self.test_data_time_offset)

    @mock.patch("builtins.open", mock.mock_open(read_data=""))
    def test_read_exif_time_tags_no_exif_data_error(self):
        """Check that NoExifDataError exception is raised when accessing file without exif data block"""
        self.assertRaises(
            pysetimexif.NoExifDataError,
            pysetimexif.read_exif_time_tags,
            "file_without_exif.jpg",
        )

    def test_datetime_from_exif_datetime(self):
        """Check timestamp returned by datetime_from_exif_datetime"""
        dt = pysetimexif.datetime_from_exif_datetime(
            self.test_data_time_string, self.test_data_time_offset
        )
        self.assertEqual(dt.timestamp(), self.test_data_time_seconds)

    def test_datetime_from_exif_datetime_invalid(self):
        """Check that 'InvalidTimestampError' exception is raised when an invalid exif timestamp is encountered"""
        self.assertRaises(
            pysetimexif.InvalidTimestampError,
            pysetimexif.datetime_from_exif_datetime,
            "01.01.2000 12:34:56",
            "+00:00",
        )


if __name__ == "__main__":
    unittest.main()
