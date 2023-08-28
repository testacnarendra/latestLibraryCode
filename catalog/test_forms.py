from django.test import TestCase
import datetime 

from catalog.forms import RenewBookForm


class RenewBookFormTest(TestCase):
	def test_renew_form_date_field_label(self):
		form = RenewBookForm()
		self.assertTrue(form.fields['due_back'].label is None or form.fields['due_back'].label == 'New renewal date')

	def test_renew_form_date_field_help_text(self):
		form = RenewBookForm()
		self.assertEqual(form.fields['due_back'].help_text, 'Enter a date between now and 4 weeks (default 3).')

	# def test_renew_form_date_in_past(self):
	# 	date = datetime.date.today() - datetime.timedelta(days=1)
	# 	form = RenewBookForm(data={'due_back':date})
	# 	self.assertFalse(form.is_valid())
		