from django.shortcuts import render , get_object_or_404 , redirect
from produits.models import  Categorie, Order, OrderItem, Produit
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from authapp.models import UserRegistrationModel
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView, View
from django.urls import reverse_lazy
# Create your views here.


#home
def index(request):
    product_object = Produit.objects.all()
    categories = Categorie.objects.all()
    item_name = request.GET.get('item')
    if item_name !='' and item_name is not None:
        product_object = Produit.objects.filter(name__icontains=item_name)

    paginator = Paginator(product_object , 7)
    page = request.GET.get('page')
    product_object = paginator.get_page(page)
    return render(request , 'produits/index.html', context= {'produits': product_object, 'categories':categories})


#detail
def detail(request , myid):
    product_object = Produit.objects.get(id=myid)
    return render(request , 'produits/detail.html' , context={'product': product_object})


def checkout(request):
    return render(request , 'produits/checkout.html')


login_required
def confirmation(request):
    has_order = False
    order_qs = Order.objects.filter(user=request.user , order = False)
    if order_qs.exists():
        order = order_qs[0]
        order.ordered = True
        order.save()
        has_order = True

    return render(request , 'produits/confirmation.html', {'has_order': has_order})


#statistique des achats
@staff_member_required
def statistique(request):
    commande = Order.objects.all().order_by('-ordered_date')
    valide = Order.objects.all().count()
    order_item = OrderItem.objects.all().count()
    total = UserRegistrationModel.objects.all().count()
    return render(request, 'statistique/index.html',{'commande':commande, 'valid': valide, 'order_item':order_item, 'total': total})


@staff_member_required
def product_sellers_list(request):
    userproduits = Produit.objects.all()
    return render(request, 'statistique/table-export.html', {'userproduit':userproduits})


@staff_member_required
def profile(request):
    userprofiles = UserRegistrationModel.objects.all()
    return render(request, 'statistique/app-profile.html', {'userprofiles':userprofiles})





@login_required
def add_to_card(request, pk):
    #get_object_or_404 permet de recuperer une page si el existe au cas contraire renvoit l'erreur 404
    item = get_object_or_404(Produit, id=pk)
    order_item, _ = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__id=item.id).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, f"{item}-quantité augmenté")    
        else:
            order.item.add(order_item)
            messages.success(request, f"produit {item} ajouté")    
    else:
        ordered_date  = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
        messages.info(request, f"produit {item} ajouté")
    return redirect('produits:product_detail', myid=pk)  



class DeleteViewProduct(LoginRequiredMixin,DeleteView):
	model = Produit
	template_name = 'produits/delete_product.html'
	success_url = reverse_lazy('produits:produtListSeller')
	success_message = 'le produit a été supprimé avec succès'    
 


