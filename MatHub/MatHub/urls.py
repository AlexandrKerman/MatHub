from django.contrib import admin
from django.urls import path
from mymain.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', main_win, name="home"),
    path('material', materials, name="materials"),
    path('order', orders, name="orders"),
    path('storage', storages, name="storages"),
    path('consumer', consumers, name="consumers"),
    path('storage/<int:storage_id>', material_in_storage, name="storage"),
    path('order/<int:order_id>', material_in_order, name='order'),
    path('create_order', create_order, name='create_order'),
    path('create_storage', create_storage, name='create_storage'),
    path('login', Login, name='login'),
    path('logout', Logout, name='logout')
]