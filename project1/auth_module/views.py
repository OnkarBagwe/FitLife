from cmath import log
from django.contrib import messages
from django.shortcuts import redirect
from distutils.log import Log
from django.shortcuts import render
from django.views.generic import UpdateView
from forms import register_user_form
from auth_module.models import registered_user
# Create your views here.
class register_user_form_view(UpdateView):
    model = registered_user
    form = register_user_form
    template_name = 'register.html'

# def register(request):
#     print("one")
#     # return render(request, 'register.html')
#     return render(request, 'register.html', {'form': register_user_form})

def register(request):
    if request.method == 'POST':
        form = register_user_form(request.POST)
        if form.is_valid():
            if registered_user.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request,'Email already exists')
            else:
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account has been created! You are now able to log in')
                return redirect('home')

    else:
        form = register_user_form()
    return render(request, 'register.html', {'form': form})


def home(request):
    return render(request,'home.html')