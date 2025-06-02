from .models import History

def save_message(sender_user, receiver_user, msg_text):
    History.objects.create(
        sender=sender_user,
        receiver=receiver_user,
        message=msg_text
    )
