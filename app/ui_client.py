import datetime


class UiClient:
    def __init__(self, clinics):
        self.home_services = ["Doctors Availability",
                              "Book Appointment", "Delete an Appointment", "Reports"]
        self.clinics = clinics

    def prompt_default_list_option(self, option_list, input_message):
        for index, item in enumerate(option_list):
            print(f"  #{index} - {item}")
        plain_selected_option = input(input_message)
        try:
            return int(plain_selected_option)
        except ValueError:
            print("You should provide a non negative integer")
        return None

    def get_input_template(self, message):
        return f"$ {message} > "

    def get_error_template(self, message):
        return f"\n! {message} !"

    def check_past_date(self, date):
        return date < datetime.date.today()

    def prompt_date(self):
        date_str = input(self.get_input_template(
            "When do you want to make an appointment? (YYYY-MM-DD)"))
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            return date
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")
        return None

    def start_clinic_services(self, clinic_index):
        clinic = self.clinics[clinic_index]
        print(f"# Welcome to {clinic.name} #\n")
        selected_option = self.prompt_default_list_option(self.home_services, self.get_input_template(
            "Which service are you looking for?"))
        service = self.home_services[selected_option]
        match selected_option:
            case 0:
                print(
                    f"\n# Selected Option: {service} #\n")
            case 1:
                print(
                    f"\n# Selected Option: {service} #\n")
                self.book_appointment(clinic_index)
            case 2:
                print(
                    f"\n# Selected Option: {service} #\n")
            case 3:
                print(
                    f"\n# Selected Option: {service} #\n")
            case _:
                print(
                    self.get_error_template(f"\"{selected_option}\" is not a valid service option"))
        print("")
        self.start_clinic_services(clinic_index)

    def show_patient_sign_in(self, clinic_index):
        document = input(
            self.get_input_template("What are your document number?"))
        patient = self.clinics[clinic_index].get_patient_by_document(document)
        if patient is None:
            print(self.get_error_template(
                f"There is no patient registered in this client for this document: \"{document}\""))
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
            date = self.prompt_date()
            if date is None:
                return
            is_past_date = self.check_past_date(date)
            if is_past_date:
                print("You must provide a non past date")
                return
            print("")
            doctors = clinic.get_available_doctors_by_specialty_and_date(
                specialty_name, date)
            if len(doctors) == 0:
                print("No doctors available")
                return
            selected_doctor = self.prompt_default_list_option(
                doctors, self.get_input_template("Which doctor would you rather?"))
            doctor = doctors[selected_doctor]
            doctor.add_appointment(patient, date)
            print("\n~ You have booked your appointment to",
                  date, "sucefully with", doctor.name, "~")
        except IndexError:
            print("\nSelected option is not valid")
