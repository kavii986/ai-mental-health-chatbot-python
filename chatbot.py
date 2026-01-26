def detect_mood(message: str) -> str:
    msg = message.lower()

    if "sad" in msg or "depressed" in msg or "cry" in msg:
        return "sad"
    if "stress" in msg or "tension" in msg or "pressure" in msg:
        return "stress"
    if "anxiety" in msg or "panic" in msg or "fear" in msg:
        return "anxiety"
    if "lonely" in msg or "alone" in msg:
        return "lonely"
    if "angry" in msg or "mad" in msg or "irritated" in msg:
        return "angry"

    return "normal"


def get_support_response(mood: str) -> str:
    if mood == "sad":
        return "I'm sorry you're feeling sad. Do you want to talk about it? (yes/no)"
    if mood == "stress":
        return "Stress can be tough. Do you want a quick breathing tip? (yes/no)"
    if mood == "anxiety":
        return "Anxiety can feel overwhelming. Do you want a calming exercise? (yes/no)"
    if mood == "lonely":
        return "Feeling lonely is hard. Do you want to share what you're going through? (yes/no)"
    if mood == "angry":
        return "It's okay to feel angry. Do you want a simple calming method? (yes/no)"

    return "I understand. Tell me more."


def get_calming_exercise(mood: str) -> str:
    if mood == "sad":
        return "Try this: Take 5 slow breaths. Inhale 4 seconds, exhale 4 seconds. Repeat 3 times."
    if mood == "stress":
        return "Box breathing: inhale 4, hold 4, exhale 4, hold 4. Repeat 3 times."
    if mood == "anxiety":
        return "4-7-8 breathing: inhale 4, hold 7, exhale 8. Repeat 3 times."
    if mood == "lonely":
        return "Grounding: Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste."
    if mood == "angry":
        return "Pause: take 10 deep breaths and relax your shoulders. Drink water slowly."

    return "Take a deep breath and give yourself a moment."


def handle_yes_no(mood: str, user_reply: str) -> str:
    reply = user_reply.lower().strip()

    yes_list = ["yes", "y", "yeah", "ok", "okay", "sure"]
    no_list = ["no", "n", "not now", "nope"]

    if reply in yes_list:
        if mood == "sad":
            return "I'm here for you. What made you feel sad today?"
        if mood == "stress":
            return "Try this: inhale 4 seconds, hold 4 seconds, exhale 4 seconds. Repeat 3 times."
        if mood == "anxiety":
            return "Try 4-7-8 breathing: inhale 4, hold 7, exhale 8. Repeat 3 times."
        if mood == "lonely":
            return "You’re not alone. Would you like to talk to someone you trust today?"
        if mood == "angry":
            return "Pause and take 5 slow breaths. Then drink water. Do you feel a little better?"

    if reply in no_list:
        return "That's okay. I'm here whenever you're ready. Tell me anything you want."

    return "Please reply with yes or no."


def print_help():
    print("Bot: Available commands:")
    print("Bot: 1) help  - show commands")
    print("Bot: 2) reset - start a fresh conversation")
    print("Bot: 3) exit  - close the chatbot")


def main():
    print("Welcome to Mental Health Support Chatbot")
    print("Type 'help' for commands | Type 'exit' to stop")

    last_mood = None

    waiting_yes_no = False
    waiting_story = False
    waiting_exercise = False

    yes_list = ["yes", "y", "yeah", "ok", "okay", "sure"]
    no_list = ["no", "n", "not now", "nope"]

    while True:
        user_message = input("You: ").strip()
        user_lower = user_message.lower().strip()

        # Commands
        if user_lower == "exit":
            print("Bot: Take care. You are not alone.")
            break

        if user_lower == "help":
            print_help()
            continue

        if user_lower == "reset":
            last_mood = None
            waiting_yes_no = False
            waiting_story = False
            waiting_exercise = False
            print("Bot: Reset done. You can start again.")
            continue

        # If bot asked exercise yes/no
        if waiting_exercise and last_mood is not None:
            if user_lower in yes_list:
                print("Bot:", get_calming_exercise(last_mood))
                print("Bot: I hope that helps a little. You can talk to me anytime.")
                waiting_exercise = False
                continue
            elif user_lower in no_list:
                print("Bot: No problem. I'm here for you. Tell me more if you want.")
                waiting_exercise = False
                continue
            else:
                print("Bot: Please reply with yes or no.")
                continue

        # If user is sharing the reason/story after bot asked
        if waiting_story and last_mood is not None:
            print("Bot: Thank you for sharing. That sounds difficult. You are doing your best.")
            print("Bot: Do you want a small calming exercise? (yes/no)")
            waiting_story = False
            waiting_exercise = True
            continue

        # If bot asked yes/no previously
        if waiting_yes_no and last_mood is not None:
            bot_reply = handle_yes_no(last_mood, user_message)
            print("Bot:", bot_reply)

            # If user said yes, next message will be their story/reason (only for sad/lonely)
            if user_lower in yes_list and last_mood in ["sad", "lonely"]:
                waiting_story = True

            waiting_yes_no = False
            continue

        # Detect mood from current message
        mood = detect_mood(user_message)
        last_mood = mood

        response = get_support_response(mood)
        print("Bot:", response)

        # If response expects yes/no
        if "(yes/no)" in response:
            waiting_yes_no = True


if __name__ == "__main__":
    main()
