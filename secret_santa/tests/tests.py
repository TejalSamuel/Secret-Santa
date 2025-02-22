import unittest
import pandas as pd
from services.secret_santa_assigner_service import SecretSantaAssigner  

class TestSecretSanta(unittest.TestCase):

    def setUp(self):
        # Employees DataFrame
        self.employees_df = pd.DataFrame({
            "Employee_Name": ["Alice", "Bob", "Charlie"],
            "Employee_EmailID": ["alice@example.com", "bob@example.com", "charlie@example.com"]
        })

        # Previous year assignments DataFrame
        self.previous_df = pd.DataFrame({
            "Employee_Name": ["Alice", "Bob", "Charlie"],
            "Employee_EmailID": ["alice@example.com", "bob@example.com", "charlie@example.com"],
            "Secret_Child_Name": ["Charlie", "Alice", "Bob"],
            "Secret_Child_EmailID": ["charlie@example.com", "alice@example.com", "bob@example.com"]
        })
        self.employees = self.employees_df["Employee_EmailID"].tolist()


    def test_unique_assignments(self):
        """Test that all Secret Santa assignments are unique (no duplicate recipients)."""
        assigner = SecretSantaAssigner(self.employees_df, self.previous_df)
        assignments = assigner.assign_secret_santa()

        if isinstance(assignments, pd.DataFrame):
            assignments = assignments.to_dict(orient="records")
        
        secret_children = [row for row in assignments]
        self.assertEqual(len(secret_children), len(set(secret_children)), "Duplicate assignments found!")

    def test_no_self_assignment(self):
        """Test that no employee is assigned to themselves."""
        assigner = SecretSantaAssigner(self.employees_df, self.previous_df)
        assignments = assigner.assign_secret_santa()

        if isinstance(assignments, pd.DataFrame):
            assignments = assignments.to_dict(orient="records")

        for giver, recipient in assignments.items():
            self.assertNotEqual(giver,recipient, f"{giver} was assigned to themselves!")

    def test_no_previous_year_assignment(self):
        """Test that no one gets the same Secret Santa as last year."""
        assigner = SecretSantaAssigner(self.employees_df, self.previous_df)
        assignments = assigner.assign_secret_santa()

        if isinstance(assignments, pd.DataFrame):
            assignments = assignments.to_dict(orient="records")

        prev_pairs = {
            (row["Employee_EmailID"], row["Secret_Child_EmailID"])
            for _, row in self.previous_df.iterrows()
        }

        for current_giver, current_recipient in assignments.items():
            self.assertNotIn(
                (current_giver,current_recipient),
                prev_pairs,
                f"{current_giver} was assigned the same person as last year!"
            )

    def test_empty_input(self):
        """Test that the function handles empty input without crashing."""
        empty_employees = pd.DataFrame(columns=["Employee_Name", "Employee_EmailID"])
        empty_previous_assignments = pd.DataFrame(columns=["Employee_Name", "Employee_EmailID", "Secret_Child_Name", "Secret_Child_EmailID"])

        assigner = SecretSantaAssigner(empty_employees, empty_previous_assignments)
        assignments = assigner.assign_secret_santa()

        self.assertEqual(len(assignments), 0, "Assignments should be empty when no employees are provided!")

if __name__ == "__main__":
    unittest.main()
