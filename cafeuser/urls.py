from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
     path('item-view/',views.ListMainItem,name='item-view'),
     path('search/',views.SerchMainItem,name='search'),
     path('add-to-cart/<int:pro_id>/',views.AddToCart,name='add-to-cart'),
     path('view-cart/',views.ViewCartUser,name='view-cart'),
     path('increase-quantity/<str:product_name>/', views.IncreaseQty, name='increase-quantity'),
     path('decrease-quantity/<str:product_name>/', views.DecreaseQty, name='decrease-quantity'),
     path('remove/<str:product_name>/', views.RemoveItem, name='remove-item'),
     path('checkout/',views.CreateCheckout,name='checkout'),
     path('sucsess-url/',views.Success,name='sucsess-url'),
     path('cancel/',views.cancel,name='cancel'),
     




    
     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)