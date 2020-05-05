# delivery/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django import forms
from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.forms.models import inlineformset_factory

from delivery.models import (
    Food,
    Category,
    Invoice,
    InvoiceDetail
    )

class IndexView(ListView):
    model = Food
    template_name = 'delivery/index.html'

class CategoryFoodView(ListView):
    model = Food
    template_name = 'delivery/category_food.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class DetailFoodView(ListView):
    model = Food
    template_name = 'delivery/food_detail.html'

    def get_queryset(self):
        food_name = self.kwargs['food_name']
        self.food = get_object_or_404(Food, name=food_name)
        qs = super().get_queryset().filter(name=self.food)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['food'] = self.food
        return context

# --- qiita --- #

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('customer',)


class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = ('food', 'quantity',)

    def __init__(self, *args, **kwargs):
        super(InvoiceDetailForm, self).__init__(*args, **kwargs)

        self.fields['item'].choices = lambda: [('', '-- 商品 --')] + [
            (item.id, '%s %s円' % (item.name.ljust(10, '　'), item.unit_price)) for item in
            Item.objects.order_by('order')]

        choices_number = [('', '-- 個数 --')] + [(str(i), str(i)) for i in range(1, 10)]
        self.fields['quantity'].widget = Select(choices=choices_number)


InvoiceDetailFormSet = inlineformset_factory(
    parent_model=Invoice,
    model=InvoiceDetail,
    form=InvoiceDetailForm,
    extra=1,
    min_num=1,
    validate_min=True,
)

class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

class InvoiceMixin(object):
    def form_valid(self, form, formset):

        # formset.saveでインスタンスを取得できるように、既存データに変更が無くても更新対象となるようにする
        for detail_form in formset.forms:
            if detail_form.cleaned_data:
                detail_form.has_changed = lambda: True

        # インスタンスの取得
        invoice = form.save(commit=False)
        formset.instance = invoice
        details = formset.save(commit=False)

        sub_total = 0

        # 明細に単価と合計を設定
        for detail in details:
            detail.unit_price = detail.item.unit_price
            detail.amount = detail.unit_price * detail.quantity
            sub_total += detail.amount

        # 見出しに小計、消費税、合計、担当者を設定
        tax = round(sub_total * 0.08)
        total_amount = sub_total + tax

        invoice.sub_total = sub_total
        invoice.tax = tax
        invoice.total_amount = total_amount
        invoice.created_by = self.request.user

        # DB更新
        with transaction.atomic():
            invoice.save()
            formset.instance = invoice
            formset.save()

        # 処理後は詳細ページを表示
        return redirect(invoice.get_absolute_url())


class InvoiceCreateView(InvoiceMixin, FormsetMixin, CreateView):
    template_name = 'invoice/invoice_form.html'
    model = Invoice
    form_class = InvoiceForm
    formset_class = InvoiceDetailFormSet


class InvoiceUpdateView(InvoiceMixin, FormsetMixin, UpdateView):
    is_update_view = True
    template_name = 'invoice/invoice_form.html'
    model = Invoice
    form_class = InvoiceForm
    formset_class = InvoiceDetailFormSet

class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy('index')
