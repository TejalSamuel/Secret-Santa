import pandas as pd

class CSVService:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("CSVService initialized.")

    def read_csv(self, file_path):
        """Read a CSV file into a Pandas DataFrame."""
        try:
            df = pd.read_csv(file_path)
            self.logger.info(f"Successfully read CSV: {file_path}")
            return df
        except FileNotFoundError:
            self.logger.error(f"File not found at: {file_path}")
            return None
        except Exception as e:
            self.logger.error(f"Error reading CSV {file_path}: {e}")
            return None

    def write_csv(self, df, file_path):
        try:
            df.to_csv(file_path, index=False)
            self.logger.info(f"Successfully wrote CSV: {file_path}")
        except Exception as e:
            self.logger.error(f"Error writing CSV {file_path}: {e}")

