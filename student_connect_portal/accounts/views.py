from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .models import User, StudentProfile, TeacherProfile, ParentProfile

def login_view(request):
    # Unified Portal Selection Page
    return render(request, 'accounts/portal_login.html')


def signup_view(request):
    # Unified Portal Selection Page
    return render(request, 'accounts/portal_signup.html')


def generic_login_view(request, role, template_name, redirect_url):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            if user.role == role:
                login(request, user)
                if role == 'parent' and hasattr(user, 'parent_profile') and user.parent_profile:
                    request.session['linked_student_id'] = user.parent_profile.linked_student.student_id
                return redirect(redirect_url)
            else:
                return render(request, template_name, {'error': f'Invalid credentials. This account is not registered as a {role.capitalize()}.'})
        else:
            return render(request, template_name, {'error': 'Invalid username or password.'})

    return render(request, template_name)


def generic_signup_view(request, role, profile_model, id_field, template_name, redirect_url):
    if request.method == "POST":
        profile_id = request.POST.get('profile_id')
        email = request.POST.get('email')

        # Verify against profile database records
        try:
            filter_kwargs = {id_field: profile_id, 'email': email, 'is_active': True}
            profile = profile_model.objects.get(**filter_kwargs)
        except profile_model.DoesNotExist:
            return render(request, template_name, {
                'form': CustomUserCreationForm(),
                'error': f'No verified {role} record found in college database matching ID & Email.'
            })

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = role
            user.email = email

            if role == 'student':
                user.student_profile = profile
            elif role == 'teacher':
                user.teacher_profile = profile
            elif role == 'parent':
                user.parent_profile = profile

            user.save()
            login(request, user)

            if role == 'parent' and profile.linked_student:
                request.session['linked_student_id'] = profile.linked_student.student_id

            return redirect(redirect_url)
        else:
            return render(request, template_name, {
                'form': form,
                'error': form.errors
            })

    else:
        form = CustomUserCreationForm()

    return render(request, template_name, {'form': form})


def student_login_view(request):
    return generic_login_view(request, 'student', 'accounts/student_login.html', '/dashboard/home/')


def student_signup_view(request):
    return generic_signup_view(request, 'student', StudentProfile, 'student_id', 'accounts/student_signup.html', '/dashboard/home/')


def teacher_login_view(request):
    return generic_login_view(request, 'teacher', 'accounts/teacher_login.html', '/teacher/dashboard/')


def teacher_signup_view(request):
    return generic_signup_view(request, 'teacher', TeacherProfile, 'teacher_id', 'accounts/teacher_signup.html', '/teacher/dashboard/')


def parent_login_view(request):
    return generic_login_view(request, 'parent', 'accounts/parent_login.html', '/parent/dashboard/home/')


def parent_signup_view(request):
    return generic_signup_view(request, 'parent', ParentProfile, 'parent_id', 'accounts/parent_signup.html', '/parent/dashboard/home/')


def logout_view(request):
    logout(request)
    return redirect('/login/')
