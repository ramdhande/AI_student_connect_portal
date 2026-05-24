def chatbot_reply(message):
    message = message.lower().strip()
    
    # Custom keyword weights and synonyms
    exam_words = ["exam", "examination", "midterm", "test", "timetable", "schedule", "grade", "marks", "result"]
    fee_words = ["fee", "fees", "payment", "due", "tuition", "fine", "scholarship"]
    grievance_words = ["grievance", "complain", "complaint", "issue", "problem", "report", "harassment"]
    contact_words = ["contact", "office", "phone", "number", "email", "support", "helpdesk", "admin"]
    hello_words = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"]
    
    # Guest, Parent and New User Synonyms
    parent_words = ["parent", "mother", "father", "guardian", "child", "son", "daughter", "ward"]
    register_words = ["register", "signup", "create account", "new user", "how to login", "sign up"]
    admission_words = ["admission", "intake", "courses", "stream", "branches"]
    
    if any(w in message for w in hello_words):
        return "Hello there! I am the Student Connect AI Assistant. How can I guide you today? You can ask about exams, college fees, filing a grievance, registrations, or parent services."
        
    elif any(w in message for w in parent_words):
        return "👨‍👩‍👧‍👦 **Parent Portal Guide:** As a parent or guardian, you can stay informed by reading campus announcements under the Notices Board. If you wish to track specific grievances submitted by your ward, please log in with your designated parent account, or consult our administration office at parent-support@college.edu."
        
    elif any(w in message for w in register_words):
        return "📝 **How to Register:** If you are a new student, click **'Create an account'** on the Sign In page. You must enter your verified **Student ID** and registered **college email** to link with institutional records. If you receive an error, contact the Admin registrar's office."
        
    elif any(w in message for w in admission_words):
        return "🎓 **Admissions & Streams:** Our college offers premier 4-year engineering branches in **Computer Engineering, Information Technology, and AI & Data Science**. For intake deadlines and syllabus information, contact admissions@college.edu."
        
    elif any(w in message for w in exam_words):
        return "📅 **Exam Info:** Midterm and final exam announcements, schedules, and grading standards are automatically posted in the **Notices** section. You can filter notices by clicking the **'Academic'** tag."
        
    elif any(w in message for w in fee_words):
        return "💰 **Fee Inquiries:** Official fee structures, payment deadlines, and bank details are shared directly on the Notice Board under the **'Administrative'** category. To avoid penalty, complete all clearances on time."
        
    elif any(w in message for w in grievance_words):
        return "📝 **Submit a Grievance:** You can file a formal complaint using the **'Submit Grievance'** widget. Our AI system will automatically detect the sentiment and urgency to assign an appropriate priority level (High/Medium/Low) so the college administration can resolve it quickly."
        
    elif any(w in message for w in contact_words):
        return "📞 **Contact Administration:** You can reach out directly to the college helpdesk at **admin@college.edu** or visit the Administrative Office between 10:00 AM and 4:00 PM."
        
    elif "name" in message:
        return "🤖 I am the **Student Connect AI Support Assistant**, built to help you navigate notices and manage your campus grievances efficiently!"
        
    elif message.startswith("translate "):
        parts = message.split(":", 1)
        if len(parts) == 2:
            lang_part = parts[0].replace("translate", "").strip()
            text_part = parts[1].strip()
            from .translation import translate_text
            return f"Translated ({lang_part.capitalize()}): " + translate_text(text_part, lang_part)
        else:
            return "To translate a custom phrase, use the format: **translate <language>: <text>** (e.g., *translate hindi: All students must complete their fee clearance.*)"
            
    else:
        return "I'm sorry, I couldn't fully map that question. You can ask me about **exams, fees, filing grievances**, or use my translation services (e.g., *'translate hindi: College remains closed'*)."
    
