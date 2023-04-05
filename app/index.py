from specialty import Specialty
from doctor import Doctor
from patient import Patient
from clinic import Clinic
from ui_client import UiClient

cardiology = Specialty("Cardiology")
dermatology = Specialty("Dermatology")

doctors = [Doctor("Dr. Expert", [dermatology], 2), Doctor("Dr. Cardio", [cardiology, dermatology], 10),
           Doctor("Dr. Derma", [dermatology], 8)]

patients = [Patient("123", "Some One"), Patient("701", "Weslley Gomes")]

clinic = Clinic("Best Clinic", "pass", doctors, patients)

ui_client = UiClient([clinic])
ui_client.start_clinic_services(0)
