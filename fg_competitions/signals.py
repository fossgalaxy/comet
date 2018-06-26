from django.db.models.signals import pre_save
from django.dispatch import receiver

from . import tools
from .models import SubmissionUpload

print("signal file loaded")

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

    tools.emailBuildFailure(owner, obj) 
