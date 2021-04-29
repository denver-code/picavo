import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

username = 'picavo.adm@gmail.com'  
password = 'kertsher'  


def send_confirm(to_address, con_url):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Auth info"
    msg['From'] = username
    msg['To'] = to_address
    html = """<p><h2>Hey!</h2></p> 
<p><h3>If you want to continue using the PicAvo platform then you need to confirm your address.</h3></p>
<p><h3>To do this, follow the link below, otherwise your account will be deleted after 4 hours.</h3></p>
<center><a href="""+con_url+""">Activate</a></center>"""
    part1 = MIMEText(html, 'html')
    msg.attach(part1)
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.ehlo()
    server.starttls()
    server.login(username,password)  
    server.sendmail(username, to_address, msg.as_string())  
    server.quit()

def send_code(to_address, ccode):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Auth info"
    msg['From'] = username
    msg['To'] = to_address
    html = """<p><h2>Hey!</h2></p> 
<p><h3>If you want to reset your password continue read this message, else close this message.</h3></p>
<p><h3>To do this, enter a code below to form in picavo page.</h3></p>
<center><h1><b>"""+ccode+"""</b></h1></center>"""
    part1 = MIMEText(html, 'html')
    msg.attach(part1)
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.ehlo()
    server.starttls()
    server.login(username,password)  
    server.sendmail(username, to_address, msg.as_string())  
    server.quit()
    