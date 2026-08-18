from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import ServiceCategory, Service, ContactMessage


def home(request):

    categories = ServiceCategory.objects.all()

    return render(
        request,
        'core/home.html',
        {
            'categories': categories
        }
    )


def category_services(request, category_id):

    category = get_object_or_404(
        ServiceCategory,
        id=category_id
    )

    services = Service.objects.filter(
        category=category,
        is_active=True
    )

    return render(
        request,
        'core/services_by_category.html',
        {
            'category': category,
            'services': services
        }
    )


def location(request):

    return render(
        request,
        'core/location.html'
    )


def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        messages.success(
            request,
            "Thank you! Your message has been received. We'll get back to you soon."
        )

        return redirect("/")

    return redirect("/")