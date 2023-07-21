import smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

def prepare_attachment(path_of_file_to_send: str) -> MIMEBase:
    """Prepare the attachement for a email using the contents of a file.

    Args:
        path_of_file_to_send (str): Path of the file which needs to be attached to the mail.
                                    The file needs to be in PDF format.

    Returns:
        MIMEBase: MIMEBase object which can be attached to mail.
    """
    assert path_of_file_to_send.split(".")[-1]=="pdf", "Only PDF files are supported at the moment."
    filename = path_of_file_to_send
    
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    return part

def send_email_to_people(senders_email: str,
                         receipients: list, 
                         path_of_file_to_send: str, 
                         subject: str=f"Stocks to watch out for in Nifty 50 {date.today}",
                         body: str=f"Support and Resistance with RSI for Nifty 50 {date.today()}") -> None:
    """Send emails to a list of recepients with an attachment.

    Args:
        senders_email (str): Email of the sender.
        receipients (list): List of recepeints.
        path_of_file_to_send (str): File to send as attachment.
        subject (str, optional): Subject of the email. Defaults to "Stocks to watch out for in Nifty 50 {date.today}".
        body (str, optional): Body of the email. Defaults to "Support and Resistance with RSI for Nifty 50 {date.today()}".
    """
    password = input("Type your password and press enter:")
    part = prepare_attachment(path_of_file_to_send)
    
    for recepient in receipients:
        receiver_email = recepient
        
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = senders_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(senders_email, password)
            server.sendmail(senders_email, receiver_email, text)