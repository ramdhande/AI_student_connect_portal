import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_connect_portal.settings')
django.setup()

from accounts.models import User, StudentProfile

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

    print("\n--- Seeding & Repair Finished Successfully! ---")
    print("You can now log in using any of the credentials.")

if __name__ == '__main__':
    seed()
