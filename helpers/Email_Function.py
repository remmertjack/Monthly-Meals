'''
Project: Monthly Meals
Title: Email Function
Author: Jack Remmert
Date: 5/23/2020
'''
from datetime import date
import calendar
import pandas as pd
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

send_email(receiver_email, receiver_name, file)

def send_email(receiver_email, receiver_name = None, file = None):
    # get Month and Year for Subject
    tdy = date.today()
    month_num = calendar.nextmonth(tdy.year,tdy.month)[1]
    month_name = calendar.month_name[month_num]
    year = tdy.year+1 if month_num == 1 else tdy.year
    
    # set up email settings
    port = 465 # For SSL
    password = input('Type your password and press enter: ')
    
    sender_email = "mealsmonthly@gmail.com"
    receiver_email = receiver_email
    
    message = MIMEMultipart('alternative')
    message["Subject"] = "Meals for " +month_name+" " + str(year)
    message["From"] = sender_email
    message["To"] = receiver_email
    
    addresse = 'Hi,' if pd.isnull(receiver_name) else 'Hi {},'.format(receiver_name)
    month_year = month_name + ' '+str(year)
    #==========
    # Body
    html = """\
    <html>
        <body>
            <p>{addresse}<br>
            <br>
            Here are your dinner meals for {month_year}!<br>
            <br>
            We hope you enjoy.<br>
            <br>
            Best, Monthly Meals <br>
            <br>
            <i>For any questions or comments please email 
            <a href="mailto:mealsmonthly@gmail.com"> mealsmonthly@gmail.com </a>
            with the month and meal in the subject line.
            </i>
        </body>
    </html>
    
    """.format(addresse=addresse, month_year=month_year)
    msg = MIMEText(html, 'html')
    message.attach(msg)
    
    #==========
    # Attach the Meals as an image
    # Open PDF file in binary mode
    if file is not None:
        with open(file, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)
        
        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file}",
        )
        
        # Add attachment to message and convert message to string
        message.attach(part)
    
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login('mealsmonthly@gmail.com',password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        # ToDo: send email here
    

