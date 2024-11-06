from django.conf import settings
from django.urls import path
from .views import fake_checkout, chatbot_reply, login_view, register, base, product_list, product_detail, add_to_cart, cart_details
from django.conf.urls.static import static

app_name = 'store'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),  # Renamed to avoid conflict with Django's built-in login
    path('', base, name='base'),
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_details, name='cart_details'),
    path('checkout/', fake_checkout, name='checkout'),  # Assuming you want to use fake_checkout
    path('chatbot-response/', chatbot_reply, name="chatbot_reply"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)