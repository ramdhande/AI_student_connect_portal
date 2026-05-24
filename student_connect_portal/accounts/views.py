from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .models import User
from .models import StudentProfile

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == 'admin':
                return redirect('/admin-dashboard/')
            elif user.role == 'parent':
                return redirect('/parent/dashboard/home/')
            else:
                return redirect('/dashboard/home/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def signup_view(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        email = request.POST.get('email')

        # Verify student against college database
        try:
            student = StudentProfile.objects.get(
                student_id=student_id,
                email=email,
                is_active=True
            )
        except StudentProfile.DoesNotExist:
            return render(request, 'signup.html', {
                'form': CustomUserCreationForm(),
                'error': 'You are not found in college records. Please contact administration.'
            })

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.email = email
            user.student_profile = student # VERY IMPORTANT
            user.save()

            login(request, user)
            return redirect('/dashboard/home/')

        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': form.errors
            })

    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('/login/')
