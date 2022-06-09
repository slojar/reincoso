import profile
import requests
import logging
from re import A
from django.conf import settings
from investment.models import InvestmentTransaction, UserInvestment
from loan.models import Loan, LoanTransaction

from savings.models import Saving
from .models import Profile, Wallet
import json
from humanize import intcomma

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

Reincoso Cooperative Society welcomes you! 

We're thrilled to have you among us. We consider ourselves fortunate that you picked us and I'd want to express 
our gratitude on behalf of the whole organization.

In the meanwhile, please visit our website (www.reincosocoop.com) 
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
    subject = "Reincoso Membership"

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
    body = f"""
Dear {profile.user.first_name},   
 
Thank you for using Reincoso Quick Save option.Your quick save of N{intcomma(amount, 2)} is successful.
Your current balance is N{intcomma(balance, 2)}.
    """
    recipient = profile.user.email
    subject = "Successful Quick Save"

    send_email_using_mailgun(recipient, subject, body)


def failed_quick_save_mail(profile, amount) -> None:
    balance = Wallet.objects.get(user=profile)
    body = f"""
Dear {profile.user.first_name},

Your Quick Save option of N{intcomma(amount, 2)} is NOT successful (due to insufficient bank balance or network issues). 
Kindly try again or contact us on coopadmin@reincoso.com. If the problem presides, please contact your bank
        """

    recipient = profile.user.email
    subject = "Failed Quick Save"

    send_email_using_mailgun(recipient, subject, body)


# Opt into Automated Savings ?? I haven't figured out the point where user opts into Auto_Save plan
def auto_save_creation_mail(profile, saving) -> None:
    body = f"""
    Dear {profile.user.first_name},
        You have successfully opted for our {saving.duration} Auto save plan. 
        For any further inquiry, please contact us on:
        Email - coopadmin@reincoso.com
    """

    recipient = profile.user.email
    subject = "Reincoso Savings"

    send_email_using_mailgun(recipient, subject, body)


def successful_auto_save_mail(profile, amount) -> None:
    balance = Wallet.objects.get(user=profile).balance
    body = f"""
Dear {profile.user.first_name},

Thank you for using Reincoso Auto Save option. Your Auto save of N{intcomma(amount.amount, 2)} {amount.duration}
plan is successful. Your current balance is N{intcomma(balance, 2)}.

For any further inquiry, please contact us on:
Email - coopadmin@reincoso.com
    """

    recipient = profile.user.email
    subject = "Success Auto Save"

    send_email_using_mailgun(recipient, subject, body)


def failed_auto_save_mail(profile, amount) -> None:
    body = f"""
Dear {profile.user.first_name},

Your Auto Save option of N{intcomma(amount.amount, 2)} {amount.duration} plan is NOT successful (due to insufficient bank balance or network issues).
Kindly try again or contact us on coopadmin@reincoso.com. 
If the problem presides, please contact your bank.
        """

    recipient = profile.user.email
    subject = "Failed Auto Save"

    send_email_using_mailgun(recipient, subject, body)


#   DONE
def awaiting_investment_approval_mail(request):
    body = f"""
Dear {request.user.first_name},

Your investment request has been received and is being reviewed by the investment committee. 
You will be notified as soon as your investment is approved.
For any further inquiry please contact us on:
Email - coopadmin@reincoso.com
    """
    recipient = request.user.email
    subject = "Investment with Reincoso"
    send_email_using_mailgun(recipient=recipient, subject=subject, message=body)


#   DONE
def investment_notification_to_admin(request, investment_transaction):
    body = f"""
Hi Reincoso,

The investment amount of {intcomma(investment_transaction.amount, 2)} in {investment_transaction.user_investment.investment.name} 
with {investment_transaction.user_investment.percentage}% per annum from {request.user.first_name} is currently waiting 
to be reviewed and approved. Kindly go through it and process as due.
"""

    recipient = "coopadmin@reincoso.com"
    subject = "Reincoso Investment Request"
    send_email_using_mailgun(recipient=recipient, subject=subject, message=body)


#   Done
def approved_investment_mail(user_investment):
    all_investment_transaction = UserInvestment.objects.filter(user=user_investment.user)
    total_amount_invested: int = 0
    total_amount_invested = sum(
        [total_amount_invested + amount.amount_invested for amount in all_investment_transaction]
    )
    body = f"""
Dear {user_investment.user.user.first_name},

Your investment of N{intcomma(user_investment.amount_invested, 2)} on {user_investment.investment.name} with {user_investment.percentage}% per annum has been approved.
Your current investment balance is N{intcomma(total_amount_invested, 2)}.

For any further inquiry, please contact us on:
Email - coopadmin@reincoso.com
    """

    recipient = user_investment.user.user.email
    subject = "Investment with Reincoso"
    send_email_using_mailgun(recipient=recipient, subject=subject, message=body)


#   Done
def declined_investment_mail(user_investment):
    body = f"""
Dear {user_investment.user.user.first_name},

Your investment of N{intcomma(user_investment.amount_invested, 2)} on {user_investment.investment.name} with 
{user_investment.percentage}% per annum has been declined at this moment.

For any further inquiry, please contact us on:
Email - coopadmin@reincoso.com
"""

    recipient = user_investment.user.user.email
    subject = "Investment with Reincoso"
    send_email_using_mailgun(recipient=recipient, subject=subject, message=body)


def successful_investment_mail(request, investment_transaction, total_amount_invested) -> None:
    body = f"""
Dear {request.user.first_name},

You have made an investment of {intcomma(investment_transaction.amount, 2)} on {investment_transaction.user_investment.investment.name} 
with {investment_transaction.user_investment.percentage}% per annum.
Your current investment balance is N{intcomma(total_amount_invested, 2)}.

For any further inquiry, please contact us on:
Email - coopadmin@reincoso.com
"""

    recipient = request.user.email
    subject = "Investment with Reincoso"
    send_email_using_mailgun(recipient, subject, body)


def failed_investment_mail(request, investment_transaction) -> None:
    body = f"""
Dear {request.user.first_name},

Your Investment of N{intcomma(investment_transaction.amount, 2)} on {investment_transaction.user_investment.investment.name} 
is NOT successful (due to insufficient bank balance or network issues). 

Kindly try again or contact us on coopadmin@reincoso.com. If the problem presides, please contact your bank
"""

    recipient = request.user.email
    subject = "Investment with Reincoso"

    send_email_using_mailgun(recipient, subject, body)

# Confirm this page
def investment_maturity_mail(request) -> None:
    balance = Wallet.objects.get(user=request.user).balance
    body = f"""
        Dear {request.user.first_name},
        We are pleased to notify you that your Nxxxx investment in (Real estate/P2P/Agriculture/Fixed income) has matured and interest will be paid to you shortly. 
        For any further inquiry please contact us on:
        Email - coopadmin@reincoso.com
    """

    recipient = request.user.email
    subject = "Investment with Reincoso"

    send_email_using_mailgun(recipient, subject, body)


def loan_request_processing_mail(request) -> None:
    body = f"""
Dear {request.user.first_name},

Your loan application has been received and is being reviewed by the loan committee.\n
Your loan will be disbursed as soon as all requirements are met.

For any further inquiry please contact us on:
Email - coopadmin@reincoso.com

"""

    recipient = request.user.email
    subject = "Reincoso Loan Request"

    send_email_using_mailgun(recipient, subject, body)


def store_template(body, template_name):

    response = requests.post(url="https://api.mailgun.net/v3/reincosocoop.com/templates", auth=("api", api_key),
                             data={'template': body, 'name': template_name,
                                   'description': "Reincoso Guarantor Request"})
    return response.text


def mail_to_guarantor(request, guarantor):
    """
        Info: This function sends mail to guarantor, to accept or decline the request.
        info: store_template(body, template_name="mail_to_guarantor1.html") this function is responsible for adding
        a template to mailgun, the official template used for sending the mail to the guarantor is
        named 'mail_to_guarantor1.html' this can be changed from the store_template() and once changed in this function it
        should be updated in the data['template'] of this function.
    """
    profile = Profile.objects.get(user=request.user)
    loan = LoanTransaction.objects.filter(user=profile).last()

    body = """
        <div class='entry' style='color:black'>
                Dear {{ name }},<br><br>
                
                You have been selected to guarantee for the loan amount of N{{ loan_amount }} for {{ guarantee_name }} and you will 
                be held liable if the debts are not repaid. You can Accept or Reject this offer of Guarantorship through this link
                <a href='{{ request_scheme }}://{{ request_host_name }}/confirm-guarantorship/?guarantor={{ guarantor_phone_number }}&guarantee={{ guarantee_phone_number }}'>Click Here</a>.<br> <br>
                For any further inquiry please contact us on:
                Email - coopadmin@reincoso.com
        </div>
    """

    subject = "Reincoso Guarantor Request"
    return requests.post("https://api.mailgun.net/v3/reincosocoop.com/messages", auth=("api", api_key), data={
        "from": "Reincoso <no-reply@reincosocoop.com>", "to": [guarantor.user.email], "subject": subject,
        "template": "mail_to_guarantor1.html", "t:variables": json.dumps({"name": guarantor.user.first_name,
                                                                          "loan_amount": str(intcomma(loan.amount, 2)),
                                                                          "guarantee_name": request.user.first_name,
                                                                          "request_scheme": request.scheme,
                                                                          "request_host_name": request.get_host(),
                                                                          "guarantor_phone_number": guarantor.phone_number,
                                                                          "guarantee_phone_number": profile.phone_number})
    })


def guarantor_accept_mail(user, guarantor) -> None:
    body = f"""
Dear {user.first_name}, 

{guarantor} has Accepted to be your Guarantor.

For any further inquiry please contact us on:
Email - coopadmin@reincoso.com
"""
    subject = "Reincoso Guarantor Accepted"

    send_email_using_mailgun(recipient=user.email, subject=subject, message=body)


def guarantor_declined_mail(user, guarantor) -> None:
    body = f"""
Dear {user.first_name}, 
    
{guarantor} has Declined to be your Guarantor.

For any further inquiry please contact us on:
Email - coopadmin@reincoso.com
"""

    subject = "Reincoso Guarantor Declined"

    send_email_using_mailgun(recipient=user.email, subject=subject, message=body)


def inform_user_of_added_guarantor(request) -> None:
    profile = Profile.objects.get(user=request.user)

    loan = LoanTransaction.objects.filter(user=profile).last()
    guarantor = ", ".join(list(request.data.get("guarantor")))
    body = f"""
Dear {request.user.first_name},

You have added {guarantor} as your guarantor(s) for the loan amount of N{intcomma(loan.amount, 2)}
For any further inquiry please contact us on:
Email - coopadmin@reincoso.com
"""

    recipient = request.user.email
    subject = "Guarantor Added"

    send_email_using_mailgun(recipient, subject, body)


def admin_loan_processing_status_mail(request) -> None:
    body = f"""
Dear Reincoso,

The loan amount of N{intcomma(request.data.get("amount"), 2)} from {request.user.first_name} is currently waiting to be reviewed and approved. 
Kindly go through it and process as due.
        """

    recipient = request.user.email
    subject = "Loan processing status"

    send_email_using_mailgun(recipient, subject, body)

# This hasn't been implemented
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


def loan_clear_off(request, loan) -> None:
    body = f"""
Dear {request.user.first_name},

Congratulations! You have successfully cleared your loan of N{intcomma(loan.amount)}. Your loan balance is N0.00. 
You can apply for more loans with us.

For any further inquiry please contact us on:
Email - coopadmin@reincoso.com
"""

    recipient = request.user.email
    subject = "Reincoso Loan Repayment"

    send_email_using_mailgun(recipient, subject, body)


def withdrawal_request_mail_user(request) -> None:
    body = f"""
        Dear {request.user.first_name},
        
        Your application to make a withdrawal of N{intcomma(request.data.get("amount"))} has been received and is being reviewed by the committee.
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

A withdrawal request of N{intcomma(request.data.get("amount"), 2)} from {request.user.first_name} is currently
waiting to be approved and disbursed. Kindly go through it and process as due.
"""

    recipient = settings.ADMIN_EMAIL
    subject = "Withdrawal Request"

    send_email_using_mailgun(recipient, subject, body)
