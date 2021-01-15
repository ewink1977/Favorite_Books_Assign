from django.urls import path
from . import views
	
urlpatterns = [
	path('', views.home, name = 'home'),
    path('register/', views.handle_registration, name = 'register'),
    path('login/', views.handle_login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('books/', views.all_books, name = 'all_books'),
    path('addbook/', views.add_book, name = 'add_book'),
    path('book/<bookid>', views.view_book, name = 'view_book'),
    path('book/<bookid>/edit', views.edit_book, name = 'edit_book'),
    path('book/<bookid>/favorite', views.fav_book, name = 'fav_book'),
]
