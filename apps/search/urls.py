from django.urls import path
from .views import SuggestView

urlpatterns = [
    path('suggest', SuggestView.as_view(), name='search_suggest'),
]
