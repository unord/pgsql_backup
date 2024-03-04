

def get_version(filename='version.txt') -> str:
    try:
        # Read the existing version
        with open(filename, 'r') as file:
            version_text = file.read().strip()
        version = float(version_text)

        # Update the version
        new_version = version + 0.01

        return str(new_version)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
    except ValueError:
        print(f"Invalid content in {filename}. Expected a float.")
        return None
