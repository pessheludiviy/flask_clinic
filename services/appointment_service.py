from repositories.appointment_repo import create_appointment

def book(user_id, doctor_id, time):
    create_appointment(user_id, doctor_id, time)
