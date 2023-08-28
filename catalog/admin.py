from django.contrib import admin
from catalog.models import Genre, Book, Author, Language, BookInstance

# Register your models here.

admin.site.register(Genre)
admin.site.register(Language)


class BookInstanceInline(admin.TabularInline):
	model = BookInstance
	extra = 0
	exclude = ['imprint']


class BookAdmin(admin.ModelAdmin):
	# pass
	# fields = ["title", "genre", "language", "author", "isbn", "display_genre" ]
	list_display = ('title', 'author', 'display_genre')
	
	fieldsets = [
	("Book Information", {"fields":["title", ("isbn", "genre", "language")]}),
	("Author Information", {"fields":["author"]})

	]
	
	inlines = [BookInstanceInline]
	list_filter = ["title"]
	search_fields = ["title"]

admin.site.register(Book, BookAdmin)



class AuthorAdmin(admin.ModelAdmin):
	list_display = ["first_name", "last_name", "date_of_birth", "date_of_death"]
	fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]
	search_fields = ["first_name", "last_name"]
admin.site.register(Author, AuthorAdmin)


class BookInstanceAdmin(admin.ModelAdmin):
	search_fields = ["status"]
	list_display = ['book', "display_author", "borrower", "status", "due_back"]
	fieldsets = [
	(None, {"fields":["book", "status", "borrower", "id"]}),
	("Availability", {"fields":['due_back']}),
	]
admin.site.register(BookInstance, BookInstanceAdmin)