from django.urls import path
from .views import RegisterView,LoginView, PurchaseView

urlpatterns = [
    path ('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='auth'), 
    path('purchase/', PurchaseView.as_view(), name='purchase'), 
]