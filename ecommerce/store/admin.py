from django.contrib import admin
from .models import Product, Cart, CartItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'image_preview')
    fields = ('name', 'description', 'price', 'stock', 'image')
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="width: 50px; height: 50px;"/>'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
