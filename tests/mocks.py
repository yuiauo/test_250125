# ========================= login endpoint ========================
post_login_user_not_found = {
    'login': 'string',
    'password': 'string',
}

post_login_bad_password = {
    'login': 'patient_1',
    'password': 'string',
}

post_login_patient_ok = {
    'login': 'patient_1',
    'password': 'qwe123rty456',
}

post_login_doctor_ok = {
    'login': 'doctor_1',
    'password': 'qwe12r3ty456',
}
