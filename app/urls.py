from . import views
from django.urls import path


urlpatterns = [
    # Главная страница
    path('', views.HomeView.as_view(), name='home'),
    
    # Управление записями о движении денежных средств
    path('cashflow/add/', views.CashFlowCreateView.as_view(), name='cashflow_add'),
    path('cashflow/edit/<int:pk>/', views.CashFlowUpdateView.as_view(), name='cashflow_edit'),
    path('cashflow/delete/<int:pk>/', views.CashFlowDeleteView.as_view(), name='cashflow_delete'),
    
    # Страница управления справочниками
    path('dictionary/', views.DictionaryListView.as_view(), name='dictionary'),
    
    # Управление статусами
    path('status/add/', views.StatusCreateView.as_view(), name='status_add'),
    path('status/edit/<int:pk>/', views.StatusUpdateView.as_view(), name='status_edit'),
    path('status/delete/<int:pk>/', views.StatusDeleteView.as_view(), name='status_delete'),
    
    # Управление типами
    path('type/add/', views.TypeCreateView.as_view(), name='type_add'),
    path('type/edit/<int:pk>/', views.TypeUpdateView.as_view(), name='type_edit'),
    path('type/delete/<int:pk>/', views.TypeDeleteView.as_view(), name='type_delete'),
    
    # Управление категориями
    path('category/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('category/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Управление подкатегориями
    path('subcategory/add/', views.SubcategoryCreateView.as_view(), name='subcategory_add'),
    path('subcategory/edit/<int:pk>/', views.SubcategoryUpdateView.as_view(), name='subcategory_edit'),
    path('subcategory/delete/<int:pk>/', views.SubcategoryDeleteView.as_view(), name='subcategory_delete'),
    
    # AJAX-запросы для динамических списков
    path('ajax/get-categories/', views.get_categories_by_type, name='ajax_get_categories'),
    path('ajax/get-subcategories/', views.get_subcategories_by_category, name='ajax_get_subcategories'),
]
