
# Emails in django are a pain, use allauth to send it.
from allauth.account.adapter import get_adapter
from allauth.utils import build_absolute_uri

def emailBuildFailure(owner, upload):
    """Report a failure to build an agent to it's owner"""
    adapter = get_adapter()

    context = {
        "owner": owner,
        "upload": upload,
        "url": build_absolute_uri(None, upload.get_absolute_url())
    }

    adapter.send_mail('fg_competitions/email/failure', owner.email, context)

