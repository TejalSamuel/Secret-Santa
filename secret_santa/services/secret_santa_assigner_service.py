import pandas as pd
import random
from derangement_service import FisherYatesDerangement

class SecretSantaAssigner:
    def __init__(self, employees_df, previous_df, logger):
        """
        Initializes the Secret Santa Assigner with employee and previous assignment data.

        :param employees_df: DataFrame with columns ["Employee_EmailID", "Employee_Name"]
        :param previous_df: DataFrame with columns ["Employee_EmailID", "Secret_Child_EmailID"]
        :param logger: Logger instance for logging events
        """
        self.logger = logger
        self.logger.info("SecretSantaAssigner initialized.")

        self.employees_df = employees_df
        self.previous_df = previous_df
        self.employees = employees_df["Employee_EmailID"].tolist()
        self.previous_assignments = None

        # Convert previous assignments to a dictionary for quick lookup
        if not self.previous_df.empty:
            self.previous_assignments = dict(zip(previous_df["Employee_EmailID"], previous_df["Secret_Child_EmailID"]))
            self.logger.info("Previous assignments loaded successfully.")
        else:
            self.logger.warning("No previous assignments found. Assignments will be generated from scratch.")

        self.derangement_service = FisherYatesDerangement(self.employees, self.previous_assignments, self.logger )
        

    def fisher_yates_derangement(self):
        """Generates a Fisher-Yates derangement ensuring:
        - No self-assignment
        - No repeat from previous year"""
        self.logger.info("Generating Fisher-Yates derangement...")
        
        n = len(self.employees)
        indices = list(range(n))

        for i in range(n - 1, 0, -1):
            j = random.randint(0, i - (i == indices[i]))
            indices[i], indices[j] = indices[j], indices[i]
        
        if self.previous_assignments:
            # Ensure previous assignment rules
            if any(self.previous_assignments.get(self.employees[i]) == self.employees[indices[i]] for i in range(n)):
                self.logger.warning("Previous assignment conflict detected. Retrying derangement...")
                return self.fisher_yates_derangement()  # Retry if previous match exists
        
        self.logger.info("Valid derangement generated successfully.")
        return indices

    def assign_secret_santa(self):
        """
        Assigns Secret Santa while ensuring:
        - No self-assignment
        - No repeat from previous assignments
        - Unique recipient for each participant

        :return: Dictionary {giver_email: recipient_email}
        """
        self.logger.info("Starting Secret Santa assignment...")
        
        if not self.employees:
            self.logger.error("No employees found. Cannot proceed with assignment.")
            return {}
        
        derangement = self.derangement_service.generate()
        assignments = {self.employees[i]: self.employees[derangement[i]] for i in range(len(self.employees))}
        
        self.logger.info("Secret Santa assignments completed successfully.")
        return assignments

    @staticmethod
    def map_names_to_emails(assignments_dict, employees_df):
        """
        Maps employee names to emails in the final assignment.

        :param assignments_dict: Dictionary {giver_email: recipient_email}
        :param employees_df: DataFrame with ["Employee_EmailID", "Employee_Name"]
        :return: DataFrame with ["Employee_Name", "Employee_EmailID", "Secret_Child_Name", "Secret_Child_EmailID"]
        """
        assignments_df = pd.DataFrame(assignments_dict.items(), columns=["Employee_EmailID", "Secret_Child_EmailID"])
        employees_df = employees_df.set_index("Employee_EmailID")
        
        assignments_df["Employee_Name"] = assignments_df["Employee_EmailID"].map(employees_df["Employee_Name"])
        assignments_df["Secret_Child_Name"] = assignments_df["Secret_Child_EmailID"].map(employees_df["Employee_Name"])
        
        return assignments_df[["Employee_Name", "Employee_EmailID", "Secret_Child_Name", "Secret_Child_EmailID"]]

