from django import forms
from mymain.models import *


class Create_storage_form (forms.Form):
    storage_address = forms.CharField(max_length=120, required=True, label="Адрес", widget=forms.TextInput(attrs={'class': 'char_field', 'rows': 1}))
    storage_phone = forms.CharField(max_length=11, required=True, label="Телефон", widget=forms.NumberInput(attrs={'class': 'number_field'}))

class Create_order_form (forms.Form):
    consumer_name = forms.CharField(max_length=70, required=True, label="ФИО заказчика", widget=forms.TextInput(attrs={'class': 'char_field', 'rows': 1}))
    consumer_phone = forms.CharField(max_length=11, required=True, label="Телефон", widget=forms.NumberInput(attrs={'class': 'number_field'}))
    storage_num = forms.ModelChoiceField (queryset=Storage.objects.all(), label="Склад")

class  Materials_form (forms.Form):
    material = forms.CharField(max_length=50, required=True, label="Материал", widget=forms.TextInput(attrs={'class': 'order_char_field', 'rows': 1}))
    material_count = forms.CharField(max_length=10, required=True, label="Количество", widget=forms.NumberInput(attrs={'class': 'order_number_field'}))

class Fields_num (forms.Form):
    fields_num = forms.CharField(max_length=2, required=False, label="Кол-во элементов", widget=forms.NumberInput(attrs={'class': 'number_field', 'id': 'field_num'}))

class Login_form (forms.Form):
    login_field = forms.CharField(max_length=15, required=True, label="Логин", widget=forms.TextInput(attrs={'class': 'input', 'readonly onfocus': "this.removeAttribute('readonly')"}))
    password_field = forms.CharField(max_length=50, required=True, label="Пароль", widget=forms.PasswordInput(attrs={'class': 'input', 'readonly onfocus': "this.removeAttribute('readonly')"}))
