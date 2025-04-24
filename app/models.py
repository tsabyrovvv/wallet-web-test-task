from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Status(models.Model):
    """Модель для хранения статусов ДДС (Бизнес, Личное, Налог и т.д.)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Наименование статуса")
    
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Type(models.Model):
    """Модель для хранения типов ДДС (Пополнение, Списание и т.д.)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Наименование типа")
    
    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для хранения категорий ДДС (Инфраструктура, Маркетинг и т.д.)"""
    name = models.CharField(max_length=100, verbose_name="Наименование категории")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories', verbose_name="Тип")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['type__name', 'name']
        unique_together = ['name', 'type']
    
    def __str__(self):
        return f"{self.name} ({self.type})"


class Subcategory(models.Model):
    """Модель для хранения подкатегорий ДДС (VPS, Proxy, Farpost, Avito и т.д.)"""
    name = models.CharField(max_length=100, verbose_name="Наименование подкатегории")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Категория")
    
    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['category__name', 'name']
        unique_together = ['name', 'category']
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"


class CashFlow(models.Model):
    """Модель для хранения записей о движении денежных средств"""
    date_created = models.DateField(verbose_name="Дата создания записи")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)], 
        verbose_name="Сумма (руб.)"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания в системе")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время последнего обновления")
    
    class Meta:
        verbose_name = "Движение денежных средств"
        verbose_name_plural = "Движение денежных средств"
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.date_created} - {self.type} - {self.category} - {self.subcategory} - {self.amount} руб."
    
    def clean(self):
        """Проверка логических зависимостей между полями"""
        super().clean()
        
        # Проверка зависимости между типом и категорией
        if self.type and self.category and self.category.type != self.type:
            raise ValidationError({
                'category': f'Выбранная категория "{self.category}" не относится к выбранному типу "{self.type}"'
            })
        
        # Проверка зависимости между категорией и подкатегорией
        if self.category and self.subcategory and self.subcategory.category != self.category:
            raise ValidationError({
                'subcategory': f'Выбранная подкатегория "{self.subcategory}" не относится к выбранной категории "{self.category}"'
            })
        
        # Проверка даты (не может быть в будущем)
        if self.date_created and self.date_created > timezone.now().date():
            raise ValidationError({
                'date_created': 'Дата создания записи не может быть в будущем'
            })
    
    def save(self, *args, **kwargs):
        """Переопределение метода сохранения для запуска валидации"""
        self.full_clean()  # Запускаем валидацию перед сохранением
        super().save(*args, **kwargs)
        