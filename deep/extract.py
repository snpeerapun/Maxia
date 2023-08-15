import re
import nltk

text = "On Monday, October 25th, at 09:30 AM, there is an appointment with a lawyer."

sentences = nltk.sent_tokenize(text)

for sentence in sentences:
    appointment_info = {
        "subject": "",
        "time": "",
        "date": "",
        "location": "",
        "attend": ""
    }

    # Extract the subject of the appointment.
    match = re.search(r"(.*) appointment", sentence)
    if match:
        appointment_info["subject"] = match.group(1)

    # Extract the time of the appointment.
    match = re.search(r"at ([0-2][0-9]:[0-5][0-9])", sentence)
    if match:
        appointment_info["time"] = match.group(1)

    # Extract the date of the appointment.
    match = re.search(r"(today|tomorrow|[0-9]{1,2} [a-zA-Z]{3}, [0-9]{4})", sentence)
    if match:
        appointment_info["date"] = match.group(1)

    # Extract the location of the appointment.
    match = re.search(r"at (.*)", sentence)
    if match and match.group(1) != appointment_info["subject"]:
        appointment_info["location"] = match.group(1)

    # Extract the attendee of the appointment.
    match = re.search(r"with (.*)", sentence)
    if match:
        appointment_info["attend"] = match.group(1)

    print(appointment_info)