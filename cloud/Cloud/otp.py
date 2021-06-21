import smtplib, ssl

def send_otp(reciever,otp,for_what):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "saurabhtalele1122@gmail.com"  # Enter your address
    receiver_email = reciever # Enter receiver address
    password = "saurabh@1122"
    otp = otp
    message = ""
    if for_what == "register":

        message = """\
        Subject: OTP for MyCloud
        
        your OTP for Registration on MyCloud is """+otp
    elif for_what == "forgot":
        message = """\
               Subject: OTP for MyCloud

               your OTP for Password Reset on MyCloud is """ + otp

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)