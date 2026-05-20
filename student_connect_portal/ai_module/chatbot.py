def chatbot_reply(message):
    message = message.lower()

    if message.startswith("translate hindi:"):
        text = message.replace("translate hindi:", "").strip()
        return "हिंदी अनुवाद: " + text

    if "exam" in message:
        return "Exam related notices are available in the Notices section."

    elif "fee" in message or "fees" in message:
        return "Fee details will be shared through official notices."

    elif "grievance" in message:
        return "You can submit a grievance using the form on this page."

    elif "contact" in message:
        return "Please contact the college administration office."

    elif "hello" in message or "hi" in message:
        return "Hello! How can I help you today?"
    
    elif "what is your name" in message or "your name" in message:
        return "I am the Student Connect Portal AI assistant."

    else:
        return "Sorry, I can help with exams, fees, grievances, or translation."
    
