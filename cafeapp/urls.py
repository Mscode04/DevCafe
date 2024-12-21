from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
      path('add-item/', views.CreateMainItem, name='create-item-main'),
      path('item-list-admin/',views.ListMainItemAdimn,name='item-list-admin'),
      path('item-main-update/<int:item_id>/',views.UpdateMainItem,name='item-main-update'),
      path('item-main-delete/<int:item_id>/',views.DeleteMainItem,name='item-main-delete'),
      path('item-main-detail/<int:item_id>/',views.DetailMainItem,name='item-main-detail'),
      path('search-ad/',views.SerchMainItemAdmin,name='search-ad'),
]
      




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)