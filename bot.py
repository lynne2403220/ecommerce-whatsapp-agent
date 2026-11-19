
import queue
import threading
import time

from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv
from neonize import extract_text

from agent import run_agent


client = NewClient("whatsapp_session.db")

message_queue = queue.Queue()
REQUEST_DELAY_SECONDS = 3

# Record when this bot starts.
# Messages sent before this time will be ignored.
BOT_START_TIME = int(time.time())

# Only this WhatsApp group is allowed.
ALLOWED_GROUP_ID = "120363143145485008@g.us"


def process_messages():
    while True:
        customer_id, user_message, message = message_queue.get()

        try:
            print(f"Processing message from {customer_id}")

            response = run_agent(
                user_message,
                session_id=customer_id
            )

            client.reply_message(response, message)

            print(f"Reply sent to {customer_id}")

        except Exception as error:
            print(f"Message processing error: {error}")

        finally:
            message_queue.task_done()
            time.sleep(REQUEST_DELAY_SECONDS)


@client.event(ConnectedEv)
def on_connected(client, event):
    print("WhatsApp connected successfully!")
    print("Ignoring messages sent before bot startup.")


@client.event(MessageEv)
def on_message(client, message):
    try:
        source = message.Info.MessageSource

        # Ignore messages sent by this WhatsApp account.
        if source.IsFromMe:
            return

        # Check when the message was originally sent.
        message_timestamp = int(message.Info.Timestamp)

        # Handle timestamps expressed in milliseconds, if encountered.
        if message_timestamp > 100000000000:
            message_timestamp //= 1000

        # Ignore old messages.
        if message_timestamp < BOT_START_TIME:
            print("Old message ignored.")
            return

        # Allow only the approved group.
        if source.IsGroup:
            group_id = (
                f"{source.Chat.User}@{source.Chat.Server}"
            )

            if group_id != ALLOWED_GROUP_ID:
                return

            customer_id = ALLOWED_GROUP_ID

        else:
            # Allow new private messages.
            customer_id = str(source.Sender.User)

        user_message = extract_text(message.Message)

        if not user_message or not user_message.strip():
            return

        message_queue.put(
            (customer_id, user_message, message)
        )

        print(f"New message queued from {customer_id}")

    except Exception as error:
        print(f"Message handling error: {error}")


worker = threading.Thread(
    target=process_messages,
    daemon=True
)
worker.start()


print("Starting E-Commerce WhatsApp AI Agent...")
print("Allowed group: El bash Mohandeseen")
print("New private messages: ENABLED")
print("Old messages: IGNORED")
print("Other groups: BLOCKED")
print("Scan the QR code with WhatsApp if requested.")

client.connect()
