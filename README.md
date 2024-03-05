# PostgreSQL Backup Tool

This tool automates the process of backing up PostgreSQL databases to a specified directory, logs the backup process, and integrates with Uptime Kuma for health checks. It's designed to run as a Docker container for easy deployment and scaling.

## Features

- Automatic backup of PostgreSQL databases based on a JSON configuration file.
- Logging of backup successes and failures.
- Health check integration with Uptime Kuma.
- Customizable backup directory, logging, and operational parameters through environment variables.

## Prerequisites

- Docker and Docker Compose
- Python 3.12 or later
- PostgreSQL client installed in the environment where the tool runs

## Repository Info and Configuration

1. **Github Repository**

   ```shell
   git clone https://github.com/unord/pgsql_backup.git
   cd pgsql_backup
   ```

2. **Docker Hub Repository**

   The Docker image for this tool is available on Docker Hub at `docker_repo_url`.


3. **Configuration**

   Set the necessary environment variables in either directly the OS or in a `.env` file in the project root. Required environment variables include:

   - `DOCKER_REPO`: Docker repository URL.
   - `GITHUB_README`: URL to the GitHub README.md file.
   - `UPTIME_KUMA_URL`: Uptime Kuma health check URL.
   - `UPTIME_KUMA_URL_CHECK`: Health check interval set in Uptime Kuma(Used for log info only).
   - `PROJECT_HOST_FOLDER`: Host folder path for the project.
   - `JSON_DB_CONFIG_FILE`: Path to the JSON configuration file for database backups.
   - `BASE_BACKUP_DIR_HOST_FOLDER`: Directory to store the backup files.
   - `LOG_FILE`: Log file path.
   - `MAIN_LOOP_TIME`: Main loop sleep time in seconds.

4. **Running the Tool**

   Start the Docker container using Docker Compose file or create your own Dockerfile.


## Usage

Once the container is running, it will automatically start backing up databases according to the schedule set by `MAIN_LOOP_TIME`. Backup logs can be found in the `LOG_FILE` specified.

## JSON Configuration Format

The tool expects a JSON configuration file specifying the databases to back up. The format is as follows:

```json
[
  {
    "project_name": "Project1",
    "name": "db_name1",
    "host": "localhost",
    "port": "5432",
    "user": "user1",
    "password": "password1"
  }
]
```
## Test Module

Two test modules are available in the `test` directory. The `test_pgsql_backup.py` module tests the database backup process functions with mock data, while the `test_logger.py` module tests the logging functions of the logger class with mock data.

## License

MIT License

Copyright (c) 2024 U/NORD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
