from accounts.models import StudentProfile, ParentProfile, StudentProgress, Attendance
from notices.models import Notice
from grievances.models import Grievance

def chatbot_reply(message, request=None):
    message = message.lower().strip()
    
    # 1. Check if user is authenticated and get context
    user = None
    if request and request.user and request.user.is_authenticated:
        user = request.user

    # 2. Database Queries triggered by keywords
    
    # Keyword Lists
    grade_words = ["grade", "marks", "result", "sgpa", "cgpa", "score", "progress", "performance", "academic"]
    attendance_words = ["attendance", "present", "absent", "lectures", "eligible"]
    grievance_words = ["grievance", "complain", "complaint", "status", "issue"]
    notice_words = ["notice", "bulletin", "announcement", "circular", "latest news", "what's new"]
    hello_words = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"]
    help_words = ["help", "what can you do", "options", "commands", "menu"]

    # --- COMMAND: HELP MENU ---
    if any(w in message for w in help_words):
        if user:
            role_specific_help = ""
            if user.role == 'student':
                role_specific_help = "\n• **Grades**: Ask *'what are my grades?'* or *'show my scores'*.\n• **Attendance**: Ask *'what is my attendance?'*.\n• **Grievances**: Ask *'check my grievances'*."
            elif user.role == 'parent':
                role_specific_help = "\n• **Grades**: Ask *'how is my child performing?'* or *'what are my child's grades?'*.\n• **Attendance**: Ask *'what is my child's attendance?'*."
            
            return f"🤖 **AI Helpdesk Assistant Menu:**\n\nYou are logged in as a **{user.role.capitalize()}**.{role_specific_help}\n• **Notices**: Ask *'show recent notices'* to see the latest bulletins.\n• **Translation**: Ask *'translate <language>: <phrase>'* (e.g. *'translate marathi: School opens on Monday'*).\n• **Q&A**: Ask about admissions, fee structures, or campus contacts."
        else:
            return "🤖 **AI Helpdesk Assistant Menu:**\n\nYou are visiting as a Guest. You can:\n• Ask about college admissions (e.g. *'what courses do you offer?'*)\n• Ask about administrative contacts (*'how to contact the admin'*)\n• Ask about account registration guides (*'how to register'*)\n• Use translation services (*'translate hindi: Good Morning'*)\n\n*Tip: Login to access your dynamic grades and attendance details.*"

    # --- Hello Greetings ---
    if any(w in message for w in hello_words):
        name = user.first_name if (user and user.first_name) else (user.username if user else "there")
        greeting = f"Hello {name}! I am the Student Connect AI Assistant. How can I guide you today? "
        if user:
            greeting += f"You can ask about exams, attendance registers, notice updates, or grievances."
        else:
            greeting += "You can ask about admissions, contact information, or how to register an account."
        return greeting

    # --- DYNAMIC: GRADES & PERFORMANCE ---
    if any(w in message for w in grade_words):
        if not user:
            return "🔑 Please sign in to your student or parent account to inspect midterm marks, SGPA tracks, and evaluation grades."
        
        if user.role == 'student':
            if not hasattr(user, 'student_profile') or not user.student_profile:
                return "⚠ No verified student profile links detected for this account. Please coordinate with the campus registrar."
            
            records = StudentProgress.objects.filter(student=user.student_profile)
            if not records.exists():
                return "🎓 Your midterm grading scores have not been entered into the registry database yet."
            
            reply = f"📊 **Your Midterm Performance Summary ({user.student_profile.full_name}):**\n"
            for r in records:
                reply += f"\n• **{r.subject}**: Marks: **{r.marks}/100** | Grade: **{r.grade}** (Semester {r.semester})"
            return reply
            
        elif user.role == 'parent':
            student_id = request.session.get('linked_student_id')
            if not student_id:
                return "🔗 You have not linked your parent account to a student profile yet. Please complete linkage on the dashboard first."
            
            profile = StudentProfile.objects.filter(student_id=student_id).first()
            if not profile:
                return "⚠ Linked student record not found."
            
            records = StudentProgress.objects.filter(student=profile)
            if not records.exists():
                return f"🎓 Academic marks for your child **{profile.full_name}** are not seeded yet."
            
            reply = f"📊 **Child's Academic Performance Review ({profile.full_name}):**\n"
            for r in records:
                reply += f"\n• **{r.subject}**: Marks: **{r.marks}/100** | Grade: **{r.grade}**"
            return reply
            
        elif user.role in ['teacher', 'admin']:
            return "👨‍🏫 Faculty Desk: To inspect or update student grades, please use the **Student Manager Registry** pane on your dashboard."

    # --- DYNAMIC: ATTENDANCE ---
    if any(w in message for w in attendance_words):
        if not user:
            return "🔑 Sign in to track class lecture attendances and eligibility details."
            
        if user.role == 'student':
            if not hasattr(user, 'student_profile') or not user.student_profile:
                return "⚠ Student profile not found."
            
            records = Attendance.objects.filter(student=user.student_profile)
            if not records.exists():
                return "📅 No attendance registers configured for your account yet."
            
            reply = f"📝 **Your Lecture Attendance Status ({user.student_profile.full_name}):**\n"
            for r in records:
                status = "✓ Eligible" if r.percentage >= 75 else "⚠ Shortage"
                reply += f"\n• **{r.subject}**: **{r.percentage}%** ({r.classes_attended}/{r.total_classes} lectures) — *{status}*"
            return reply
            
        elif user.role == 'parent':
            student_id = request.session.get('linked_student_id')
            if not student_id:
                return "🔗 Please link your parent profile to a student ID to track attendance."
                
            profile = StudentProfile.objects.filter(student_id=student_id).first()
            if not profile:
                return "⚠ Student profile record not found."
                
            records = Attendance.objects.filter(student=profile)
            if not records.exists():
                return f"📅 Attendance records for **{profile.full_name}** are not registered yet."
                
            reply = f"📝 **Child's Class Attendance Summary ({profile.full_name}):**\n"
            for r in records:
                status = "Eligible" if r.percentage >= 75 else "Shortage (Below 75%)"
                reply += f"\n• **{r.subject}**: **{r.percentage}%** ({r.classes_attended}/{r.total_classes} lectures) — *{status}*"
            return reply
            
        elif user.role in ['teacher', 'admin']:
            return "👨‍🏫 Faculty Desk: Use the dashboard roster to review class-wide attendance sheets or submit metrics."

    # --- DYNAMIC: GRIEVANCES ---
    if any(w in message for w in grievance_words):
        if not user:
            return "🔑 Sign in to check your complaints status or file new grievances."
            
        if user.role == 'student':
            grievances = Grievance.objects.filter(student=user).order_by('-created_at')
            if not grievances.exists():
                return "📝 You have not filed any grievances yet. Use the grievance submitter widget on your home dashboard."
                
            reply = f"📋 **Your Grievances Desk Status ({user.username}):**\n"
            for g in grievances[:3]:
                reply += f"\n• **Subject**: *{g.subject}* | Status: **{g.get_status_display()}** | Sentiment: **{g.sentiment or 'Pending'}**"
                if g.admin_message:
                    reply += f"\n  └ *Reply*: \"{g.admin_message}\""
            return reply
            
        elif user.role == 'parent':
            return "🔒 **Privacy Notice:** Grievance logs and responses are kept strictly private to the student account and are not accessible on parent accounts."
            
        elif user.role in ['teacher', 'admin']:
            pending = Grievance.objects.filter(status='pending').count()
            return f"📥 **Grievance Desk Summary:** There are **{pending}** pending grievances awaiting attention. Please head to your dashboard administration panel to resolve them."

    # --- DYNAMIC: NOTICES & ANNOUNCEMENTS ---
    if any(w in message for w in notice_words):
        notices = Notice.objects.all().order_by('-priority', '-created_at')[:3]
        if not notices.exists():
            return "📢 No active announcements posted on the notice board yet."
            
        reply = "📢 **Latest Announcements:**\n"
        for n in notices:
            reply += f"\n• **[{n.category}] {n.title}** ({n.created_at.strftime('%b %d')}): *{n.content[:100]}...*"
        return reply

    # Guest, Parent and New User Synonyms
    parent_words = ["parent", "mother", "father", "guardian", "child", "son", "daughter", "ward"]
    register_words = ["register", "signup", "create account", "new user", "how to login", "sign up"]
    admission_words = ["admission", "intake", "courses", "stream", "branches"]
    fee_words = ["fee", "fees", "payment", "due", "tuition", "fine", "scholarship"]
    contact_words = ["contact", "office", "phone", "number", "email", "support", "helpdesk", "admin"]
    
    if any(w in message for w in parent_words):
        return "👨‍👩‍👧‍👦 **Parent Portal Guide:** As a parent or guardian, you can stay informed by reading campus announcements under the Notices Board. If you wish to track specific grievances submitted by your ward, please log in with your designated parent account, or consult our administration office at parent-support@college.edu."
        
    elif any(w in message for w in register_words):
        return "📝 **How to Register:** If you are a new student, click **'Create an account'** on the Sign In page. You must enter your verified **Student ID** and registered **college email** to link with institutional records. If you receive an error, contact the Admin registrar's office."
        
    elif any(w in message for w in admission_words):
        return "🎓 **Admissions & Streams:** Our college offers premier 4-year engineering branches in **Computer Engineering, Information Technology, and AI & Data Science**. For intake deadlines and syllabus information, contact admissions@college.edu."
        
    elif any(w in message for w in fee_words):
        return "💰 **Fee Inquiries:** Official fee structures, payment deadlines, and bank details are shared directly on the Notice Board under the **'Administrative'** category. To avoid penalty, complete all clearances on time."
        
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
        return "I'm sorry, I couldn't fully map that question. You can type **'help'** to see my commands, ask me about your **grades, attendance, notices, grievances**, or translate phrases (e.g., *'translate hindi: College remains closed'*)."
