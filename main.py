from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Store chat history
chat_history = []

# Function to get current date
def get_date():
    return datetime.now().strftime("%d-%m-%Y")

# Function to get current time
def get_time():
    return datetime.now().strftime("%I:%M %p")

# Function to get timestamp
def get_timestamp():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p")

# Chatbot response function
def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    if user_input in ["hi", "hello", "hey"]:
        return "Hello! How can I help you today?"

    elif user_input in ["what is your name", "your name", "who are you"]:
        return "I am RuleBot, a Rule-Based AI Chatbot created using Python."

    elif user_input in ["how are you", "how are you?"]:
        return "I am doing great! Thanks for asking."

    elif user_input in ["what can you do", "help", "features"]:
        return "I can greet you, answer simple questions, tell the current date and time, and store chat history."

    elif user_input in ["who created you", "who made you"]:
        return "I was created as a project using Python and rule-based logic."

    elif user_input in ["what is ai", "define ai", "artificial intelligence"]:
        return "Artificial Intelligence is the ability of machines to simulate human intelligence."

    elif user_input in ["what is python", "define python"]:
        return "Python is a popular high-level programming language used in AI, web development, automation, and more."

    elif user_input in ["what is this project", "about this project"]:
        return "This is a Rule-Based AI Chatbot project that gives predefined responses using if-else conditions."

    elif user_input in ["why are you created", "your purpose"]:
        return "My purpose is to simulate a simple human conversation using predefined rules."

    elif user_input in ["date", "today's date", "what is the date", "current date"]:
        return f"Today's date is {get_date()}."

    elif user_input in ["time", "current time", "what is the time", "tell me the time"]:
        return f"The current time is {get_time()}."

    elif user_input in ["day", "what day is today", "today"]:
        return f"Today is {datetime.now().strftime('%A')}."

    elif user_input in ["thank you", "thanks"]:
        return "You're welcome!"

    elif user_input in ["good morning", "good afternoon", "good evening"]:
        return "Wishing you a wonderful day!"

    elif user_input in ["bye", "exit", "quit"]:
        return "Goodbye! Have a nice day 😊"

    else:
        return "Sorry, I don't understand that. Please try asking something else."

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Get chatbot response
@app.route("/get", methods=["POST"])
def get_bot_response():
    user_input = request.form["msg"]
    bot_reply = chatbot_response(user_input)
    timestamp = get_timestamp()

    # Store user message
    chat_history.append({
        "sender": "You",
        "message": user_input,
        "timestamp": timestamp
    })

    # Store bot reply
    chat_history.append({
        "sender": "Bot",
        "message": bot_reply,
        "timestamp": timestamp
    })

    return jsonify({
        "response": bot_reply,
        "timestamp": timestamp
    })

# Return chat history
@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(chat_history)

# Clear chat history
@app.route("/clear", methods=["POST"])
def clear_history():
    chat_history.clear()
    return jsonify({"message": "Chat history cleared successfully!"})

if __name__ == "__main__":
    app.run(debug=True)