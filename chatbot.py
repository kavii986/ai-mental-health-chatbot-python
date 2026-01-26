print("Welcome to Mental Health Support Chatbot")
print("Type 'exit' to stop")

while True:
    user_message = input("You: ")

    if user_message.lower() == "exit":
        print("Bot: Take care. You are not alone.")
        break

    if "sad" in user_message.lower():
        print("Bot: I'm sorry you're feeling sad. Do you want to talk about it?")
    elif "stress" in user_message.lower():
        print("Bot: Stress can be tough. Try taking a deep breath slowly.")
    elif "anxiety" in user_message.lower():
        print("Bot: Anxiety is difficult. You can try 4-7-8 breathing.")
    else:
        print("Bot: I understand. Tell me more.")
