class Doctor:
    def __init__(self, document, name, specialties, max_availability_per_day):
        self.document = document
        self.name = name
        self.specialties = specialties
        self.max_availability_per_day = max_availability_per_day

    def __str__(self):
        return self.name

    def get_specialties_names(self):
        return [item.name for item in self.specialties]
