from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CourseForm, LessonForm
from django.contrib import messages

def frontend(request):
    return render(request, 'frontend/index.html')
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = form.cleaned_data['role']
            user.save()
            login(request, user)  # Auto-login after registration
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def home_view(request):
    return render(request, "base.html")

@login_required
def course_list_view(request):
    courses = Course.objects.all()
    return render(request, "course_list.html", {"courses": courses})

@login_required
def create_course_view(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect("course_list")
    else:
        form = CourseForm()
    return render(request, "create_course.html", {"form": form})


@login_required
def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = request.user in course.students.all()

    if request.method == "POST" and not is_enrolled:
        course.students.add(request.user)
        return redirect("course_detail", course_id=course.id)

    return render(request, "course_detail.html", {"course": course, "is_enrolled": is_enrolled})


@login_required
def lesson_list_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()

    return render(request, "lesson_list.html", {"course": course, "lessons": lessons})

@login_required
def create_lesson_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user != course.teacher:
        return redirect("course_detail", course_id=course.id)  # Prevent non-teachers from creating lessons

    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect("lesson_list", course_id=course.id)
    else:
        form = LessonForm()

    return render(request, "create_lesson.html", {"form": form, "course": course})


@login_required
def quiz_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = QuizQuestion.objects.filter(lesson=lesson)

    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.POST.get(str(question.id))
            if user_answer and user_answer.lower().strip() == question.correct_answer.lower().strip():
                score += 1

        QuizResult.objects.create(user=request.user, lesson=lesson, score=score)

        return render(request, 'quiz_result.html', {
            'lesson': lesson,
            'score': score,
            'total': questions.count()
        })

    return render(request, 'quiz.html', {
        'lesson': lesson,
        'questions': questions
    })

@login_required
def dashboard_view(request):
    results = QuizResult.objects.filter(user=request.user)
    enrolled_courses = Course.objects.filter(students=request.user)

    return render(request, 'dashboard.html', {
        'results': results,
        'enrolled_courses': enrolled_courses,
    })