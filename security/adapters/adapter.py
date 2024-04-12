
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context, subject=None):
        context['EMAIL_TO'] = email
        context['VERIFICATION_CODE'] = 983546
        context['BUSINESS_NAME'] = "No Business Name"

        msg = self.render_mail(template_prefix, email, context)
        subject = "Welcome to %s"

        if subject:
            msg.subject = subject

        msg.send()