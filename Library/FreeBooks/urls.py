
from django.urls import path
from .views import home_view,authorsListView,authorsDetailView

urlpatterns = [
    path('', home_view.as_view(), name='home'),
	path('authors/', authorsListView.as_view(), name='AuthorList'),
	path('authors/<int:pk>', authorsDetailView.as_view(), name='AuthorDetail'),

]
