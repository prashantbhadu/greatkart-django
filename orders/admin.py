from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('product', 'variations_display', 'quantity', 'product_price', 'ordered', 'user', 'payment')
    extra = 0

    def variations_display(self, obj):
        return ", ".join(str(v) for v in obj.variations.all()) or '—'
    variations_display.short_description = 'Variations'


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user', 'payment_method', 'amount_paid', 'status', 'created_at']
    search_fields = ['payment_id', 'user__email']
    list_per_page = 20
    readonly_fields = ['payment_id', 'user', 'payment_method', 'amount_paid', 'status', 'created_at']


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'full_name', 'phone', 'email',
        'city', 'country', 'order_total', 'tax',
        'status', 'is_ordered', 'created_at'
    ]
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_filter = ['status', 'is_ordered']
    list_per_page = 20
    inlines = [OrderProductInline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'product_price', 'ordered', 'created_at']
    list_per_page = 20


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
