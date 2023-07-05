
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
# from estores import settings




def SendEmail(subject:str, email_to:str, context:dict, template:str):
    try:

        subject = f'subject'
        html_message = render_to_string(template, context)
        plain_message = strip_tags(html_message)
        send_mail(
        subject,
        plain_message, 
        f"EzyThrift <{settings.DEFAULT_FROM_EMAIL}>",
        [email_to], 
        html_message=html_message, 
    )
        return {"status":200}
    except Exception as e:
        print(e)
        return {"status":400}
    

