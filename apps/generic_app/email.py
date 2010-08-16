from django.conf import settings
from django.template import loader, Context
from django.core.mail import EmailMultiAlternatives
from generic_app.html2text import html2text


def send_html_mail(template_name, email_context, subject, recipients, sender=None, fail_silently=False):
    """
    This function will send a multi-part e-mail with both HTML and
    Text parts.

    template_name must be a HTML file and must contain .html extension.

    email_context should be a plain python dictionary. It is applied against
        both the email messages (templates) & the subject.

    subject can be plain text or a Django template string, eg:
        New Job: {{ job.id }} {{ job.title }}

    recipients can be either a string, eg 'a@b.com' or a list, eg:
        ['a@b.com', 'c@d.com']. Type conversion is done if needed.

    sender can be an e-mail, 'Name <email>' or None. If unspecified, the
        DEFAULT_FROM_EMAIL will be used.

    """
    if not sender:
        sender = settings.DEFAULT_FROM_EMAIL

    context = Context(email_context)

    html_part = loader.get_template(template_name).render(context)
    text_part = html2text(html_part)

    subject_part = loader.get_template_from_string(subject).render(context)

    if type(recipients) != list:
        recipients = [recipients,]

    msg = EmailMultiAlternatives(subject_part, text_part, sender, recipients)
    msg.attach_alternative(html_part, "text/html")
    return msg.send(fail_silently)
