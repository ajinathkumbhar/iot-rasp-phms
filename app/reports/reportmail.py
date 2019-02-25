import smtplib
import os
from string import Template
from sensors.accevents import AccEvents

mAccEvent = AccEvents()

class Pimail:
    def __init__(self):
        self.__name = "Pimail"
        self.__email_config = os.path.expanduser('~/emailconfig.txt')
        self.__contacts = os.path.expanduser('reports/contacts.txt')
        self.__message_template = os.path.expanduser('reports/message.txt')
        self.__sender_id = None
        self.__sender_pass = None
        self.__load_email_config()

    def __load_email_config(self):
        with open(self.__email_config, mode='r') as config_file:
            for word in config_file:
                self.sender_id = word.split()[0]
                self.sender_pass = word.split()[1]

    def __get_contacts(self,filename):
        """
        Return two lists names, emails containing names and email addresses
        read from a file specified by filename.
        """
        names = []
        emails = []
        with open(filename, mode='r') as contacts_file:
            for a_contact in contacts_file:
                names.append(a_contact.split()[0])
                emails.append(a_contact.split()[1])
        return names, emails

    def __read_template(self,filename):
        """
        Returns a Template object comprising the contents of the
        file specified by filename.
        """

        with open(filename, 'r') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    def send(self,sens_data):
        names, emails = self.__get_contacts(self.__contacts) # read contacts
        message_template = self.__read_template(self.__message_template)
        evt = mAccEvent.get_event_str(sens_data.acc_event)
        # set up the SMTP server
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(self.sender_id, self.sender_pass)

        # For each contact, send the email:
        for name, email in zip(names, emails):
            # add in the actual person name to the message template
            message = message_template.substitute(SUBJECT="Report",
                                                  PERSON_NAME=name.title(),
                                                  ID="3256AD887WQ",
                                                  PULSE_RATE=str(sens_data.hbeat),
                                                  TEMP=str(sens_data.temp),
                                                  GES_EVENT=evt
                                                  )
            # Prints out the message body for our sake
            print(message)

                # send the message via the server set up earlier.
            print "Sending mail form : " + self.sender_id + " to " + email
            # try:
            #     s.sendmail(self.sender_id,email,message)
            # except:
            #     print "failed to send email to " + email

        # Terminate the SMTP session and close the connection
        s.quit()




