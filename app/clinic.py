import datetime
from appointment import Appointment

MAX_DAYS = 10


class Clinic:
    def __init__(self, name, password, doctors, patients):
        self.name = name
        self.password = password
        self.doctors = doctors
        self.patients = patients
        self.appointments = []

    def get_doctor_by_document(self, document):
        for doctor in self.doctors:
            if doctor.document == document:
                return doctor
        return None

    def get_patient_by_document(self, document):
        for patient in self.patients:
            if patient.document == document:
                return patient
        return None

    def add_doctor(self, doctor):
        self.doctors.append(doctor)

    def get_appointments_by_date(self, date):
        return [appointment for appointment in self.appointments if appointment.date == date]

    def get_appointments_by_doctor(self, doctor):
        return [appointment for appointment in self.appointments if appointment.doctor.document == doctor.document]

    def get_appointments_by_patient(self, patient):
        return [appointment for appointment in self.appointments if appointment.patient.document == patient.document]

    def add_appointment(self, doctor, patient, date):
        appointment = Appointment(doctor, patient, date)
        self.appointments.append(appointment)

    def cancel_appointment(self, appointment):
        self.appointments.remove(appointment)

    def check_doctor_availability_by_date(self, doctor, date):
        count = 0
        for appointment in self.appointments:
            if appointment.doctor.document == doctor.document and appointment.date == date:
                count += 1
        return count < doctor.max_availability_per_day

    def get_doctor_appointments_by_date(self, doctor, date):
        return [appointment for appointment in self.appointments if appointment.doctor.document == doctor.document and appointment.date == date]

    def get_doctor_next_dates_available(self, doctor):
        dates = []
        date = datetime.date.today()
        while len(dates) < MAX_DAYS:
            appointments = self.get_doctor_appointments_by_date(doctor, date)
            if len(appointments) < doctor.max_availability_per_day:
                dates.append(date.strftime('%Y-%m-%d'))
            date = date + datetime.timedelta(days=1)
        return dates

    def get_available_doctors_by_specialty_and_date(self, specialty_name, date):
        doctors = []
        for doctor in self.doctors:
            if self.check_doctor_availability_by_date(doctor, date):
                specialties_names = doctor.get_specialties_names()
                if specialty_name in specialties_names:
                    doctors.append(doctor)
        return doctors

    def get_specialties_offered(self):
        specialties = set(
            specialty for doctor in self.doctors for specialty in doctor.get_specialties_names())
        return list(specialties)
