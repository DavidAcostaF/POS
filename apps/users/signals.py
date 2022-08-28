from django.db.models.signals import post_save
from django.conf import settings
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import get_template
from django.template.loader import render_to_string
import uuid


from .models import MyUser

def AddUuid(sender,instance,**kwargs):
    print('si')
    if instance.uuid == None:
        uid = str(uuid.uuid4())[:10]
        instance.uuid = uid
        print(uid)
        instance.save()
        template = render_to_string('mails/activate.html',{
            'uid':uid
        })
        context = {
            'uid':uid
        }
        #content = template.render(context)
        mail = EmailMultiAlternatives(
        'Activate account',
        template,
        from_email=settings.EMAIL_HOST_USER,
        to=[instance.email],
        )
        mail.fail_silently = False
        mail.attach_alternative(template,'text/html')
        mail.send()
        

post_save.connect(AddUuid,sender = MyUser)