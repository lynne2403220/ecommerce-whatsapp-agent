
from agent import run_agent

SESSION_ID = "terminal-test"

print("E-Commerce AI Assistant")
print("Type 'exit' to end the conversation.")
print("-----------------------------------")

while True:
    user_message = input("You: ").strip()

    if user_message.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    if not user_message:
        continue

    response = run_agent(user_message, session_id=SESSION_ID)

    print("Agent:", response)
    print()
