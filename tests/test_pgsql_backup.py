import json
import subprocess
from unittest.mock import patch, mock_open, MagicMock
import pytest
from pgsql_backup import DatabaseBackup
import subprocess


def test_load_config_valid(mock_logger, db_config):
    db_config_json = json.dumps(db_config)
    with patch("builtins.open", mock_open(read_data=db_config_json)):
        db_backup = DatabaseBackup(mock_logger, config_file="valid_config.json")
        assert db_backup.load_config() == db_config

def test_validate_config_invalid(mock_logger):
    db_backup = DatabaseBackup(mock_logger)
    invalid_config = [{"name": "db_name1"}]  # Simulating missing required keys
    assert not db_backup.validate_config(invalid_config)

@patch("builtins.open", mock_open(read_data="invalid json"))
def test_load_config_invalid_json(mock_logger):
    db_backup = DatabaseBackup(mock_logger, config_file="invalid_config.json")
    with patch.object(db_backup.logger, "log") as mock_log:
        assert db_backup.load_config() is None
        mock_log.assert_called_with("JSON decode error in config file: Expecting value: line 1 column 1 (char 0)", tag="ERROR")


@patch("os.path.exists", return_value=False)
@patch("os.makedirs")
def test_create_backup_dir(mock_makedirs, mock_exists, mock_logger):
    db_backup = DatabaseBackup(mock_logger)
    with patch.object(mock_logger, "get_timestamp", return_value="2023-03-04 12:00:00"):
        expected_path = "database_backup/Project1/20230304"
        assert db_backup.create_backup_dir("Project1") == expected_path
        mock_makedirs.assert_called_once_with(expected_path)

@patch("subprocess.run")
def test_dump_database_success(mock_subprocess, mock_logger, db_config):
    db_backup = DatabaseBackup(mock_logger)
    db_backup.create_backup_dir = MagicMock(return_value="/dummy/path/Project1/20230304")
    db_backup.dump_database(db_config[0])
    mock_subprocess.assert_called_once()
    mock_logger.log.assert_called_with("Backup successful for project: Project1, database: db_name1", tag="SUCCESS")

@patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, 'cmd', stderr="mock error"))
def test_dump_database_failure(mock_subprocess, mock_logger, db_config):
    db_backup = DatabaseBackup(mock_logger)
    db_backup.create_backup_dir = MagicMock(return_value="/dummy/path/Project1/20230304")
    success = db_backup.dump_database(db_config[0])
    assert not success
    mock_subprocess.assert_called_once()
    mock_logger.log.assert_called_with("Backup failed for project: Project1, database: db_name1. Error: mock error", tag="ERROR")


# Ensures db_config is passed as a parameter if it's a fixture
@patch("pgsql_backup.DatabaseBackup.load_config")
@patch("pgsql_backup.DatabaseBackup.dump_database")
def test_backup_databases_all_success(mock_dump_database, mock_load_config, mock_logger, db_config):
    mock_load_config.return_value = db_config
    mock_dump_database.return_value = True
    db_backup = DatabaseBackup(mock_logger)
    success = db_backup.backup_databases()
    assert success is True
    # Validate that dump_database is called with the correct configuration
    mock_dump_database.assert_called_with(db_config[0])


@patch("pgsql_backup.DatabaseBackup.load_config")
@patch("pgsql_backup.DatabaseBackup.dump_database", return_value=False)  # Simulate a failure directly
def test_backup_databases_failure(mock_dump_database, mock_load_config, mock_logger, db_config):
    mock_load_config.return_value = db_config
    db_backup = DatabaseBackup(mock_logger)
    success = db_backup.backup_databases()
    assert not success, "Expected backup_databases to return False on dump_database failure"
    mock_dump_database.assert_called()  # Ensures dump_database was called, implying a backup attempt was made
