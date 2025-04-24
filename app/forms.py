from django import forms
from django.utils import timezone
from .models import Status, Type, Category, Subcategory, CashFlow

class DateRangeFilterForm(forms.Form):
    """Форма для фильтрации по диапазону дат"""
    date_from = forms.DateField(
        label="Дата с",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border border-gray-300 rounded px-3 py-2 w-full'})
    )
    date_to = forms.DateField(
        label="Дата по",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border border-gray-300 rounded px-3 py-2 w-full'})
    )
    status = forms.ModelChoiceField(
        label="Статус",
        queryset=Status.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'})
    )
    type = forms.ModelChoiceField(
        label="Тип",
        queryset=Type.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'})
    )
    category = forms.ModelChoiceField(
        label="Категория",
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'})
    )
    subcategory = forms.ModelChoiceField(
        label="Подкатегория",
        queryset=Subcategory.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'})
    )


class StatusForm(forms.ModelForm):
    """Форма для создания и редактирования статусов"""
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'})
        }


class TypeForm(forms.ModelForm):
    """Форма для создания и редактирования типов"""
    class Meta:
        model = Type
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'})
        }


class CategoryForm(forms.ModelForm):
    """Форма для создания и редактирования категорий"""
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'}),
            'type': forms.Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'})
        }


class SubcategoryForm(forms.ModelForm):
    """Форма для создания и редактирования подкатегорий"""
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'}),
            'category': forms.Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'})
        }


class CashFlowForm(forms.ModelForm):
    """Форма для создания и редактирования записей о движении денежных средств"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Если запись редактируется, настраиваем первоначальные queryset для зависимых полей
        if self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
        else:
            # Для новой записи ограничиваем выбор подкатегорий
            self.fields['subcategory'].queryset = Subcategory.objects.none()
            
            # Если форма отправляется и выбрана категория
            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
                except (ValueError, TypeError):
                    pass
    
    class Meta:
        model = CashFlow
        fields = ['date_created', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date_created': forms.DateInput(attrs={'type': 'date', 'class': 'border border-gray-300 rounded px-3 py-2 w-full'}),
            'status': forms.Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'}),
            'type': forms.Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'id': 'id_type'}),
            'category': forms.Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'id': 'id_subcategory'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01', 'class': 'border border-gray-300 rounded px-3 py-2 w-full'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'border border-gray-300 rounded px-3 py-2 w-full'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        
        # Проверка зависимостей между типом и категорией
        type_obj = cleaned_data.get('type')
        category = cleaned_data.get('category')
        
        if type_obj and category and category.type != type_obj:
            self.add_error('category', 'Выбранная категория не соответствует выбранному типу')
        
        # Проверка зависимостей между категорией и подкатегорией
        subcategory = cleaned_data.get('subcategory')
        
        if category and subcategory and subcategory.category != category:
            self.add_error('subcategory', 'Выбранная подкатегория не соответствует выбранной категории')
            
        return cleaned_data
    