import pandas as pd
from services.config_service import ConfigService
from services.csv_service import CSVService
from services.secret_santa_assigner_service import SecretSantaAssigner
from services.logger import LoggerService
import os 


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class SecretSantaManager:
    def __init__(self):
        """Initialize the 
        Secret Santa Manager 
        with configurations 
        and services."""
        self.config_service = ConfigService.get_instance()
        self.logger_service = LoggerService()
        self.logger = self.logger_service.get_logger("SecretSantaManager")
        self.csv_service = CSVService(logger=self.logger)
        
        # Load file paths from config
        self.EMPLOYEE_CSV_PATH = self.get_abs_path(self.config_service.get_value("PATHS", "EMPLOYEE_CSV_PATH"))
        self.PREVIOUS_CSV_PATH = self.get_abs_path(self.config_service.get_value("PATHS", "PREVIOUS_ASSIGNMENTS_CSV_PATH"))
        self.OUTPUT_CSV_PATH = self.get_abs_path(self.config_service.get_value("PATHS", "OUTPUT_CSV_PATH"))


    def get_abs_path(self,relative_path):
        """Convert a relative path from config.ini to an absolute path based on the project root."""
        return os.path.abspath(os.path.join(BASE_DIR, relative_path))



    def load_data(self):
        """Load employee and previous 
        assignment data from CSV files."""
        self.logger.info("Loading input CSV files...")
        #Read employee data and previous year's secret santa data from csv
        self.employees_df = self.csv_service.read_csv(file_path=self.EMPLOYEE_CSV_PATH)
        self.previous_df = self.csv_service.read_csv(file_path=self.PREVIOUS_CSV_PATH)

        if self.employees_df is None:
            self.logger.error("Missing required input files. Exiting program.")
            exit(1)
        if self.previous_df is None:
            self.logger.info("Missing required input files. Going ahead without considering previous assignments.")
            self.previous_df = pd.DataFrame(columns=["Employee_Name","Employee_EmailID" ,"Secret_Child_Name", "Secret_Child_EmailID"])

        self.validate_data()

    def validate_data(self):
        """Validate required columns 
        in input CSV files."""
        self.logger.info("Validating input CSV files...")

        required_columns = {"Employee_Name", "Employee_EmailID"}
        if not required_columns.issubset(self.employees_df.columns):
            self.logger.error(f"Missing required columns in {self.EMPLOYEE_CSV_PATH}. Expected: {required_columns}")
            exit(1)
        if not self.previous_df.empty:
            if "Employee_Name" not in self.previous_df.columns or "Employee_EmailID" not in self.previous_df.columns or "Secret_Child_Name" not in self.previous_df.columns:
                self.logger.error(f"Missing required columns in {self.PREVIOUS_CSV_PATH}. Expected: [Employee_Name,Employee_EmailID ,Secret_Child_Name, Secret_Child_EmailID]")
        
    def assign_secret_santa(self):
        """Assign Secret Santa 
        and save results to a CSV file."""

        self.assigner_service = SecretSantaAssigner(employees_df=self.employees_df, previous_df=self.previous_df, logger=self.logger)
        assignments = self.assigner_service.assign_secret_santa()

        if not assignments:
            self.logger.error("Failed to generate valid Secret Santa assignments.")
            exit(1)

        assignments_df = SecretSantaAssigner.map_names_to_emails(assignments, self.employees_df)
        assignments_df.to_csv(self.OUTPUT_CSV_PATH, index=False, encoding="utf-8")
        self.logger.info(f"Secret Santa assignments saved to {self.OUTPUT_CSV_PATH}")

    def run(self):
        """Execute the 
        full Secret Santa process."""
        self.load_data()
        self.assign_secret_santa()


