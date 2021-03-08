# you must set: 1. file path of log (infile in get_actual_log())
#               2. search expression (pharse in log_scan())
#               3. email (send_to_email,subject in sendemail())
#               4. path to the service restart script (main)
# python version: .2.7 



from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, datetime
import subprocess



#function that returns the path of the current log file - today's log name
def get_actual_log():
    name = "log_name" + str(date.today()) + ".log"
    name = name.replace('-', '')
    print("Name of log:", name)
    infile = 'C:\Python_test_file\\'+name
    #infile = name
    print(infile)
    return infile

#saves program status info to the log
def save_to_log(info_to_log):
    logfile = open("status.log","w")
    info_to_log = str(info_to_log)
    logfile.write(info_to_log)
    logfile.close()

#function generating time for program pause
def sleep_time ():
    sleep_time = 24 - datetime.now().hour
    sleep_time = sleep_time * 3600
    return sleep_time

# scans the document for the entered text and evaluates it true, false
def log_scan(infile):
    important = ''
    try:
        phrase = "expression"
        with open(infile) as f:
            f = f.readlines()
        for line in f:
            if phrase in line:
                important = line
                infoscan = "Log error found: true"
                print(infoscan)
                return True, important, infoscan
        infoscan = "Log error found: false"
        print(infoscan)
        return False, important, infoscan
    except:
        infoscan = 'Log does not exist or another opening file error'
        print(infoscan)
        return False, important, infoscan


#send email
def sendemail(message): 
    try:
        email = 'name_email'
        password = 'password'
        send_to_email = 'name_email'
        subject = 'subject'  # The subject line

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = send_to_email
        msg['Subject'] = subject

        # Attach the message to the MIMEMultipart object
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP_SSL('smtp.seznam.cz', 465)
        # server.starttls()
        server.login(email, password)
        text = msg.as_string()  # You now need to convert the MIMEMultipart object to a string to send
        server.sendmail(email, send_to_email, text)
        server.quit()

        emailstatus = 'Email was sent'
        print(emailstatus)
        return emailstatus
    except:
        emailstatus = 'Email send error'
        print(emailstatus)
        save_to_log(infolog)
        return emailstatus

# main
if __name__ == "__main__":
    while True:
        print("I am alive!")
        infile = get_actual_log()
        result, important, infoscan = log_scan(infile)
        infolog = ""
        emailstatus = ""
        
        if result == True: #found the search expression
            message = important
            emailstatus = sendemail(message)
            if emailstatus == 'Email send error':
                sleep(30)
                emailstatus = sendemail(message)
            print("Error: ", important)
            print("I'm waiting for a new log")
            infolog = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), infoscan, emailstatus,  "I'm waiting for a new log"
            save_to_log(infolog)
            try: #restart services
                subprocess.call([r'C:\Python_test_file\test_bat\restart_service.bat', '>C:\\Python_test_file\\test_bat\\restart_service.log']) #call restart script(bash) and redirects output
            except:
                print ("Restart service error")
            time_to_sleep = sleep_time()
            sleep(time_to_sleep)  # waiting for the new log (next day)

        else: #the expression was not found, after 1 hour will repeat scan
            print("I'm waiting 1 hour")
            infolog = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), infoscan, emailstatus, "I'm waiting 1 hour"
            save_to_log(infolog)
            sleep(3600)