from django.conf import settings
from generic_app.email import send_html_mail

from accounts.models import Profile, Batch

def send_birthday_greetings(profile,
                            template_name='greetings/birthday_greetings_email.html'):

    c = {'first_name' : profile.first_name,
         'orgnization' : settings.ORGANIZATION}
    subject = "Happy Birthday"

    to = []
    if profile.college_email_id:
        to.append(profile.college_email_id)

    if profile.personal_email_id:
        to.append(profile.personal_email_id)

    if profile.personal_email_id2:
        to.append(profile.personal_email_id2)

    if to:
        send_html_mail(template_name, c, subject, to)


def send_reminder_to_group(profile,
                           template_name='greetings/birthday_reminder_to_group.html'):

    try:
        batch = Batch.objects.get(course__exact=profile.course,
                                  year__exact=profile.year_of_joining)
    except Batch.DoesNotExist:
        return

    if batch.code.contains('staff'):
        return

    batch_email_id = '%s@%s' % (batch.code, settings.GOOGLE_APPS_DOMAIN)
    subject = "%s's Birthday Reminder" % profile.first_name

    c = {'first_name': profile.first_namefirst_name,
         'birth_day': profile.birth_day,
         'register_number': profile.register_number,
        }

    send_html_mail(template_name, c, subject, batch_email_id)

