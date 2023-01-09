from django.contrib import admin

from .models import Payment, Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'city', 'order_total', 'delivery_charge', 'is_ordered', 'status','payment',)

    list_filter = ('status', 'is_ordered','payment',)
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email')
    list_per_page = 20
    inlines = [OrderProductInline]



class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'payment_method', 'amount_paid', 'status', 'created_at',)
    list_filter = ('status', 'payment_method')
    search_fields = ('payment_id',)
    list_per_page = 20

admin.site.register(Payment,PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)