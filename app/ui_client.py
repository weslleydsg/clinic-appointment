import datetime


class UiClient:
    def __init__(self, clinics):
        self.home_services = ["Doctors Availability",
                              "Book Appointment", "Cancel an Appointment", "Reports"]
        self.clinics = clinics

    def prompt_default_list_option(self, option_list, input_message):
        for index, item in enumerate(option_list):
            print(f"  #{index} - {item}")
        plain_selected_option = input(input_message)
        try:
            return int(plain_selected_option)
        except ValueError:
            print(
                self.get_error_template("\nYou should provide a non negative integer"))
        return None

    def get_input_template(self, message):
        return f"$ {message} > "

    def get_error_template(self, message):
        return f"\n! {message} !"

    def check_past_date(self, date):
        return date < datetime.date.today()

    def prompt_date(self, message):
        input_message = self.get_input_template(
            f"{message} (YYYY-MM-DD)")
        date_str = input(input_message)
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            return date
        except ValueError:
            print(
                self.get_error_template("\nInvalid date format. Please enter the date in the format YYYY-MM-DD."))
        return None

    def start_clinic_services(self, clinic_index):
        clinic = self.clinics[clinic_index]
        print(f"# Welcome to {clinic.name} #\n")
        selected_option = self.prompt_default_list_option(self.home_services, self.get_input_template(
            "Which service are you looking for?"))
        try:
            service = self.home_services[selected_option]
            match selected_option:
                case 0:
                    print(
                        f"\n# Selected Option: {service} #\n")
                    self.show_doctor_availability(clinic_index)
                case 1:
                    print(
                        f"\n# Selected Option: {service} #\n")
                    self.book_appointment(clinic_index)
                case 2:
                    print(
                        f"\n# Selected Option: {service} #\n")
                    self.cancel_appointment(clinic_index)
                case 3:
                    print(
                        f"\n# Selected Option: {service} #\n")
                    self.prompt_reports(clinic_index)
                case _:
                    print(
                        self.get_error_template(f"\"{selected_option}\" is not a valid service option"))
        except IndexError:
            print(
                self.get_error_template("\nSelected option is not valid"))
        except TypeError:
            print(
                self.get_error_template("\nYou should provide a non negative integer"))
        print("")
        self.start_clinic_services(clinic_index)

    def show_doctor_sign_in(self, clinic_index):
        document = input(
            self.get_input_template("\nWhat are your document number?"))
        doctor = self.clinics[clinic_index].get_doctor_by_document(document)
        if doctor is None:
            print(self.get_error_template(
                f"There is no doctor registered in this clinic for this document: \"{document}\""))
            return None
        print(f"\n# Welcome, {doctor.name} #\n")
        return doctor

    def show_patient_sign_in(self, clinic_index):
        document = input(
            self.get_input_template("What are your document number?"))
        patient = self.clinics[clinic_index].get_patient_by_document(document)
        if patient is None:
            print(self.get_error_template(
                f"There is no patient registered in this clinic for this document: \"{document}\""))
            return None
        print(f"\n# Welcome, {patient.name} #\n")
        return patient

    def book_appointment(self, clinic_index):
        patient = self.show_patient_sign_in(clinic_index)
        if patient is None:
            return
        clinic = self.clinics[clinic_index]
        specialties = clinic.get_specialties_offered()
        selected_specialty = self.prompt_default_list_option(
            specialties, self.get_input_template("Which specialty are you looking for?"))
        try:
            specialty_name = specialties[selected_specialty]
            print(f"\n# Selected Specialty: \"{specialty_name}\" #\n")
            date = self.prompt_date("When do you want to make an appointment?")
            if date is None:
                return
            is_past_date = self.check_past_date(date)
            if is_past_date:
                print(
                    self.get_error_template("You must provide a non past date"))
                return
            print("")
            doctors = clinic.get_available_doctors_by_specialty_and_date(
                specialty_name, date)
            if len(doctors) == 0:
                print(
                    self.get_error_template("No doctors available"))
                return
            selected_doctor = self.prompt_default_list_option(
                doctors, self.get_input_template("Which doctor would you rather?"))
            doctor = doctors[selected_doctor]
            clinic.add_appointment(doctor, patient, date)
            print("\n~ You have booked your appointment to",
                  date, "successfully with", doctor.name, "~")
        except IndexError:
            print(
                self.get_error_template("\nSelected option is not valid"))
        except TypeError:
            print(
                self.get_error_template("\nYou should provide a non negative integer"))

    def show_doctor_availability(self, clinic_index):
        try:
            clinic = self.clinics[clinic_index]
            selected_doctor = self.prompt_default_list_option(
                clinic.doctors, self.get_input_template("Which doctor would you rather?"))
            doctor = clinic.doctors[selected_doctor]
            dates = clinic.get_doctor_next_dates_available(doctor)
            print(f"\n# {doctor.name} next dates available is: #")
            for date in dates:
                print(f"    {date}")
        except IndexError:
            print(
                self.get_error_template("\nSelected option is not valid"))
        except TypeError:
            print(
                self.get_error_template("\nYou should provide a non negative integer"))

    def cancel_appointment(self, clinic_index):
        try:
            patient = self.show_patient_sign_in(clinic_index)
            if patient is None:
                return
            clinic = self.clinics[clinic_index]
            appointments = clinic.get_appointments_by_patient(patient)
            if len(appointments) == 0:
                print(
                    self.get_error_template("You have no appointments"))
                return
            selected_appointment = self.prompt_default_list_option(
                appointments, self.get_input_template("Which appointment do you want to cancel?"))
            clinic.cancel_appointment(appointments[selected_appointment])
        except IndexError:
            print(
                self.get_error_template("\nSelected option is not valid"))

    def show_appointments(self, appointments):
        for appointment in appointments:
            print(
                f"    Appointment on {appointment.date} for patient {appointment.patient.name} with {appointment.doctor.name}")

    def handle_show_appointments(self, appointments):
        if len(appointments) == 0:
            print(
                self.get_error_template("The is no appointments available"))
            return
        self.show_appointments(appointments)

    def show_clinic_appointments_by_date(self, clinic, date):
        appointments = clinic.get_appointments_by_date(date)
        if len(appointments) == 0:
            print(
                self.get_error_template("The is no appointments available"))
            return
        print("\n# Appointments for date:", date, ":\n")
        self.show_appointments(appointments)

    def prompt_reports(self, clinic_index):
        reports_option = ["Patient appointments", "Doctor appointments",
                          "Clinic appointments for today", "Clinic appointments by date"]
        selected_option = self.prompt_default_list_option(reports_option, self.get_input_template(
            "Which service are you looking for?"))
        clinic = self.clinics[clinic_index]
        match selected_option:
            case 0:
                print("")
                patient = self.show_patient_sign_in(clinic_index)
                appointments = clinic.get_appointments_by_patient(patient)
                self.handle_show_appointments(appointments)
            case 1:
                doctor = self.show_doctor_sign_in(clinic_index)
                appointments = clinic.get_appointments_by_doctor(doctor)
                self.handle_show_appointments(appointments)
            case 2:
                date = datetime.date.today()
                self.show_clinic_appointments_by_date(clinic, date)
            case 3:
                date = self.prompt_date(
                    "When do you want to see the appointments?")
                self.show_clinic_appointments_by_date(clinic, date)
            case _:
                print(
                    self.get_error_template(f"\"{selected_option}\" is not a valid report option"))
