import random

class FisherYatesDerangement:
    def __init__(self, employees, previous_assignments, logger):
        """
        Initializes the Fisher-Yates Derangement generator.

        :param employees: List of employee email IDs.
        :param previous_assignments: Dictionary {giver_email: recipient_email} from previous year.
        :param logger: Logger instance for debugging.
        """
        self.employees = employees
        self.previous_assignments = previous_assignments
        self.logger = logger

    def generate(self):
        """
        Generates a valid derangement ensuring:
        - No self-assignment
        - No repeat from the previous year

        :return: List of indices representing the derangement.
        """
        n = len(self.employees)
        indices = list(range(n))

        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            if j == i:
                j = (j - 1) if j > 0 else (j + 1)

            indices[i], indices[j] = indices[j], indices[i]

        # Validate against previous assignments
        if self.previous_assignments:
            prev_conflicts = {
                i for i in range(n) if self.previous_assignments.get(self.employees[i]) == self.employees[indices[i]]
            }

            if prev_conflicts:
                self.logger.warning(f"Previous assignment conflict detected for {len(prev_conflicts)} participants. Retrying swaps.")
                while prev_conflicts:
                    i = prev_conflicts.pop()
                    j = random.randint(0, n - 1)
                    if j not in prev_conflicts and j != i:
                        indices[i], indices[j] = indices[j], indices[i]

        self.logger.info("Successfully generated valid derangement.")
        return indices

