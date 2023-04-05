class Clinic:
    def __init__(self, name, password, doctors, patients):
        self.name = name
        self.password = password
        self.doctors = doctors
        self.patients = patients

    def add_doctor(self, doctor):
        self.doctors.append(doctor)

    def get_patient_by_document(self, document):
        for patient in self.patients:
            if patient.document == document:
                return patient
        return None

    def get_available_doctors_by_specialty_and_date(self, specialty_name, date):
        doctors = []
        for doctor in self.doctors:
            if doctor.check_availability_by_date(date):
                specialties_names = doctor.get_specialties_names()
                if specialty_name in specialties_names:
                    doctors.append(doctor)
        return doctors

    def get_specialties_offered(self):
        specialties = []
        for doctor in self.doctors:
            specialties_names = doctor.get_specialties_names()
            specialties = list(set(specialties + specialties_names))
        return specialties
