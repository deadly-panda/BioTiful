from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomeView,
    ItemDetailView,
    CatalogueView,
    CategoryItemsView,
    add_to_cart,
    remove_from_cart,
    CartView,
    CheckoutView,
    remove_single_item_from_cart,
    PanierDetailView,
    add_panier_to_cart,


)

app_name='mainApp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('catalogue/', CatalogueView.as_view(), name='catalogue'),
    path('catalogue/<catname>', CategoryItemsView.as_view(), name='cat_products'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('panier/<slug>/', PanierDetailView.as_view(), name='panier'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('add_panier_to_cart/<slug>/', add_panier_to_cart, name='add_panier_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),    
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('cartView', CartView.as_view(), name='cartView'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)