import os
import json
import subprocess
import re
from icecream import ic

class DatabaseBackup:
    def __init__(self, logger, config_file="db_config.json", base_backup_dir="database_backup"):
        self.config_file = config_file
        self.logger = logger
        self.base_backup_dir = base_backup_dir

    def clean_string(self, value):
        """Remove non-printable characters from a string."""
        # This regex matches all non-printable characters except whitespace chars
        cleaned_value = re.sub(r'[^\x20-\x7E]+', '', value)
        return cleaned_value, cleaned_value != value

    def ensure_utf8_no_bom(self):
        """Ensure file is UTF-8 without BOM and fix if needed."""
        try:
            with open(self.config_file, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            # Detect if BOM was present and removed by 'utf-8-sig'
            if content.startswith(u'\ufeff'):
                self.logger.log("UTF-8 BOM found and removed from the configuration file.", tag="WARNING")
            # Save the file without BOM in UTF-8 encoding
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            self.logger.log(f"Error processing config file for UTF-8 BOM: {e}", tag="ERROR")

    def validate_config(self, configs):
        dirty = False
        for config in configs:
            required_keys = ["project_name", "name", "host", "port", "user", "password"]
            for key in required_keys:
                if key not in config:
                    self.logger.log(f"Invalid configuration: Missing required key {key}", tag="ERROR")
                    return False
                if isinstance(config[key], str):
                    cleaned_value, is_dirty = self.clean_string(config[key])
                    config[key] = cleaned_value
                    dirty |= is_dirty
                    if is_dirty:
                        self.logger.log(f"Invisible characters removed from {key} in {config['project_name']}", tag="WARNING")
        if dirty:
            self.save_cleaned_config(configs)
        return True

    def save_cleaned_config(self, configs):
        """Save the cleaned config back to the file in a pretty format."""
        try:
            with open(self.config_file, "w", encoding='utf-8') as f:
                json.dump(configs, f, indent=4)
                self.logger.log("Configuration file has been cleaned and saved.", tag="INFO")
        except Exception as e:
            self.logger.log(f"Error saving cleaned config file: {e}", tag="ERROR")

    def load_config(self):
        self.ensure_utf8_no_bom()
        try:
            with open(self.config_file, "r", encoding='utf-8') as f:
                configs = json.load(f)
                if self.validate_config(configs):
                    return configs
                else:
                    self.logger.log("Configuration validation failed.", tag="ERROR")
        except json.JSONDecodeError as e:
            self.logger.log(f"JSON decode error in config file: {e}", tag="ERROR")
        except Exception as e:
            self.logger.log(f"Error loading config file: {e}", tag="ERROR")
        return None


    def create_backup_dir(self, project_name):
        # Format the date as 'YYYYMMDD'
        today_str = self.logger.get_timestamp().split(" ")[0].replace("-", "")
        # Construct the backup path using the base directory, project name, and date
        backup_path = os.path.join(self.base_backup_dir, project_name, today_str)
        ic("backup_path", backup_path)
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
            ic("Backup directory did not exist and therefore one was created")
            return backup_path
        return None

    def dump_database(self, db_config):
        backup_path = self.create_backup_dir(db_config["project_name"])
        ic("backup_path", backup_path)
        if backup_path:
            # Command to dump the database, ensuring the password is passed securely
            dump_command = f"pg_dump -h {db_config['host']} -p {db_config['port']} -U {db_config['user']} -F p -b -v -f \"{os.path.join(backup_path, db_config['name'] + '.sql')}\" {db_config['name']}"
            try:
                subprocess.run(dump_command, check=True, shell=True, text=True, capture_output=True, env={"PGPASSWORD": db_config['password']})
                ic("Dump command successful")
                ic("dump_command", dump_command)
                self.logger.log(f"Backup successful for project: {db_config['project_name']}, database: {db_config['name']}", tag="SUCCESS")
            except subprocess.CalledProcessError as e:
                self.logger.log(f"Backup failed for project: {db_config['project_name']}, database: {db_config['name']}. Error: {e.stderr.strip()}", tag="ERROR")
                ic("Dump command failed")
                ic("dump_command", dump_command)
                return False
            return True

    def backup_databases(self):
        ic("Getting database configurations")
        configs = self.load_config()
        ic("configs", configs)
        if not configs:
            ic("No configurations found")
            return False
        all_successful = True
        for db_config in configs:
            ic("Current db_config", db_config)
            if not self.dump_database(db_config):
                all_successful = False
        return all_successful

    def run(self):
        if self.backup_databases():
            self.logger.log("All database backups completed successfully.", tag="SUCCESS")



def main():
    pass


if __name__ == "__main__":
    main()
