from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Chatbot logic ---
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


# --- Simple state (for demo) ---
state = {
    "last_mood": None,
    "waiting_yes_no": False,
    "waiting_story": False,
    "waiting_exercise": False,
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    user_lower = user_message.lower().strip()

    if not user_message:
        return jsonify({"reply": "Please type something."})

    # Commands
    if user_lower == "help":
        return jsonify({"reply": "Commands: help, reset, exit"})

    if user_lower == "reset":
        state["last_mood"] = None
        state["waiting_yes_no"] = False
        state["waiting_story"] = False
        state["waiting_exercise"] = False
        return jsonify({"reply": "Reset done. You can start again."})

    if user_lower == "exit":
        return jsonify({"reply": "Take care. You are not alone."})

    # Exercise stage
    if state["waiting_exercise"] and state["last_mood"] is not None:
        yes_list = ["yes", "y", "yeah", "ok", "okay", "sure"]
        no_list = ["no", "n", "not now", "nope"]

        if user_lower in yes_list:
            reply = get_calming_exercise(state["last_mood"])
            state["waiting_exercise"] = False
            return jsonify({"reply": reply})

        if user_lower in no_list:
            state["waiting_exercise"] = False
            return jsonify({"reply": "No problem. I'm here for you. Tell me more if you want."})

        return jsonify({"reply": "Please reply with yes or no."})

    # Story stage
    if state["waiting_story"] and state["last_mood"] is not None:
        state["waiting_story"] = False
        state["waiting_exercise"] = True
        return jsonify(
            {
                "reply": "Thank you for sharing. That sounds difficult. You are doing your best. Do you want a small calming exercise? (yes/no)"
            }
        )

    # Yes/No stage
    if state["waiting_yes_no"] and state["last_mood"] is not None:
        reply = handle_yes_no(state["last_mood"], user_message)
        state["waiting_yes_no"] = False

        yes_list = ["yes", "y", "yeah", "ok", "okay", "sure"]
        if user_lower in yes_list and state["last_mood"] in ["sad", "lonely"]:
            state["waiting_story"] = True

        return jsonify({"reply": reply})

    # Normal mood detection
    mood = detect_mood(user_message)
    state["last_mood"] = mood

    reply = get_support_response(mood)
    if "(yes/no)" in reply:
        state["waiting_yes_no"] = True

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
