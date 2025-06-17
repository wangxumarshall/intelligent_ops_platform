import unittest
import os
import shutil
from datetime import datetime
# Assuming litewebserver.py is in the same directory or accessible via PYTHONPATH
from litewebserver import parse_click_logs

class TestClickLogParser(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test logs
        self.test_log_dir_base = os.path.join(os.path.dirname(__file__), "test_logs_temp")
        self.test_log_dir = os.path.join(self.test_log_dir_base, "click") # Mimic structure
        os.makedirs(self.test_log_dir, exist_ok=True)

    def tearDown(self):
        # Remove the temporary directory after tests
        if os.path.exists(self.test_log_dir_base):
            shutil.rmtree(self.test_log_dir_base)

    def _write_log_file(self, filename, lines):
        """Helper to write lines to a log file in the test log directory."""
        filepath = os.path.join(self.test_log_dir, filename)
        with open(filepath, 'w') as f:
            for line in lines:
                f.write(line + "\n")

    def test_empty_log_directory(self):
        """Test parsing when the log directory is empty."""
        # Test with empty directory
        stats = parse_click_logs(log_dir_path=self.test_log_dir)
        self.assertEqual(stats, {})

        # Test with non-existent directory (by removing it temporarily)
        shutil.rmtree(self.test_log_dir_base)
        stats_non_existent = parse_click_logs(log_dir_path=self.test_log_dir)
        self.assertEqual(stats_non_existent, {})
        # Recreate for other tests if needed, though tearDown should handle cleanup
        os.makedirs(self.test_log_dir, exist_ok=True)


    def test_single_log_file(self):
        """Test parsing a single log file with valid entries."""
        log_lines = [
            "2023-10-01 - IP: 192.168.1.1 - Link: /link1 - Card: Card A",
            "2023-10-01 - IP: 192.168.1.2 - Link: /link2 - Card: Card B",
            "2023-10-01 - IP: 192.168.1.3 - Link: /link1 - Card: Card A", # Another for Card A
        ]
        self._write_log_file("2023-10-01.log", log_lines)

        stats = parse_click_logs(log_dir_path=self.test_log_dir)

        expected_stats = {
            "2023-10, Card A": 2,
            "2023-10, Card B": 1,
        }
        self.assertEqual(stats, expected_stats)

    def test_multiple_log_files(self):
        """Test aggregation across multiple log files from different dates/months."""
        log_lines_oct = [
            "2023-10-15 - IP: 10.0.0.1 - Link: /pageA - Card: Analytics Dashboard",
            "2023-10-16 - IP: 10.0.0.2 - Link: /pageB - Card: User Profile",
        ]
        self._write_log_file("2023-10-15.log", log_lines_oct) # File name date doesn't drive logic

        log_lines_nov = [
            "2023-11-01 - IP: 10.0.0.3 - Link: /pageA - Card: Analytics Dashboard",
            "2023-11-01 - IP: 10.0.0.4 - Link: /pageA - Card: Analytics Dashboard", # 2nd for Nov
            "2023-11-02 - IP: 10.0.0.5 - Link: /pageC - Card: Settings Page",
        ]
        self._write_log_file("2023-11-01.log", log_lines_nov)

        stats = parse_click_logs(log_dir_path=self.test_log_dir)

        expected_stats = {
            "2023-10, Analytics Dashboard": 1,
            "2023-10, User Profile": 1,
            "2023-11, Analytics Dashboard": 2,
            "2023-11, Settings Page": 1,
        }
        self.assertEqual(stats, expected_stats)

    def test_malformed_log_entries(self):
        """Test that malformed lines are skipped and valid lines are parsed."""
        log_lines = [
            "2023-12-01 - IP: 1.1.1.1 - Link: /good1 - Card: Valid Card 1",
            "This is a completely malformed line", # Malformed
            "2023-12-01 - IP: 2.2.2.2 - Link: /good2 - Card: Valid Card 2",
            "2023-12-01IP: 3.3.3.3 - Link: /badformat - Card: Bad Format Card", # Malformed date/separator
            "2023-12-02 - IP: 4.4.4.4 - Link: /good3", # Missing Card part
            "2023-12-03 - IP: 5.5.5.5 - Link: /good4 - Card: Valid Card 1", # Another for Valid Card 1
            "InvalidDate - IP: 6.6.6.6 - Link: /good5 - Card: Card With Bad Date", # Invalid date
        ]
        self._write_log_file("malformed.log", log_lines)

        # We can also capture stdout to check for print statements if desired,
        # but for now, we'll just check the output.
        # For more advanced testing, you might mock `print`.

        stats = parse_click_logs(log_dir_path=self.test_log_dir)

        expected_stats = {
            "2023-12, Valid Card 1": 2,
            "2023-12, Valid Card 2": 1,
        }
        self.assertEqual(stats, expected_stats)

    def test_log_file_with_mixed_dates_and_cards(self):
        """Test a single file with entries for multiple cards and different months."""
        log_lines = [
            "2024-01-10 - IP: 1.2.3.4 - Link: /feat1 - Card: Feature Alpha",
            "2024-01-15 - IP: 1.2.3.5 - Link: /feat2 - Card: Feature Beta",
            "2024-01-20 - IP: 1.2.3.6 - Link: /feat1 - Card: Feature Alpha", # Alpha again
            "2024-02-05 - IP: 1.2.3.7 - Link: /feat1 - Card: Feature Alpha", # Alpha in Feb
            "2024-02-10 - IP: 1.2.3.8 - Link: /feat3 - Card: Feature Gamma",
            "2024-01-25 - IP: 1.2.3.9 - Link: /feat2 - Card: Feature Beta", # Beta again in Jan
        ]
        self._write_log_file("mixed_log.log", log_lines)

        stats = parse_click_logs(log_dir_path=self.test_log_dir)

        expected_stats = {
            "2024-01, Feature Alpha": 2,
            "2024-01, Feature Beta": 2,
            "2024-02, Feature Alpha": 1,
            "2024-02, Feature Gamma": 1,
        }
        self.assertEqual(stats, expected_stats)

    def test_log_files_not_ending_with_log(self):
        """Ensure files not ending with .log are ignored."""
        log_lines = [
            "2023-10-01 - IP: 192.168.1.1 - Link: /link1 - Card: Card A",
        ]
        self._write_log_file("2023-10-01.txt", log_lines) # Note .txt extension
        self._write_log_file("backup.log.old", log_lines) # Note .old extension

        stats = parse_click_logs(log_dir_path=self.test_log_dir)
        self.assertEqual(stats, {})

if __name__ == '__main__':
    unittest.main()
