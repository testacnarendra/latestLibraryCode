import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.forms import RenewBookForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from catalog.models import Book, BookInstance, Author
from django.views.generic.edit import CreateView, UpdateView, DeleteView




# Create your views here.
@login_required
def index(request):
	"""View function for home page of site."""
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.all().count()
	num_visits = request.session.get('num_visits',0)
	request.session['num_visits'] = num_visits + 1
	
	context = {
		'num_books':num_books,
		'num_instances':num_instances,
		'num_instances_available':num_instances_available,
		'num_authors':num_authors,
		'num_visits':num_visits ,
	}
	return render(request, 'catalog/index.html', context=context)

def logged_out(request):
	return render(request, 'registration/logged_out.html')


class BookListView(LoginRequiredMixin, generic.ListView):
	model = Book
	context_object_name = 'book_list'
	template_name = 'catalog/book_list.html'
	paginate_by = 5
	
	def get_queryset(self):
		return Book.objects.all()
		# return Book.objects.filter(title__icontains='a')[:5]

class AuthorListView(LoginRequiredMixin, generic.ListView):
	model= Author
	context_object_name='author_list'
	template_name = 'catalog/author_list.html'

	def get_queryset(self):
		return Author.objects.all()


class BookDetailView(LoginRequiredMixin,generic.DetailView):
	model = Book
	template_name = 'catalog/book_detail.html'
	


class AuthorDetailView(generic.DetailView):
	model = Author
	template_name = 'catalog/author_detail.html' 
	

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	"""Generic class-based view listing books on loan to current user."""
	model = BookInstance
	context_object_name = 'bookinstance_list'
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 5

	def get_queryset(self):
		# return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
		for group in self.request.user.groups.all().values():
			if group['name'] == 'Librarians':
				return BookInstance.objects.all().filter(status__exact='o').order_by('due_back')
			elif self.request.user.is_staff:
				return BookInstance.objects.all().filter(status__exact='o').order_by('due_back')
			else:
				return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


@login_required
# @permission_required('can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
	book_instance = get_object_or_404(BookInstance, pk=pk)
	if request.method == 'POST':
		form = RenewBookForm(request.POST)

		if form.is_valid():
			book_instance.due_back = form.cleaned_data['due_back']
			book_instance.save()
			# redirect to a new URL:
			return HttpResponseRedirect(reverse('my-borrowed'))	
	else:
		proposed_renewal_date = datetime.date.today()+datetime.timedelta(weeks=3)
		form = RenewBookForm(initial={'due_back': proposed_renewal_date})
	context = {
		'form':form,
		'book_instance':book_instance
	}
	return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreateView(LoginRequiredMixin,CreateView):
	model = Author
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
	initial = {'date_of_death': '11/06/2020'}
	template_name_suffix = '_create_form'


class AuthorUpdateView(UpdateView):
	model = Author
	fields = '__all__'

class AuthorDeleteView(DeleteView):
	model = Author
	success_url = reverse_lazy('authors')


class BookCreateView(CreateView):
	model = Book
	fields = '__all__'
	template_name_suffix = '_create_form'