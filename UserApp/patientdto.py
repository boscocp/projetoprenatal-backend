class PatientDTO:
    def __init__(self, id, name, cpf, birt_date, email):
        self.id = id
        self.name = name
        self.cpf = cpf
        self.birt_date = birt_date
        self.email = email
    
    def __str__(self) -> str:
        return self.name