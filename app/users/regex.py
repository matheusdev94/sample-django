from django.core.validators import RegexValidator

class Regex:
    cep_regex = RegexValidator(regex=r'^\d{8}$', message="O CEP deve conter 8 dígitos.")
    address_number_regex = RegexValidator(regex=r'^\d{1,7}$', message="O número do endereço deve conter no máximo 7 dígitos.")
    phone_regex = RegexValidator(regex=r'^\d{9,}$', message="O número de telefone deve conter 9 dígitos.")
    name_regex = RegexValidator(regex=r'^[a-zA-Z]{1,50}$', message="O nome deve conter apenas letras e ter no máximo 50 caracteres.")
    


