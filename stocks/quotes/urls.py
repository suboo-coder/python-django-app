from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about.html', views.about, name='about'),  # href="{% url 'about' %}"
    path("add_stocks.html", views.add_stocks, name="add_stocks"),
    path("delete/<stock_id>", views.delete_stock, name="delete"),
]
