from django.shortcuts import render
from .forms import UserRegisterForm , PatientForm , DoctorForm , PersonForm , UpdateForm, ReceptionistForm
from django.views.generic import View

# Create your views here.
def index(request):
	return render(request,'index.html')

def test(request):
	return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = PatientForm(request.POST)

        if u_form.is_valid():
            u_form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
    else:
        u_form = UserRegisterForm()
        p_form = PatientForm()
    return render(request, 'register.html', {'u_form': u_form, 'p_form':p_form})