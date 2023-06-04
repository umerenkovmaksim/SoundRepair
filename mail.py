from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from mail_data import mail, password

# # create message object instance
# msg = MIMEMultipart()
# message = "Thank you"
# # setup the parameters of the message
# password = password
# msg['From'] = mail
# msg['To'] = "br3027645@gmail.com"
# msg['Subject'] = "Subscription"
# # add in the message body
# msg.attach(MIMEText(message, 'plain'))
# # create server
# server = smtplib.SMTP_SSL('smtp.gmail.com')
# server.starttls()
# server.ehlo()
# # Login Credentials for sending the mail
# server.login(msg['From'], password)
# # send the message via the server.
# server.sendmail(msg['From'], msg['To'], msg.as_string())
# server.quit()
# print("successfully sent email to %s:" % (msg['To']))

# with smtplib.SMTP_SSL("smtp.mail.yahoo.com", port=465) as connection:
#
#     connection.login(
#         user=mail,
#         password=password
#     )
#
#     connection.sendmail(
#         from_addr=mail,
#         to_addrs="br3027645@gmail.com",
#         msg=f"Subject:Text\n\n"
#             f"Body of the text"
)
