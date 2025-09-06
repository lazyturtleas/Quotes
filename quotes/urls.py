from django.urls import path
from . import views
from .views import QuoteCreateView

urlpatterns = [
    path("", views.random_quote, name="random_quote"),
    path("vote-ajax/<int:quote_id>/<str:action>/", views.vote_ajax, name="vote_ajax"),
    path("top/", views.top_quotes, name="top_quotes"),
    path("add/", QuoteCreateView.as_view(), name="add_quote"),
]