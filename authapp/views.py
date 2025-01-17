from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from produits.models import  Order
from .forms import UserCustomerForm, UserRegistration, UserEditForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.

#dashbord du vendeur
@login_required(login_url='/login')
def dashbord(request):
    order_list = []
    order = Order.objects.all()
    for order in order:
        for element in order.item.all():
            if element.item.user ==request.user:
                order_list.append(element)
    count = len(order_list)


    context = {
        'count': count,
        'order_list':order_list,

         "welcome": "Welcome to your dashboard"
    }

    return render(request, 'seller/index.html', context=context)


def registerUser(request):
    if request.method == 'POST':
        form = UserCustomerForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect
        
        else:
            form = UserCustomerForm()

        context = {
            "form":form
        }


    return render(request, 'authapp/registeruser.html', context=context)  




def sign(request):
    error = False
    if request.method == "POST":

        #on va traiter le formulaire
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username , password=password)
        if user is None and user.is_active:
            login(request , user)
            if user.peut_vendre:
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))   
                return redirect('/')
            elif user.ne_peut_vendre:
                return render(request, 'authapp/peux_pas_vendre.html')
            else:
                return redirect('/')
            
        else :
            error = True
    return render(request, 'registration/log.html',{'error':error})

@login_required
def logout(request):
    logout(request)
    return redirect('/auth')    


@login_required(login_url='/login')
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()

    else:
        user_form = UserEditForm(instance = request.user)

        context = {
            'form': user_form
        }

        return render(request, 'authapp/edit.html', context=context)


