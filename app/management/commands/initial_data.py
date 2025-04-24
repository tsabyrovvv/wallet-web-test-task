from django.db import transaction
from django.core.management.base import BaseCommand
from app.models import Status, Type, Category, Subcategory

class Command(BaseCommand):
    help = 'Инициализирует базу данных начальными данными'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Начало инициализации базы данных...')
        
        # Создаем статусы
        statuses = [
            {'name': 'Бизнес'},
            {'name': 'Личное'},
            {'name': 'Налог'},
        ]
        
        for status_data in statuses:
            Status.objects.get_or_create(name=status_data['name'])
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(statuses)} статусов'))
        
        # Создаем типы
        types = [
            {'name': 'Пополнение'},
            {'name': 'Списание'},
        ]
        
        for type_data in types:
            Type.objects.get_or_create(name=type_data['name'])
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(types)} типов'))
        
        # Получаем созданные типы для использования при создании категорий
        income_type = Type.objects.get(name='Пополнение')
        expense_type = Type.objects.get(name='Списание')
        
        # Создаем категории
        categories = [
            {'name': 'Зарплата', 'type': income_type},
            {'name': 'Подработка', 'type': income_type},
            {'name': 'Инвестиции', 'type': income_type},
            {'name': 'Инфраструктура', 'type': expense_type},
            {'name': 'Маркетинг', 'type': expense_type},
            {'name': 'Хозяйственные расходы', 'type': expense_type},
        ]
        
        created_categories = []
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                type=category_data['type']
            )
            created_categories.append(category)
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(categories)} категорий'))
        
        # Создаем подкатегории
        subcategories = [
            # Инфраструктура
            {'name': 'VPS', 'category': Category.objects.get(name='Инфраструктура', type=expense_type)},
            {'name': 'Proxy', 'category': Category.objects.get(name='Инфраструктура', type=expense_type)},
            {'name': 'Домены', 'category': Category.objects.get(name='Инфраструктура', type=expense_type)},
            # Маркетинг
            {'name': 'Farpost', 'category': Category.objects.get(name='Маркетинг', type=expense_type)},
            {'name': 'Avito', 'category': Category.objects.get(name='Маркетинг', type=expense_type)},
            {'name': 'Контекстная реклама', 'category': Category.objects.get(name='Маркетинг', type=expense_type)},
            # Хозяйственные расходы
            {'name': 'Аренда офиса', 'category': Category.objects.get(name='Хозяйственные расходы', type=expense_type)},
            {'name': 'Канцтовары', 'category': Category.objects.get(name='Хозяйственные расходы', type=expense_type)},
            # Зарплата
            {'name': 'Основная работа', 'category': Category.objects.get(name='Зарплата', type=income_type)},
            {'name': 'Премия', 'category': Category.objects.get(name='Зарплата', type=income_type)},
            # Подработка
            {'name': 'Фриланс', 'category': Category.objects.get(name='Подработка', type=income_type)},
            {'name': 'Консультации', 'category': Category.objects.get(name='Подработка', type=income_type)},
            # Инвестиции
            {'name': 'Дивиденды', 'category': Category.objects.get(name='Инвестиции', type=income_type)},
            {'name': 'Проценты по вкладам', 'category': Category.objects.get(name='Инвестиции', type=income_type)},
        ]
        
        for subcategory_data in subcategories:
            Subcategory.objects.get_or_create(
                name=subcategory_data['name'],
                category=subcategory_data['category']
            )
        
        self.stdout.write(self.style.SUCCESS(f'Создано {len(subcategories)} подкатегорий'))
        
        self.stdout.write(self.style.SUCCESS('Инициализация базы данных завершена успешно!'))