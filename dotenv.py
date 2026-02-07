import os

def load_dotenv(file_path: str = ".env"):
    """
    Load environment variables from a file.
    """
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ[key.strip()] = value.strip().strip('"').strip("'")