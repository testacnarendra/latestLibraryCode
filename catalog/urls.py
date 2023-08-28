from django.urls import path
from .import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('index/', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/',views.AuthorListView.as_view(), name='authors'),
    path('accounts/logout', views.logged_out, name='logout'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book' ),
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/update', views.AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name='author-delete'),
    path('book/create/', views.BookCreateView.as_view(), name='book-create')


]
