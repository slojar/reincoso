import profile
import requests
import logging
from re import A
from django.conf import settings
from investment.models import InvestmentTransaction, UserInvestment
from loan.models import Loan, LoanTransaction

from savings.models import Saving
from .models import Profile, Wallet


base_url = settings.EMAIL_API_URL
api_key = settings.EMAIL_API_KEY
email_sender = settings.EMAIL_SENDER


def log_request(*args):
    for arg in args:
        logging.info(arg)


def send_email_using_mailgun(recipient, subject, message):
    auth = ("api", api_key)
    data = dict()

    data['from'] = email_sender
    data['to'] = recipient
    data['subject'] = subject
    data['text'] = message

    response = requests.post(base_url, auth=auth, data=data)
    log_request(base_url, auth, data, response.json())
    return response


def send_welcome_email_to_user(profile):
    body = f'''
    Dear {profile.user.first_name},
        [Reincoso Cooperative Society] welcomes you! 
        We're thrilled to have you among us. We consider ourselves fortunate that you picked us and I'd want to express 
        our gratitude on behalf of the whole organization. In the meanwhile, please visit our website (www.reincosocoop.com) 
        to learn more about our products and services.
    '''

    recipient = profile.user.email
    subject = "Welcome to REINCOSO"

    send_email_using_mailgun(recipient, subject, body)


def successful_membership_fee_payment(trans) -> None:
    body = f"""
    Dear {trans.user.user.first_name},
        Thank you for choosing Reincoso Cooperative Society, Your membership fee of 100,000 is successful. For any further
        inquiry please contact us on:
        Email - coopadmin@reincoso.com
    
    """

    recipient = trans.user.user.email
    subject = "Success Payment"

    send_email_using_mailgun(recipient, subject, body)


def failed_membership_fee_payment(trans) -> None:
    body = f"""
    Dear {trans.user.user.first_name},    
        Your membership fee payment of 100,000 was not successful. Kindly try again or contact us on coopadmin@reincoso.com.
        If the problem presides, please contact your bank
    """

    recipient = trans.user.user.email
    subject = "Failed Membership Payment"

    send_email_using_mailgun(recipient, subject, body)


def successful_quick_save_mail(profile, amount) -> None:
    balance = Wallet.objects.get(user=profile).balance
    
    print(profile)
    body = f"""
      Dear {profile.user.first_name},    
            Thank you for using Reincoso Quick Save option.Your quick save of N{amount} is successful.
            Your current balance is N{balance}.
      """

    recipient = profile.user.email
    subject = "Successful Quick Save"

    send_email_using_mailgun(recipient, subject, body)


def failed_quick_save_mail(profile, amount) -> None:
    balance = Wallet.objects.get(user=profile)
    body = f"""
        Dear {profile.user.first_name},
            Your Quick Save option of N{amount} is NOT successful (due to insufficient bank balance or network issues). 
            Kindly try again or contact us on coopadmin@reincoso.com. If the problem presides, please contact your bank
        """

    recipient = profile.user.email
    subject = "Failed Quick Save"

    send_email_using_mailgun(recipient, subject, body)


# Opt into Automated Savings ?? I haven't figured out the point where user opts into Auto_Save plan
def auto_save_creation_mail(profile_name, duration_name) -> None:
    body = f"""
    Dear {profile_name},
        You have successfully opted for our {duration_name} Auto save plan. 
        For any further inquiry, please contact us on:
        Email - coopadmin@reincoso.com
    """

    recipient = profile.user.email
    subject = "Activated Auto Save"

    send_email_using_mailgun(recipient, subject, body)


def successful_auto_save_mail(profile, amount) -> None:
    balance = Wallet.objects.get(user=profile).balance
    body = f"""
    Dear {profile.user.first_name},
        Thank you for using Reincoso Auto Save option. Your Auto save of N{amount.amount} ({amount.duration})
        plan is successful. Your current balance is N{balance}.
        
        For any further inquiry, please contact us on:
        Email - coopadmin@reincoso.com
    """

    recipient = profile.user.email
    subject = "Success Auto Save"

    send_email_using_mailgun(recipient, subject, body)


def failed_auto_save_mail(profile, amount) -> None:
    body = f"""
        Dear {profile.user.first_name},
            Your Auto Save option of N{amount.amount} ({amount.duration}) plan is NOT successful (due to insufficient bank balance or network issues).
            Kindly try again or contact us on coopadmin@reincoso.com. 
            If the problem presides, please contact your bank.
        """

    recipient = profile.user.email
    subject = "Failed Auto Save"

    send_email_using_mailgun(recipient, subject, body)


# Partially done but, Expecting an error here !! 
def successful_investment_mail(request, investment_id) -> None:
    investment = UserInvestment.objects.get(id=investment_id, user=request.user.profile)
    user_transaction = InvestmentTransaction(user=request.user.profile, user_investment=investment)
    body = f"""
Dear {request.user.first_name},

You have made an investment of {user_transaction.amount} on ({investment.investment.type.name}) with {investment.percentage}% per annum.
Your current investment balance is N{investment.amount_invested}.

For any further inquiry, please contact us on:
Email - coopadmin@reincoso.com
    """

    recipient = request.user.email
    subject = "Successful investment mail"

    send_email_using_mailgun(recipient, subject, body)


# partially done _/
def failed_investment_mail(request, investment_id) -> None:
    user_investment = UserInvestment.objects.get(id=investment_id, user=request.user.profile)
    user_transaction = InvestmentTransaction(user=request.user.profile, user_investment=user_investment)
    body = f"""
Dear {request.user.first_name},

Your Investment of N{user_transaction.amount} on {user_investment.investment.type.name} is NOT successful (due to insufficient bank balance or network issues). 
Kindly try again or contact us on coopadmin@reincoso.com. If the problem presides, please contact your bank
    """

    recipient = request.user.email
    subject = "Failed investment mail"

    send_email_using_mailgun(recipient, subject, body)


# pending ...
def investment_maturity_mail(request) -> None:
    balance = Wallet.objects.get(user=request.user).balance
    body = f"""
        Dear {request.user.first_name},
        We are pleased to notify you that your Nxxxx investment in (Real estate/P2P/Agriculture/Fixed income) has matured and interest will be paid to you shortly. 
        For any further inquiry please contact us on:
        Email - coopadmin@reincoso.com
    """

    recipient = request.user.email
    subject = "Investment maturity mail"

    send_email_using_mailgun(recipient, subject, body)


def loan_request_processing_mail(request) -> None:
    #: This body was indented this way intentionally, so as to be well structured when recieved via mail.
    body = f"""
Dear {request.user.first_name},

Your loan application has been received and is being reviewed by the loan committee.\n
Your loan will be disbursed as soon as all requirements are met.

For any further inquiry please contact us on:
Email - coopadmin@reincoso.com

"""

    recipient = request.user.email
    subject = "Loan request processing mail"

    send_email_using_mailgun(recipient, subject, body)


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

    recipient = guarantor.user.email
    subject = "Guarantor"

    send_email_using_mailgun(recipient, subject, body)


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

    recipient = request.user.email
    subject = "Guarantor Added"

    send_email_using_mailgun(recipient, subject, body)


def admin_loan_processing_status_mail(request) -> None:
    body = f"""
Dear Reincoso,

The loan amount of N{request.data.get("amount")} from {request.user.first_name} is currently waiting to be reviewed and approved. 
Kindly go through it and process as due.
        """

    recipient = request.user.email
    subject = "Loan processing status"

    send_email_using_mailgun(recipient, subject, body)


def user_loan_processing_status_mail(request) -> None:
    body = f"""
Dear {request.user.first_name},

Your loan of Nxxxxx has been approved/rejected and the funds will be deposited into the account you gave shortly. 
Please read the terms and conditions that were emailed to you.
If rejected- Sorry, you do not match the criteria for a loan at this time, either save more or contact us.
For any further inquiry please contact us on:
Email - coopadmin@reincoso.com
        """

    recipient = request.user.email
    subject = "Loan processing status"

    send_email_using_mailgun(recipient, subject, body)


def loan_clear_off(request) -> None:
    body = f"""
        Dear {request.user.first_name},
            Congratulations! You have successfully cleared your loan of Nxxxxxx. Your loan balance is N0.00. 
            You can apply for more loans with us.
            For any further inquiry please contact us on:
            Email - coopadmin@reincoso.com
        """

    recipient = request.user.email
    subject = "Loan clear off"

    send_email_using_mailgun(recipient, subject, body)


def withdrawal_request_mail_user(request) -> None:
    body = f"""
        Dear {request.user.first_name},
            Your application to make a withdrawal of N{request.data.get("amount")} has been received and is being reviewed by the committee.
            You will be credited shortly.
            For any further inquiry please contact us on:
            Email - coopadmin@reincoso.com
        """

    recipient = request.user.email
    subject = "Withdraw Request"

    send_email_using_mailgun(recipient, subject, body)


def withdrawal_request_mail_admin(request, content) -> None:
    body = f"""
    Hi Reincoso,
        A withdrawal request of N{request.data.get("amount")} from {request.user.first_name} is currently
        waiting to be approved and disbursed.
        Kindly go through it and process as due.
        
    """

    recipient = settings.ADMIN_EMAIL
    subject = "Withdrawal Request"

    send_email_using_mailgun(recipient, subject, body)



