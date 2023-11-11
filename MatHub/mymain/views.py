from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db import models, transaction
from mymain.models import Order, Consumer, Storage, Material, Material_in
from mymain.forms import *


@transaction.atomic
def material_save (mat_list):
    newlist = list()
    for i in mat_list:
        newlist.append(Material.objects.get_or_create(material_name=i)[0])
    return newlist

def delete (model, rqst):
    for_delete = list(map(int, rqst.getlist('chk')))
    model.objects.filter(id__in=for_delete).delete()


def main_win(request):
    data = {"field_num": Fields_num()}
    return render(request, "index.html", data)

def materials(request):
    material = Material_in.objects.select_related('material_name').values('material_name__id', 'material_name__material_name').annotate(total_sum=models.aggregates.Sum('material_count'))
    data = {"materials": material,
            "field_num": Fields_num()}
    return render (request, "materials.html", data)

def storages (request):
    storage = Storage.objects.values ('id', 'storage_address', 'storage_phone')
    data = {"storages": storage,
            "field_num": Fields_num()}
    if request.method == "POST":
        rqst = request.POST
        delete(Storage, rqst)
    return render(request, "storages.html", data)

def consumers (request):
    consumer = Consumer.objects.select_related('id').values('id', 'consumer_name','consumer_phone').annotate(total_count=models.aggregates.Count('order'))
    data = {"consumers": consumer,
            "field_num": Fields_num()}
    return render(request, "consumers.html", data)

def orders (request):
    order = Order.objects.select_related('consumer', 'storage', 'id').values('id', 'consumer__consumer_name', 'consumer__consumer_phone', 'storage__storage_address').annotate(total_count=models.aggregates.Count('material_in'))
    order_ids = [i['id'] for i in order.values('id')]
    data = {"orders": order,
            "field_num": Fields_num(),
            "order_ids": order_ids}
    if request.method == 'POST':
        rqst = request.POST
        order_form = Create_order_form (request.POST)
        if 'create_order_request' in rqst:
            if order_form.is_valid():
                storage_id = int (rqst['storage_num'])
                mats = list (rqst.getlist('material'))
                mat_counts = list (map (int, rqst.getlist('material_count')))
                consumer = Consumer.objects.get_or_create(consumer_name=rqst['consumer_name'], consumer_phone=rqst['consumer_phone'])
                storage = Storage.objects.get (id=storage_id)
                order = Order.objects.create (consumer=consumer[0], storage=storage)
                iterator = range (0, len(mats))
                query_mat_list = list (material_save(mats))
                Material_in.objects.bulk_create ([Material_in(**{'order': order, 'material_name': query_mat_list[i], 'material_count': mat_counts[i]}) for i in iterator], ignore_conflicts=False)
        elif 'delete_order_request' in rqst:
            delete(Order, rqst)
    return render(request, "orders.html", data)

def material_in_storage (request, storage_id):
    material = Material_in.objects.select_related('order', 'material').values('material_name__id', 'material_name__material_name').filter(order__storage=storage_id).annotate(total_sum=models.aggregates.Sum('material_count'))
    data = {"materials": material,
            "storage_id": storage_id,
            "field_num": Fields_num()}
    return render(request, "storage_material.html", data)

def material_in_order (request, order_id):
    material = Material_in.objects.select_related('material').values('material_name__id', 'material_name__material_name').filter(order=order_id).annotate(total_sum=models.aggregates.Sum('material_count'))
    data = {"materials": material,
            "order_id": order_id,
            "field_num": Fields_num()}
    return render(request, "order_material.html", data)

def create_storage (request):
    if request.method == 'POST':
        form = Create_storage_form (request.POST)
        if form.is_valid ():
            try:
                Storage.objects.get_or_create(**form.cleaned_data)
                form = Create_storage_form ()
            except:
                form.add_error (None, 'При создании склада произошла ошибка')
    else:
        form = Create_storage_form ()
    data = {"form": form,
            "field_num": Fields_num()}
    return render(request, "create_storage.html", data)

def create_order (request):
    if request.method == 'GET':
        num_field = request.GET
        try:
            num = int (num_field['fields_num'])
            if num>99:
                num=99;
        except:
            num = 0
        num_iter = range (0, num)
        material = list()
        for i in num_iter:
            material.append (Materials_form ())
    form = Create_order_form ()
    data = {"form": form,
            "field_num": Fields_num(),
            "material": material}
    return render(request, "create_order.html", data)

def Login (request):
    if request.method == 'POST':
        form = Login_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login_field']
            password = form.cleaned_data['password_field']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = Login_form()
    return render(request, 'login.html', {'form': form})

def Logout (request):
    logout(request)
    return redirect('login')