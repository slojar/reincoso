import profile
from re import A
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.core.mail import send_mail
from loan.models import Loan, LoanTransaction

from savings.models import Saving

from .models import Profile, Wallet

# Email imports

# import requests
# response = requests.post(
#     "https://api.mailgun.net/v3/sandboxfc1f18e495b442d6a7ec1dfef04b8044.mailgun.org/messages",
#     auth=("api", "0fc607b5f9c416383d7143401f1308c9-38029a9d-18a8e2d0"),
#     data={"from": "mailgun@sandboxfc1f18e495b442d6a7ec1dfef04b8044.mailgun.org",
#           "to": ["definatelycrypticwisdom@gmail.com"],
#           "subject": "Testing mailgun",
#           "text": "Testing some Mailgun awesomness!"}
# )

# Done cleaned _/ Reformat message
def send_welcome_email_to_user(profile):
    body = f'''
    Dear {profile.user.first_name},
        [Reincoso Cooperative Society] welcomes you! 
        We're thrilled to have you among us. We consider ourselves fortunate that you picked us and I'd want to express 
        our gratitude on behalf of the whole organization. In the meanwhile, please visit our website (www.reincosocoop.com) 
        to learn more about our products and services.
    '''
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = profile.user.email
    message["Subject"] = "Welcome to REINCOSO"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, profile.user.email, text)
    print("welcome Email has been sent")

# Done _/ Reformat message
def successful_membership_fee_payment(trans) -> None:
    body = f"""
    Dear {trans.user.user.first_name},
        Thank you for choosing Reincoso Cooperative Society, Your membership fee of 100,000 is successful. For any further
        inquiry please contact us on:
        Email - coopadmin@reincoso.com
    
    """
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = trans.user.user.email
    message["Subject"] = "Success Payment"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, trans.user.user.email, text)
    print("Success Membership Payment Email has been sent")

# Done _/ Reformat message
def failed_membership_fee_payment(trans) -> None:
    body = f"""
    Dear {trans.user.user.first_name},    
        Your membership fee payment of 100,000 was not successful. Kindly try again or contact us on coopadmin@reincoso.com.
        If the problem presides, please contact your bank
    """
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = trans.user.user.email
    message["Subject"] = "Failed Membership Payment"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, trans.user.user.email, text)
    print("Failed Payment Email has been sent")

# Done _/ Reformat message
def successful_quick_save_mail(profile, amount) -> None:
    balance = Wallet.objects.get(user=profile).balance
    
    print(profile)
    body = f"""
      Dear {profile.user.first_name},    
            Thank you for using Reincoso Quick Save option.Your quick save of N{amount} is successful.
            Your current balance is N{balance}.
      """
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = profile.user.email
    message["Subject"] = "Successful Quick Save"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, profile.user.email, text)
    print("Success Auto Save Email has been sent")

# Done _/ Reformat message
def failed_quick_save_mail(profile, amount) -> None:
    balance = Wallet.objects.get(user=profile)
    body = f"""
        Dear {profile.user.first_name},
            Your Quick Save option of N{amount} is NOT successful (due to insufficient bank balance or network issues). 
            Kindly try again or contact us on coopadmin@reincoso.com. If the problem presides, please contact your bank
        """
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = profile.user.email
    message["Subject"] = "Failed Quick Save"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, profile.user.email, text)
    print("Failed Auto Save Email has been sent")

# Opt into Automated Savings ?? I haven't figured out the point where user opts into Auto_Save plan
def auto_save_creation_mail(profile_name, duration_name) -> None:
    body = f"""
    Dear {profile_name},
        You have successfully opted for our {duration_name} Auto save plan. 
        For any further inquiry, please contact us on:
        Email - coopadmin@reincoso.com
    """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = profile.user.email
    message["Subject"] = "Activated Auto Save"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, profile.user.email, text)
    print("Activated Auto Save Email has been sent")

# Done _/ Text format
def successful_auto_save_mail(profile, amount) -> None:
    balance = Wallet.objects.get(user=profile).balance
    body = f"""
    Dear {profile.user.first_name},
        Thank you for using Reincoso Auto Save option. Your Auto save of N{amount.amount} ({amount.duration})
        plan is successful. Your current balance is N{balance}.
        
        For any further inquiry, please contact us on:
        Email - coopadmin@reincoso.com
    """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = profile.user.email
    message["Subject"] = "Success Auto Save"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, profile.user.email, text)
    print("Success Auto Save Email has been sent")

# Done _/ Text format
def failed_auto_save_mail(profile, amount) -> None:
    body = f"""
        Dear {profile.user.first_name},
            Your Auto Save option of N{amount.amount} ({amount.duration}) plan is NOT successful (due to insufficient bank balance or network issues).
            Kindly try again or contact us on coopadmin@reincoso.com. 
            If the problem presides, please contact your bank.
        """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] =  settings.DEFAULT_FROM_EMAIL
    message["To"] = profile.user.email
    message["Subject"] = "Failed Auto Save"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, profile.user.email, text)
    print("Failed Auto Save Email has been sent")

# Partially done but, Expecting an error here !! 
def successful_investment_mail(request, investment, user_transaction) -> None:
    body = f"""
Dear {request.user.first_name},

You have made an investment of {user_transaction.amount} on ({investment.investment.type.name}) with {investment.percentage}% per annum.
Your current investment balance is N{investment.amount_invested}.

For any further inquiry, please contact us on:
Email - coopadmin@reincoso.com
    """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = request.user.email
    message["Subject"] = "Successful investment mail"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, request.user.email, text)
    print("Successful investment Email has been sent")

# partially done _/
def failed_investment_mail(request, user_investment, user_transaction) -> None:
    body = f"""
Dear {request.user.first_name},

Your Investment of N{user_transaction.amount} on {user_investment.investment.type.name} is NOT successful (due to insufficient bank balance or network issues). 
Kindly try again or contact us on coopadmin@reincoso.com. If the problem presides, please contact your bank
    """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = "crypticwisdom84@gmail.com"
    message["To"] = request.user.email
    message["Subject"] = "Failed investment mail"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, request.user.email, text)
    print("Failed investment mail Email has been sent")

# pending ...
def investment_maturity_mail(request) -> None:
    balance = Wallet.objects.get(user=request.user).balance
    body = f"""
        Dear {request.user.first_name},
        We are pleased to notify you that your Nxxxx investment in (Real estate/P2P/Agriculture/Fixed income) has matured and interest will be paid to you shortly. 
        For any further inquiry please contact us on:
        Email - coopadmin@reincoso.com
    """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = "crypticwisdom84@gmail.com"
    message["To"] = request.user.email
    message["Subject"] = "Investment maturity mail"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, request.user.email, text)
    print("Investment maturity mail Email has been sent")

# done and well formatted _/
def loan_request_processing_mail(request) -> None:
    #: This body was indented this way intentionally, so as to be well structured when recieved via mail.
    body = f"""
Dear {request.user.first_name},

Your loan application has been received and is being reviewed by the loan committee.\n
Your loan will be disbursed as soon as all requirements are met.

For any further inquiry please contact us on:
Email - coopadmin@reincoso.com

"""

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = request.user.email
    message["Subject"] = "Loan request processing mail"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, request.user.email, text)
    print("Loan request processing mail Email has been sent")

# done _/ text format
def mail_to_guarantor(request, guarantor) -> None:
    profile = Profile.objects.get(user=request.user)
    loan = LoanTransaction.objects.filter(user=profile).last()
    body = f"""
            Dear {guarantor.user.first_name},
                You have been selected to guarantee for the loan amount of N{loan.amount} for ({request.user.first_name}) and you will be held liable if the debts are not repaid. 
                You can accept or reject offer of guarantor-ship by sending Yes to accept / No to reject.
                For any further inquiry please contact us on:
                Email - coopadmin@reincoso.com
        """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = guarantor.user.email
    message["Subject"] = "Guarantor"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, request.user.email, text)
    print("Guarantor Email has been sent")

# done _/ text format
def inform_user_of_added_guarantor(request) -> None:
    profile = Profile.objects.get(user=request.user)
    loan = LoanTransaction.objects.filter(user=profile).last()
    guarantor = ", ".join(list(request.data.get("guarantor")))
    body = f"""
            Dear {request.user.first_name},
                You have added {guarantor} as your guarantor(s) for the loan amount of N{loan.amount}.
                For any further inquiry please contact us on:
                Email - coopadmin@reincoso.com
        """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = request.user.email
    message["Subject"] = "Guarantor Added"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, request.user.email, text)
    print("Guarantor Added Email has been sent")

# done and well formated _/ 
def admin_loan_processing_status_mail(request) -> None:
    body = f"""
Dear Reincoso,

The loan amount of N{request.data.get("amount")} from {request.user.first_name} is currently waiting to be reviewed and approved. 
Kindly go through it and process as due.
        """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = "crypticwisdom84@gmail.com"
    message["To"] = request.user.email
    message["Subject"] = "Loan processing status"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, request.user.email, text)
    print("Loan processing status to Admin Email has been sent")


def user_loan_processing_status_mail(request) -> None:
    body = f"""
Dear {request.user.first_name},

Your loan of Nxxxxx has been approved/rejected and the funds will be deposited into the account you gave shortly. 
Please read the terms and conditions that were emailed to you.
If rejected- Sorry, you do not match the criteria for a loan at this time, either save more or contact us.
For any further inquiry please contact us on:
Email - coopadmin@reincoso.com
        """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = "crypticwisdom84@gmail.com"
    message["To"] = request.user.email
    message["Subject"] = "Loan processing status"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, request.user.email, text)
    print(" Loan processing status to user Email has been sent")


def loan_clear_off(request) -> None:
    body = f"""
        Dear {request.user.first_name},
            Congratulations! You have successfully cleared your loan of Nxxxxxx. Your loan balance is N0.00. 
            You can apply for more loans with us.
            For any further inquiry please contact us on:
            Email - coopadmin@reincoso.com
        """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = request.user.email
    message["Subject"] = "Loan clear off"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, request.user.email, text)
    print("Loan clear off Email has been sent")

# done _/ text format
def withdrawal_request_mail_user(request) -> None:
    body = f"""
        Dear {request.user.first_name},
            Your application to make a withdrawal of N{request.data.get("amount")} has been received and is being reviewed by the committee.
            You will be credited shortly.
            For any further inquiry please contact us on:
            Email - coopadmin@reincoso.com
        """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = request.user.email
    message["Subject"] = "Withdraw Request"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, request.user.email, text)
    print("Withdraw Request Email has been sent")

# done _/ text format
def withdrawal_request_mail_admin(request, content) -> None:
    body = f"""
    Hi Reincoso,
        A withdrawal request of N{request.data.get("amount")} from {request.user.first_name} is currently
        waiting to be approved and disbursed.
        Kindly go through it and process as due.
        
    """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = settings.ADMIN_EMAIL
    message["Subject"] = "Withdrawal Request"
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_HOST_USER, settings.PORT, context=context) as server:
        server.login(settings.DEFAULT_FROM_EMAIL, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.DEFAULT_FROM_EMAIL, request.user.email, text)
    print("Withdrawal Request Email has been sent")

# def send_welcome_email_to_user(user):
#     name = user.first_name
#     if not name:
#         name = 'Investor'
#     name = 'Investor'
#     from_email = "crypticwisdom84@gmail.com"
#     email_to = ['definatelycrypticwisdom@gmail.com']
#     subject = 'Welcome to REINCOSO GROUP'
#     message = f"""
#         Dear {name},
#
#         We are happy to have you as an investor on WealthEx. You are now on the road to the most convenient way to crypto wealth.
#         With WealthEx, you can invest in any cryptocurrency of your choice anywhere in the world.
#
#         Please contact us at support@wealthexinvestment.com for more enquiries
#
#         Regards.
#         Reincoso Team
#
#         """
#
#     send_mail(subject=subject, message=message, from_email=from_email, recipient_list=email_to)
#
#     print(f'Email sent to: {email_to}')
    # send_mail('Subject here', 'Here is the message.', 'crypticwisdom84@gmail.com',
    #           ['definatelycrypticwisdom@gmail.com'], fail_silently=False)
