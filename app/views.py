from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from .models import Status, Type, Category, Subcategory, CashFlow
from .forms import (
    DateRangeFilterForm,
    StatusForm, TypeForm, CategoryForm, SubcategoryForm, CashFlowForm,
)


class HomeView(ListView):
    """Главная страница со списком всех записей о движении денежных средств"""
    model = CashFlow
    template_name = 'cashflow/home.html'
    context_object_name = 'cashflows'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Получаем параметры фильтрации из GET-запроса
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        status_id = self.request.GET.get('status')
        type_id = self.request.GET.get('type')
        category_id = self.request.GET.get('category')
        subcategory_id = self.request.GET.get('subcategory')
        
        # Применяем фильтры
        if date_from:
            queryset = queryset.filter(date_created__gte=date_from)
        if date_to:
            queryset = queryset.filter(date_created__lte=date_to)
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if type_id:
            queryset = queryset.filter(type_id=type_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Добавляем форму для фильтрации
        filter_form = DateRangeFilterForm(self.request.GET)
        context['filter_form'] = filter_form
        
        # Сохраняем параметры фильтрации для пагинации
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = query_params.urlencode()
        
        return context


class CashFlowCreateView(CreateView):
    """Представление для создания новой записи о движении денежных средств"""
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cashflow/cashflow_form.html'
    success_url = reverse_lazy('home')
    
    def get_initial(self):
        initial = super().get_initial()
        initial['date_created'] = timezone.now().date()
        return initial
    
    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно создана')
        return super().form_valid(form)


class CashFlowUpdateView(UpdateView):
    """Представление для редактирования записи о движении денежных средств"""
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cashflow/cashflow_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно обновлена')
        return super().form_valid(form)


class CashFlowDeleteView(DeleteView):
    """Представление для удаления записи о движении денежных средств"""
    model = CashFlow
    template_name = 'cashflow/cashflow_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена')
        return super().delete(request, *args, **kwargs)


# Представления для управления справочниками

class DictionaryListView(TemplateView):
    """Представление для управления справочниками"""
    template_name = 'cashflow/dictionary.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        
        # Формы для создания новых записей
        context['status_form'] = StatusForm()
        context['type_form'] = TypeForm()
        context['category_form'] = CategoryForm()
        context['subcategory_form'] = SubcategoryForm()
        
        return context


# Представления для управления статусами

class StatusCreateView(CreateView):
    """Представление для создания нового статуса"""
    model = Status
    form_class = StatusForm
    template_name = 'cashflow/status_form.html'
    success_url = reverse_lazy('dictionary')
    
    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)


class StatusUpdateView(UpdateView):
    """Представление для редактирования статуса"""
    model = Status
    form_class = StatusForm
    template_name = 'cashflow/status_form.html'
    success_url = reverse_lazy('dictionary')
    
    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно обновлен')
        return super().form_valid(form)


class StatusDeleteView(DeleteView):
    """Представление для удаления статуса"""
    model = Status
    template_name = 'cashflow/status_confirm_delete.html'
    success_url = reverse_lazy('dictionary')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Статус успешно удален')
        return super().delete(request, *args, **kwargs)


# Представления для управления типами

class TypeCreateView(CreateView):
    """Представление для создания нового типа"""
    model = Type
    form_class = TypeForm
    template_name = 'cashflow/type_form.html'
    success_url = reverse_lazy('dictionary')
    
    def form_valid(self, form):
        messages.success(self.request, 'Тип успешно создан')
        return super().form_valid(form)


class TypeUpdateView(UpdateView):
    """Представление для редактирования типа"""
    model = Type
    form_class = TypeForm
    template_name = 'cashflow/type_form.html'
    success_url = reverse_lazy('dictionary')
    
    def form_valid(self, form):
        messages.success(self.request, 'Тип успешно обновлен')
        return super().form_valid(form)


class TypeDeleteView(DeleteView):
    """Представление для удаления типа"""
    model = Type
    template_name = 'cashflow/type_confirm_delete.html'
    success_url = reverse_lazy('dictionary')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Тип успешно удален')
        return super().delete(request, *args, **kwargs)


# Представления для управления категориями

class CategoryCreateView(CreateView):
    """Представление для создания новой категории"""
    model = Category
    form_class = CategoryForm
    template_name = 'cashflow/category_form.html'
    success_url = reverse_lazy('dictionary')
    
    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно создана')
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    """Представление для редактирования категории"""
    model = Category
    form_class = CategoryForm
    template_name = 'cashflow/category_form.html'
    success_url = reverse_lazy('dictionary')
    
    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно обновлена')
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    """Представление для удаления категории"""
    model = Category
    template_name = 'cashflow/category_confirm_delete.html'
    success_url = reverse_lazy('dictionary')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Категория успешно удалена')
        return super().delete(request, *args, **kwargs)


# Представления для управления подкатегориями

class SubcategoryCreateView(CreateView):
    """Представление для создания новой подкатегории"""
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'cashflow/subcategory_form.html'
    success_url = reverse_lazy('dictionary')
    
    def form_valid(self, form):
        messages.success(self.request, 'Подкатегория успешно создана')
        return super().form_valid(form)


class SubcategoryUpdateView(UpdateView):
    """Представление для редактирования подкатегории"""
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'cashflow/subcategory_form.html'
    success_url = reverse_lazy('dictionary')
    
    def form_valid(self, form):
        messages.success(self.request, 'Подкатегория успешно обновлена')
        return super().form_valid(form)


class SubcategoryDeleteView(DeleteView):
    """Представление для удаления подкатегории"""
    model = Subcategory
    template_name = 'cashflow/subcategory_confirm_delete.html'
    success_url = reverse_lazy('dictionary')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Подкатегория успешно удалена')
        return super().delete(request, *args, **kwargs)


# AJAX-представления для динамического обновления зависимых списков

def get_categories_by_type(request):
    """AJAX-представление для получения категорий по выбранному типу"""
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)


def get_subcategories_by_category(request):
    """AJAX-представление для получения подкатегорий по выбранной категории"""
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)
