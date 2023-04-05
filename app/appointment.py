class Appointment:
    def __init__(self, patient, date):
        self.patient = patient
        self.date = date

    def __str__(self):
        return f"patient: {self.patient.name}; date: {self.date}"
