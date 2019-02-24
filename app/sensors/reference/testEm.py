# Python code to illustrate Sending mail from
# your Gmail account
import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login("smartdev1572@gmail.com", "xxxxxxxxxxxxxxx")

# message to be sent
message = "Message_you_need_to_send"

# sending the mail
s.sendmail("smartdev1572@gmail.com", "ajinathkumbhar@gmail.com", message)

# terminating the session
s.quit()
