from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_user(username: str, message: str, data: dict) -> bool:
    """
    Notify a user with a given message and data.

    Args:
        username (str): The username of the user to notify.
        message (str): The message to send to the user.
        data (dict): The data to send to the user. It should have a 'mode' key and a 'data' key.

    Returns:
        bool: True if the notification was sent successfully, False otherwise.
    """
    try:
        channel_layer = get_channel_layer()
        # Specify the user ID to send the notification to
        to_user_id = username
        print(f"SENDING NOTIFICATION TO: {to_user_id}")
        print(f"Request DATA -> {data}")

        async_to_sync(channel_layer.group_send)(
            f"user_{to_user_id}",
            {
                "type": "send_notification",
                "message": message,
                "data": {"mode": data['mode'],"data": data['data']}
            }
        )
        return True
    except Exception as e:
        print(e)
        return False