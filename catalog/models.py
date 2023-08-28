from django.db import models
from django.urls import reverse
import uuid # Required for unique book instances
from datetime import date
from django.contrib.auth.models import User  # Required to assign User as a borrower
from datetime import date


class Genre(models.Model):
	""" model representing Book Genre"""
	name = models.CharField(max_length=200, help_text="Enter the book genre i.e Science , Fiction etc")

	def __str__(self):
		"""String for representing the model object"""
		return self.name

class Language(models.Model):
	"""Model representing a Language (e.g. English, French, Japanese, etc.)"""
	name = models.CharField(max_length=100, help_text="Enter books natural language e.g English, Hindi etc")

	def __str__(self):
		return self.name


class Author(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True, verbose_name='birth date')
	date_of_death = models.DateField(null=True, blank=True)

	class Meta:
		ordering = ['last_name']

	def __str__(self):
		return f'{self.last_name},{self.first_name}'

	def get_absolute_url(self):
		"""Returns the URL to access a particular author instance."""
		return reverse('author-detail', args=[str(self.id)])
	

class Book(models.Model):
	title=models.CharField(max_length=200)
	# book can only have one author, but authors can have multiple books ...onetomany relationship 
	author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
	summary = models.TextField(max_length=500, help_text="Enter the brief description of the book")
	isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
	# ManyToManyField used because genre can contain many books. Books can cover many genres.
	genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
	language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('book-detail', args=[str(self.id)])

	def display_genre(self):
		"""Create a string for the Genre. This is required to display genre in Admin."""
		return ', '.join(genre.name for genre in self.genre.all()[:3]) 


	
LOAN_STATUS = (
	('m', 'Maintanance'),
	('o', 'On loan'),
	('a', 'Awailable'),
	('r', 'Reserved')
	)
class BookInstance(models.Model):
	"""Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='unique id for this book across this library')
	book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True, help_text='Due back date')
	status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book Availability')
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

	class Meta:
		ordering = ['due_back']
		permissions = (("can_mark_returned", "Set book as returned"),)

	def __str__(self):
		"""String for representing the Model object."""
		return f'{self.id}, {self.book.title}'

	def display_author(self):
		# import pdb;pdb.set_trace()
		return f'{self.book.author.first_name} {self.book.author.last_name}'

	@property
	def is_overdue(self):
		"""Determines if the book is overdue based on due date and current date."""
		return bool(self.due_back and date.today() > self.due_back)


