# Python version: 2.7 

import subprocess
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, datetime


SEARCHING_EXPRESSION = "your phrase in the log line"
LOG_NAME = "log_name"
LOG_PATH = "C:\\Python_test_file\\log\\"

# email variables
email_address = 'name_email'
email_password = 'password'
send_to_email = 'name_email'
subject = 'subject'  # The subject line
server = smtplib.SMTP_SSL('smtp.seznam.cz', 465)


# Function that returns the path of the current log file (today's log name)
def get_actual_log():
    name = LOG_NAME + str(date.today()) + ".log"
    name = name.replace('-', '')
    print("Name of log:", name)
    in_file = LOG_PATH + name
    print(in_file)
    return in_file

def save_status(info_to_log):
    logfile = open("status.log","w")
    logfile.write(str(info_to_log))
    logfile.close()

# Function generating time for program pause (time remaining to the next day)
def sleep_time ():
    sleep_time = 24 - datetime.now().hour
    sleep_time = sleep_time * 3600
    return sleep_time

# Scans the document for the entered text and evaluates it
def log_scan(file):
    line_from_log = ''
    try:
        with open(file) as f:
            f = f.readlines()
        for line in f:
            if SEARCHING_EXPRESSION in line:
                line_from_log = line
                scan_info = "Log error found: true"
                print(scan_info)
                return True, line_from_log, scan_info
        scan_info = "Log error found: false"
        print(scan_info)
        return False, line_from_log, scan_info
    except:
        scan_info = 'Log does not exist or another opening file error'
        print(scan_info)
        return False, line_from_log, scan_info

def send_email(message): 
    try:
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = send_to_email
        msg['Subject'] = subject
        # Attach the message to the MIMEMultipart object
        msg.attach(MIMEText(message, 'plain'))

        # server.starttls()
        server.login(email_address, email_password)
        text = msg.as_string()  # You now need to convert the MIMEMultipart object to a string to send
        server.sendmail(email_address, send_to_email, text)
        server.quit()

        email_status = 'Email was sent'
        print(email_status)
        return email_status
    except:
        emailstatus = 'Email send error'
        print(emailstatus)
        save_to_log(infolog)
        return emailstatus


if __name__ == "__main__":
    while True:
        print("I am alive!")
        file = get_actual_log()
        result, line_from_log, scan_info = log_scan(file)
        info_to_log = ""
        email_status = ""
        
        if result == True: # found the search expression
            message = line_from_log
            email_status = send_email(message)
            if email_status == 'Email send error':
                sleep(30)
                email_status = send_email(message)
            print("Error: ", line_from_log)
            info_message = "I'm waiting for a new log"
            print(info_message)
            info_to_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), scan_info, email_status, info_message
            save_status(info_to_log)
            try: # restart services
                subprocess.call(['restart_service.bat', '>restart_service.log']) # call restart script and redirects output
            except:
                print ("Restart service error")
            time_to_sleep = sleep_time()
            sleep(time_to_sleep) # waiting for the new log (next day)

        else: # the expression was not found, after 1 hour will repeat scan
            info_message = "I'm waiting 1 hour"
            print(info_message)
            info_to_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), scan_info, email_status, info_message
            save_status(info_to_log)
            sleep(3600)
