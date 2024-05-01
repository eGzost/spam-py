import smtplib
import sys
import time
import threading
from textwrap import dedent

_, user, password = sys.argv

print(f"{user} {password}")
def send_test_message(
    sender: str,
    receiver: str,
    subject:str,
    message: str,
    user: str,
    password: str
):
    message = f"""\
        Subject: {subject}
        To: {receiver}
        From: {sender}
        {message}
    """

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.starttls()
        server.login(user, password)
        server.sendmail(sender, receiver, dedent(message))

EMAIL_SENT = False

def loading_spinner():
    while True:
        for cursor in '◜◝◞◟':
            sys.stdout.write('\rSending ' + cursor)
            sys.stdout.flush()
            time.sleep(0.1)
            if EMAIL_SENT:
                sys.stdout.write('\rDone!')
                return

subject = input('Subject: ')
message = input('Message: ')

sender = "A Test Sender <from@example.com>"
receiver = "A Test User <to@example.com>"

loading_spinner_thread = threading.Thread(target=loading_spinner)
loading_spinner_thread.start()
send_test_message(
    subject=subject,
    message=message,
    sender=sender,
    receiver=receiver,
    password=password,
    user=user
)
EMAIL_SENT = True