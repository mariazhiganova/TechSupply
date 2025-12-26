from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from suppliers.models import Supplier, Product


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'city', 'debt', 'parent_link', 'level_display', 'created_at']
    list_filter = ['city', 'type']
    search_fields = ['name', 'city', 'email']
    actions = ['clear_debt_action']

    def parent_link(self, obj):
        if obj.parent:
            url = reverse('admin:suppliers_supplier_change', args=[obj.parent.id])
            return format_html('<a href="{}">{}</a>', url, obj.parent.name)
        return '-'

    parent_link.short_description = 'Поставщик'

    def level_display(self, obj):
        return f'Уровень {obj.level}'

    level_display.short_description = 'Уровень'
    level_display.admin_order_field = 'parent'

    def clear_debt_action(self, request, queryset):
        """
        Admin action, очищающий задолженность перед поставщиком
        у выбранных объектов. Не применяется к заводам.
        """
        to_clear = queryset.exclude(type=Supplier.FACTORY)

        cleared_count = to_clear.update(debt=0)

        factories_count = queryset.filter(type=Supplier.FACTORY).count()

        messages = []
        if cleared_count > 0:
            messages.append(f'Задолженность очищена у {cleared_count} поставщиков.')

        if factories_count > 0:
            messages.append(f'{factories_count} заводов пропущены (не имеют долга)')

        if messages:
            self.message_user(request, ' '.join(messages))


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('name', 'model', 'release_date')
