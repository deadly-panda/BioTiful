from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist 
from django.utils import timezone
from .forms import CheckoutForm
from .models import *

# Create your views here.

class HomeView(ListView):
    model = Item
    template_name = "home.html"
    
    

class CatalogueView(TemplateView ): 
    template_name = "shop/catalogue.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Item.objects.all()
        context['paniers'] = Panier.objects.all()
        context['categories'] = Category.objects.all()
        return context


class ItemDetailView(DetailView):
    context_object_name = 'product'
    model = Item
    template_name = "shop/product.html"


class PanierDetailView(DetailView):
    context_object_name = 'panier'
    model = Panier
    template_name = "shop/panier.html"


class CategoryItemsView(TemplateView):
    context_object_name = 'product'
    template_name = "shop/catalogue.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Item.objects.filter(cat__name=context['catname'])       
        return context
      


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'object':order}
            return render(self.request, "shop/cart.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Vous n'avez pas de panier, Pensez a vous inscrire !")
            return redirect("/")
        
    


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item[0].quantity+=1
            order_item[0].save()
            messages.info(request, "La quantité de ce produit a éte modifier dans  votre panier")
            return redirect("mainApp:cartView")
        else:
            order.items.add(order_item[0].id)
            messages.info(request, "Ce produit a éte ajouter a votre panier")
            return redirect("mainApp:cartView")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item[0].id)
        messages.info(request, "Ce produit a éte ajouter a votre panier")
        return redirect("mainApp:cartView")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Ce produit a éte retirer de votre panier")
            return redirect("mainApp:cartView")
        else:
            messages.info(request, "Ce produit n'était pas dans votre panier")
            return redirect("mainApp:product", slug=slug)          
    else:
        messages.info(request, "Vous n'avez pas encore de panier, Veuillez vous inscrire !")
        return redirect("mainApp:product", slug=slug)
           


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity-=1
                order_item.save()
            else:
                order.items.remove(order_item)            
            return redirect("mainApp:cartView")
        else:
            messages.info(request, "Ce produit n'était pas dans votre panier")
            return redirect("mainApp:product", slug=slug)          
    else:
        messages.info(request, "Vous n'avez pas encore de panier, Veuillez vous inscrire !")
        return redirect("mainApp:product", slug=slug)




class CheckoutView(View):
    def get(self, *args, **kwargs):
        #form
        form =  CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {'form':form, 'object':order}
        return render(self.request, "shop/checkout.html", context)
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            streetaddress = form.cleaned_data.get('streetaddress')
            postcodezip = form.cleaned_data.get('postcodezip')
            ville = form.cleaned_data.get('ville')
            billing_adddress = BillingAdddress(
                user=self.request.user,
                streetaddress = streetaddress,
                postcodezip = postcodezip,
                ville = ville
            )
            billing_adddress.save()
            return redirect('mainApp:checkout')
        messages.warning(self.request, "Echéc")
        return redirect('mainApp:checkout')



@login_required
def add_panier_to_cart(request, slug):
    panier = get_object_or_404(Panier, slug=slug)
    order_item = OrderItem.objects.get_or_create(panier=panier, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(panier__slug=panier.slug).exists():
            order_item[0].quantity+=1
            order_item[0].save()
            messages.info(request, "La quantité de ce produit a éte modifier dans  votre panier")
            return redirect("mainApp:cartView")
        else:
            order.items.add(order_item[0].id)
            messages.info(request, "Ce produit a éte ajouter a votre panier")
            return redirect("mainApp:cartView")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item[0].id)
        messages.info(request, "Ce produit a éte ajouter a votre panier")
        return redirect("mainApp:cartView")


'''
@login_required
def remove_panier_from_cart(request, slug):
    panier = get_object_or_404(Panier, slug=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                panier=panier,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Ce produit a éte retirer de votre panier")
            return redirect("mainApp:cartView")
        else:
            messages.info(request, "Ce produit n'était pas dans votre panier")
            return redirect("mainApp:product", slug=slug)          
    else:
        messages.info(request, "Vous n'avez pas encore de panier, Veuillez vous inscrire !")
        return redirect("mainApp:product", slug=slug)
'''