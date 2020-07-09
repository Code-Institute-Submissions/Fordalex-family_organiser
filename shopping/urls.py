from django.urls import path
from . import views

urlpatterns = [
    path('shopping_page', views.shopping_page, name="shopping_page"),
    path('update_item/<operation>', views.update_item, name="update_item"),
    path('update_category/<operation>/<pk>', views.update_category, name="update_category"),
]