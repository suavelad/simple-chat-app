from chat_app.models import ChatHistory, ChatThread
from user.models import User


def save_chat_history(receive_data, user):

    message = receive_data.get("message", None)
    chat_id = receive_data.get("chat_id", None)
    receiver_user_id = receive_data.get("receiver_id", None)

    receiver_user = User.objects.filter(id=receiver_user_id).first()
    sender_user = user

    if receiver_user and sender_user:

        chat_thread, _ = ChatThread.objects.get_or_create(
            sender=sender_user, receiver=receiver_user
        )
        history = (
            ChatHistory()
            if chat_id == None
            else ChatHistory.objects.filter(id=int(chat_id)).first()
        )
        if history:
            history.sender = user
            history.receiver = receiver_user
            history.message = message
            history.thread = chat_thread

            if chat_id:
                history.is_edited = True
            history.save()

            return {
                "content": message,
                "chat_id": history.id,
                "thread_id": history.thread.id,
                "sender": {
                    "sender": f"{history.sender.first_name} {history.sender.last_name}",
                    "sender_id": history.sender.id,
                },
                "receiver": {
                    "receiver": f"{history.receiver.first_name} {history.receiver.last_name}",
                    "receiver_id": history.receiver.id,
                },
                "timestamp": str(history.date_created),
            }
        else:
            return None
    else:
        return None
