from logger import Logger
import datetime
from unittest.mock import mock_open, patch


# Ensures the proper patching of the datetime module used within Logger
@patch('logger.datetime')  # Adjust the patch location to 'your_module.datetime' if necessary
def test_log(mock_datetime):
    # Mock the current time to a fixed datetime
    mock_datetime.now.return_value = datetime.datetime(2023, 3, 4, 12, 0, 0)
    mock_datetime.datetime.now.return_value.strftime.return_value = "2023-03-04 12:00:00"

    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        logger = Logger("test_log.txt")
        logger.log("Test message", "DEBUG")
        mock_file().write.assert_called_once_with("2023-03-04 12:00:00 [DEBUG]: Test message\n")


def test_get_timestamp():
    # Mock the current time to a fixed datetime
    fixed_datetime = datetime.datetime(2023, 3, 4, 12, 0, 0)
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_datetime
        expected_timestamp = "2023-03-04 12:00:00"
        actual_timestamp = Logger.get_timestamp()
        assert actual_timestamp == expected_timestamp, "The timestamp format should match the expected format"
