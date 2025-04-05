from django.shortcuts import render, get_object_or_404
from .models import Painting
from .forms import ContactForm
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.core.mail import send_mail


def welcome_page(request):
    return render(request, 'gallery/welcome.html')

# Home page: show all paintings
def gallery_view(request):
    paintings = Painting.objects.all()
    return render(request, 'gallery/gallery.html', {'paintings': paintings})

# Popup view for individual painting
def painting_popup(request, pk):
    painting = get_object_or_404(Painting, pk=pk)
    return render(request, 'gallery/popup.html', {'painting': painting})

# Contact page
def contact_view(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        subject = "New contact message from Contemporan"
        message = f"""
        Name: {form.cleaned_data['name']}
        Email: {form.cleaned_data['email']}
        Message: {form.cleaned_data['message']}
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['picturicontemporane@gmail.com'])
        return render(request, 'gallery/contact_success.html')
    return render(request, 'gallery/contact.html', {'form': form})
