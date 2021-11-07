from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ContactForm
# Create your views here.

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm

def index(request):
    return render(request, 'photos/index.html')

def menu(request):
    return render(request, 'photos/menu.html')

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            new_line = '\n'
            message = f"Name: {name}{new_line}Phone: {phone}{new_line}Email: {from_email}{new_line}Message: {message}"
            try:
                send_mail("[DESSERTS] Contact Form", message, None, ['deanna@deelightfuldesserts.com'],
    fail_silently=False,)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "photos/contact.html", {'form': form})

def success(request):
    return render(request, 'photos/thank_you.html')

def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')

    return render(request, 'photos/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('gallery')

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)

def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(
            category__name=category)

    categories = Category.objects.all()
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)


def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})

def order(request):
    return render(request, 'photos/order.html')

def deletePhoto(request, pk):
    Photo.objects.filter(pk=pk).delete()
    return redirect('gallery')
    
@login_required(login_url='login')
def addPhoto(request):
    user = request.user
    categories = user.category_set.all()
    if request.method == 'POST':
        data = request.POST
        image_file = request.FILES['image_file']

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        upload = Photo(
            category=category,
            description=data['description'],
            image=image_file
        )
        upload.save()

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)
