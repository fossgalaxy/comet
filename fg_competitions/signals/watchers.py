from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.conf import settings
from allauth.utils import build_absolute_uri

if "pinax.notifications" in settings.INSTALLED_APPS:
    from pinax.notifications import models as notification
else:
    notification = None

from fg_competitions.models import SubmissionUpload

@receiver(pre_save, sender=SubmissionUpload)
def onUploadChange(sender, **kwargs):
    obj = kwargs['instance']
    old = SubmissionUpload.objects.get(pk=obj.pk)

    # if the status didn't change we don't care
    if obj.status == old.status:
        return

    # if this was not a failure, we don't care
    if obj.status not in ("BF", "VF"):
        return

    # if the user doesn't have an email, we can't email them
    owner = obj.submission.owner
    if not owner.email:
        return

    context = {
        "upload": obj,
        "url": build_absolute_uri(None, obj.get_absolute_url())
    }

    if notification:
        notification.send([owner], "build_failure", context )

