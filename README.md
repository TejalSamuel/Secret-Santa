Secret Santa Assignment System

Overview
This project is a "Secret Santa Assignment System" that ensures employees are assigned a Secret Santa in a fair manner. 
The assignment follows these key rules:
- No self-assignment – an employee cannot be their own Secret Santa.
- No repeat assignments – an employee should not receive the same Secret Santa as in previous assignments.
- Random but fair allocation – each person is assigned someone else without bias.

Algorithm Choice
We use the Fisher-Yates Shuffle to generate a derangement, 
ensuring a fair and efficient shuffle of participants. The Fisher-Yates Shuffle is chosen because:
- It provides an O(n) complexity (optimal for large datasets).
- It ensures uniform randomness, avoiding biased results.
- It can be modified to avoid repeat assignments by checking against previous data.

Prerequisites
Python 3.10+
Virtual environment (recommended)
Required dependencies (listed in requirements.txt)

Setup Instructions
1. Clone the Repository
git clone https://github.com/your-repo/secret-santa.git
cd secret-santa

2. Create and Activate a Virtual Environment
python3 -m venv venv 
source venv/bin/activate  # Activate (Linux/Mac)
venv\Scripts\activate  # Activate (Windows)

3. Install Dependencies
pip install -r requirements.txt

4. Prepare Input Data
- employees.csv: Contains employee names and email IDs.
- previous_assignments.csv (optional): Tracks past assignments to avoid repeats.

Configuration Guide (config.properties)
The config.properties file allows you to specify paths for input/output CSV files and logging configurations. 

1.[PATHS] Section

- EMPLOYEE_CSV_PATH: Path to the CSV file containing employees' names and email addresses.
- PREVIOUS_ASSIGNMENTS_CSV_PATH: Path to the previous Secret Santa assignments file (if available).
- OUTPUT_CSV_PATH: Path where the new Secret Santa assignments will be saved.

2.[LOGGING] Section

- LOG_FILE_PATH: Directory where log files will be stored.
- LOG_FILE_NAME: Name of the log file.
- BACKUP_COUNT: Number of old log files to retain before rotating.

Running the Secret Santa Assignment

Run the assignment script:
                         python main.py

This will generate a new assignment and save it as the file name you specify in 'config.properties' in OUTPUT_CSV_PATH.

Running Unit Tests
To ensure everything works correctly, run the tests using unittest:

python -m unittest discover tests/

This will execute all test cases in the tests/ directory.

Expected Output
A output csv file will be generated with columns:
- Employee_Name
- Employee_EmailID
- Secret_Child_Name
- Secret_Child_EmailID

Each row represents an employee and their assigned Secret Santa recipient.
