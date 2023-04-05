class Appointment:
    def __init__(self, doctor, patient, date):
        self.doctor = doctor
        self.patient = patient
        self.date = date

    def __str__(self):
        return f"Appointment on {self.date} with {self.doctor.name}"
