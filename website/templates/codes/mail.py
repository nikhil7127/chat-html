import smtplib
from email.message import EmailMessage
import imghdr


# format sendEmail((sender,password),receiver,{"subject":subject,"body":body})

def sendEmail(sender, receiver, message_details, attachments=None):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    try:
        server.login(sender[0], sender[1])
    except Exception:
        return "loginError"
    msg = EmailMessage()
    msg["Subject"] = message_details["subject"]
    msg["From"] = sender[0]
    msg.set_content(message_details["body"])
    msg["To"] = receiver.split(";")
    if attachments:
        for file in attachments:
            try:
                with open(file, 'rb') as f:
                    file_data = f.read()
                    file_type = imghdr.what(f.name)
                    file_name = f.name
                msg.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)
            except Exception:
                with open(file, 'rb') as f:
                    file_data = f.read()
                    file_name = f.name
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
    try:
        server.send_message(msg)
        server.quit()
        return "messageSuccess"
    except Exception:
        return "messageError"

# if __name__ == '__main__':
#     sendEmail(("testingemail7127@gmail.com", "nikhil@7127"), "nikhilvarma7127@gmail.com;18b91a04d8@srkrec.edu.in",
#               {"subject": "nice move", "body": "sending"})
