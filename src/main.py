# 3rd party imports
from datetime import datetime
import time
from icecream import ic

# local imports
import import_env
from intro import get_intro
from logger import Logger
from pgsql_backup import DatabaseBackup
import read_version
from uptime_kuma import push_health_check

# import environment variables
DOCKER_REPO = import_env.get_env_variable("DOCKER_REPO")
GITHUB_README = import_env.get_env_variable("GITHUB_README")
UPTIME_KUMA_URL = import_env.get_env_variable("UPTIME_KUMA_URL")
UPTIME_KUMA_URL_CHECK = import_env.get_env_variable("UPTIME_KUMA_URL_CHECK")
JSON_DB_CONFIG_FILE = import_env.get_env_variable("JSON_DB_CONFIG_FILE")
BASE_BACKUP_DIR_HOST_FOLDER = import_env.get_env_variable("BASE_BACKUP_DIR_HOST_FOLDER")
LOG_FILE = import_env.get_env_variable("LOG_FILE")
MAIN_LOOP_TIME = import_env.get_env_variable("MAIN_LOOP_TIME")

# get current version
CURRENT_VERSION = read_version.get_version()


def main():
    print(get_intro(DOCKER_REPO, CURRENT_VERSION, GITHUB_README, UPTIME_KUMA_URL, UPTIME_KUMA_URL_CHECK))
    ic("Starting log instance")
    logger = Logger(LOG_FILE)
    ic("Starting DatabaseBackup instance")
    db_backup = DatabaseBackup(logger, JSON_DB_CONFIG_FILE, BASE_BACKUP_DIR_HOST_FOLDER)
    ic("Starting main loop that will create dayly backups of the databases.")
    while True:
        ic("Running DatabaseBackup")
        db_backup.run()
        ic("Pushing health check to uptime-kuma")
        push_health_check(UPTIME_KUMA_URL)
        ic("Sleeping for MAIN_LOOP_TIME")
        time.sleep(int(MAIN_LOOP_TIME))


if __name__ == '__main__':
    main()
