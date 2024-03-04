import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_logger(mocker):
    mock_logger = mocker.MagicMock()
    mock_logger.log = mocker.MagicMock()
    return mock_logger

@pytest.fixture
def db_config():
    return [
        {
            "project_name": "Project1",
            "name": "db_name1",
            "host": "localhost",
            "port": "5432",
            "user": "user1",
            "password": "password1"
        }
    ]
