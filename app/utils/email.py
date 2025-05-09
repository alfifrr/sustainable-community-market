from flask_mail import Message
from flask import current_app, render_template
from app import mail


def send_activation_email(user, activation_url):
    msg = Message(
        subject="Activate your account",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=["ilugaaveresi@gmail.com"],
    )
    msg.html = render_template(
        "email/activation.html", user=user, activation_url=activation_url
    )

    msg.body = f"""Hello {user.first_name},

    You are now trying to activate your account as,
    Username: {user.username}
    Email: {user.email}
    Phone number: {user.phone_number}
    
    Please activate your account by clicking the following link:
    {activation_url}
    
    If you did not create this account, please ignore this email.
    """
    mail.send(msg)


def send_newsletter_email(email, explore_url, unsubscribe_url):
    msg = Message(
        subject="Sustainable Community Market Newsletter",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[email],
    )
    msg.html = render_template(
        "email/newsletter.html", explore_url=explore_url, unsubscribe_url=unsubscribe_url
    )
    mail.send(msg)
