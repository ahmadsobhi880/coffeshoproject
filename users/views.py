from datetime import datetime
from django.shortcuts import render, redirect
from django.http.response import Http404
from django.contrib import messages
from coffee_app.models import Coffee, CoffeeType, WeekDays
from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import View, TemplateView



class HomeView(View):
    def get(self, request):
        # query=la
        # min_price=1150
        # max_price=9400
        # day=all
        # time_from=13%3A02
        # time_to=18%3A07
        # type=Arabica
        query = request.GET.get('query', None)
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 10000)
        day = request.GET.get('day', None)
        type = request.GET.get('type', None)
        sort = request.GET.get('sort', None)

        coffee_types = []
        coffees = Coffee.objects.all()
        for coffee_type in CoffeeType.objects.all():
            coffee_types.append(coffee_type.name)


        if query:
            coffees = coffees.filter(description__icontains=query, name__icontains=query)

        if min_price or max_price:
            coffees = coffees.filter(price__range=[min_price, max_price])

        if day and not day == "all" :
            if day in WeekDays.objects.all().values_list("name", flat=True):
                coffees = coffees.filter(days_available__name=day)

        if type and not type == "-":
            if type in CoffeeType.objects.all().values_list("name", flat=True):
                coffees = coffees.filter(type__name=type)

        if sort:
            if sort == "price_high":
                coffees = coffees.order_by("-price")
            if sort == "price_low":
                coffees = coffees.order_by("price")

        context = {
            "coffee_types": coffee_types,
            "coffees": coffees,
        }
        return render(request, 'users/home.html', context)


class AboutView(TemplateView):
    template_name = "users/about.html"



def faq(request):
    return render(request, 'users/FAQ.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('full-name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        }
        message = '''
        New message: {}
        From: {}
        '''.format(data['message'], data['email'])
        send_mail(data['subject'], message, '', ['covaccinesce@gmail.com'])
    return render(request, 'users/contact.html')


def register(request):

    # check if request is of type post (user register)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        # check if form received is valid
        if form.is_valid():
            form.save()     # Save the user
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Registered For {username}.')# Flash message usage with f_string
            return redirect('login')   # Redirect user to home page
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})  # Render register with form


@login_required    # Decorator to add restrictions to profile view
# @allowed_users(allowed_roles=['admin'])
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        print(request.FILES)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'users/profile.html', context)
    elif request.method == 'GET':

        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        return render(request, 'users/profile.html', context)
    raise Http404()

