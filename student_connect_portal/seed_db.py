import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_connect_portal.settings')
django.setup()

from accounts.models import User, StudentProfile, TeacherProfile, ParentProfile, StudentProgress, Attendance

def seed():
    print("--- Starting Database Seeding & Repair ---")
    
    # 1. Clean existing records to avoid duplicates
    print("Cleaning database...")
    StudentProfile.objects.all().delete()
    # Delete test users, but keep valid ones or rebuild them
    User.objects.all().delete()
    
    # 2. Create Institutional Student Profiles
    print("Creating institutional student profiles (College Records Database)...")
    
    prof_ram = StudentProfile.objects.create(
        student_id="STU001",
        full_name="Ram Dhande",
        email="ram12@gmail.com",
        department="Computer Engineering",
        year=4,
        is_active=True
    )
    
    prof_pawan = StudentProfile.objects.create(
        student_id="STU002",
        full_name="Pawan Mama",
        email="pawan2@gmail.com",
        department="Information Technology",
        year=4,
        is_active=True
    )
    
    prof_vedant = StudentProfile.objects.create(
        student_id="STU003",
        full_name="Vedant Petkar",
        email="vedant@gmail.com",
        department="AI & Data Science",
        year=4,
        is_active=True
    )
    
    print(f"Created {StudentProfile.objects.count()} student profiles.")

    # 2.5. Create institutional Teacher & Parent Profiles
    print("Creating institutional teacher profiles...")
    prof_teacher = TeacherProfile.objects.create(
        teacher_id="TEACH001",
        full_name="Ram Teacher",
        email="teacherram@gmail.com",
        department="Computer Engineering",
        is_active=True
    )

    print("Creating institutional parent profiles...")
    prof_parent = ParentProfile.objects.create(
        parent_id="PAR001",
        full_name="Ram Parent",
        email="parentram@gmail.com",
        phone="9876543210",
        linked_student=prof_ram,
        is_active=True
    )

    # 3. Create Users with properly HASHED passwords
    print("\nCreating users with properly hashed passwords...")

    # A. Superuser / Admin "R"
    admin_user = User.objects.create_superuser(
        username="R",
        email="ram@gmail.com",
        password="ram123"
    )
    admin_user.role = 'admin'
    admin_user.save()
    print("-> Admin Superuser 'R' created successfully (Password: ram123).")

    # B. Student User "ram_dhande"
    student_ram = User.objects.create_user(
        username="ram_dhande",
        email="ram12@gmail.com",
        password="ram123"
    )
    student_ram.role = 'student'
    student_ram.student_profile = prof_ram
    student_ram.save()
    print("-> Student 'ram_dhande' created successfully (Password: ram123).")

    # C. Student User "student_mama"
    student_pawan = User.objects.create_user(
        username="student_mama",
        email="pawan2@gmail.com",
        password="pubglover12"
    )
    student_pawan.role = 'student'
    student_pawan.student_profile = prof_pawan
    student_pawan.save()
    print("-> Student 'student_mama' created successfully (Password: pubglover12).")

    # D. Student User "vedant"
    student_vedant = User.objects.create_user(
        username="vedant",
        email="vedant@gmail.com",
        password="vedant123"
    )
    student_vedant.role = 'student'
    student_vedant.student_profile = prof_vedant
    student_vedant.save()
    print("-> Student 'vedant' created successfully (Password: vedant123).")

    # E. Parent User "parent_ram"
    parent_ram = User.objects.create_user(
        username="parent_ram",
        email="parentram@gmail.com",
        password="parent123"
    )
    parent_ram.role = 'parent'
    parent_ram.parent_profile = prof_parent
    parent_ram.save()
    print("-> Parent 'parent_ram' created successfully (Password: parent123).")

    # F. Teacher User "teacher_ram"
    teacher_ram = User.objects.create_user(
        username="teacher_ram",
        email="teacherram@gmail.com",
        password="teacher123"
    )
    teacher_ram.role = 'teacher'
    teacher_ram.teacher_profile = prof_teacher
    teacher_ram.save()
    print("-> Teacher 'teacher_ram' created successfully (Password: teacher123).")

    # 4. Seed student progress and attendance
    print("\nSeeding student progress and attendance records...")
    
    subjects = [
        ("DSA (Data Structures & Algorithms)", 88, "A", 85, 40, 34),
        ("OS (Operating Systems)", 92, "A+", 78, 40, 31),
        ("DBMS (Database Management Systems)", 85, "A", 88, 40, 35),
        ("ML (Machine Learning Basics)", 90, "A+", 80, 40, 32),
        ("CN (Computer Networks)", 84, "B+", 81, 40, 32),
    ]
    
    for subject, marks, grade, percentage, total_classes, classes_attended in subjects:
        # Progress
        StudentProgress.objects.create(
            student=prof_ram,
            subject=subject,
            marks=marks,
            grade=grade,
            semester=4
        )
        # Attendance
        Attendance.objects.create(
            student=prof_ram,
            subject=subject,
            percentage=percentage,
            total_classes=total_classes,
            classes_attended=classes_attended
        )

    print("\n--- Seeding & Repair Finished Successfully! ---")
    print("You can now log in using any of the credentials.")

if __name__ == '__main__':
    seed()
