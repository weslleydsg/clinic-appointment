import datetime
from appointment import Appointment

MAX_DAYS = 10


class Doctor:
    def __init__(self, name, specialties, max_availability_per_day):
        self.name = name
        self.specialties = specialties
        self.max_availability_per_day = max_availability_per_day
        self.appointments = []

    def __str__(self):
        return self.name

    def get_specialties_names(self):
        return [item.name for item in self.specialties]

    def add_appointment(self, patient, date):
        appointment = Appointment(patient, date)
        self.appointments.append(appointment)

    def check_availability_by_date(self, date):
        count = 0
        for appointment in self.appointments:
            if appointment.date == date:
                count += 1
        return count < self.max_availability_per_day

    def get_appointments_by_date(self, date):
        appointments = []
        for appointment in self.appointments:
            if appointment.date == date:
                appointments.append(appointment)
        return appointments

    def get_next_dates_available(self):
        dates = []
        date = datetime.date.today()
        while len(dates) < MAX_DAYS:
            appointments = self.get_appointments_by_date(date)
            if len(appointments) < self.max_availability_per_day:
                dates.append(date.strftime('%Y-%m-%d'))
            date = date + datetime.timedelta(days=1)
        return dates
