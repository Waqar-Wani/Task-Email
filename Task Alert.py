import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
import re
from datetime import datetime

def read_email_config():
    config = configparser.ConfigParser()
    config.read('Email config.ini')
    sender_email = config.get('Email', 'sender_email')
    receiver_emails = config.get('Email', 'receiver_emails', fallback='').split(',')
    password = config.get('Email', 'password')
    return sender_email, receiver_emails, password

def retrieve_last_runtime(task_name):
    try:
        # Attempt to retrieve last runtime using schtasks.exe
        result_schtasks = subprocess.run(
            f'schtasks.exe /query /TN "{task_name}" /FO LIST /V | findstr /C:"TaskName" /C:"Last Run Time" /C:"Next Run Time"',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )

        # Extract the next runtime from the schtasks output
        last_runtime_match = re.search(r'Last Run Time:\s+(.*)', result_schtasks.stdout)
        last_runtime = last_runtime_match.group(1).strip() if last_runtime_match else "Not available"

    except Exception as e:
        # Handle exceptions or log errors
        print(f"An error occurred while retrieving last runtime using schtasks.exe: {e}")
        last_runtime = "Not available"

    return last_runtime

def main():
    # Read email configuration
    sender_email, receiver_emails, password = read_email_config()
    print(f"Send To: {receiver_emails}")


    # Replace with your task name
    scheduled_task_name = "biometricdatasync"

    # Retrieve the next runtime of the task
    last_runtime = retrieve_last_runtime(scheduled_task_name)

    try:
        # Check if the task has completed
        result_completion = subprocess.run(
            f'schtasks.exe /query /TN "{scheduled_task_name}" | findstr "Ready"',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )

        if "Ready" in result_completion.stdout:
            # Task has completed, send email alert
            subject = "Srinagar Biometric Sync"

            # Format the last runtime using dd-Month-yyyy and time as 10:20 PM
            last_runtime_formatted = datetime.strptime(last_runtime, "%d-%m-%Y %H:%M:%S").strftime("%d-%B-%Y %I:%M:%S %p")

            body = (
                f"Srinagar Biometric device sync has completed successfully.\n"
                f"Last runtime: {last_runtime_formatted}"
            )

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = ', '.join(receiver_emails)
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_emails, message.as_string())
                print("Email alert sent successfully.")

    except Exception as e:
        # Handle exceptions or log errors
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
