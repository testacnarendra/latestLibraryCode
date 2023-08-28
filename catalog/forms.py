from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from catalog.models import BookInstance
from django.utils.translation import gettext as _



# class RenewBookForm(forms.Form):
# 	renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

# 	def clean_renewal_date(self):
# 		data = self.cleaned_data['renewal_date']

# 		# Check if a date is not in the past.
# 		if data < datetime.date.today():
# 			return ValidationError(_('Invalid date - renewal in past'))

# 		# Check if a date is in the allowed range (+4 weeks from today).

# 		if data > datetime.date.today() + datetime.timedelta(weeks=4):
# 			return ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

# 		# Remember to always return the cleaned data.
# 		return data


def clean_renewal_date(db_field, **kwargs):		
	import pdb;pdb.set_trace()

	data = db_field.formfield(**kwargs)

	# Check if a date is not in the past.
	if data < datetime.date.today():
		return ValidationError(_('Invalid date - renewal in past'))

	# Check if a date is in the allowed range (+4 weeks from today).

	if data > datetime.date.today() + datetime.timedelta(weeks=4):
		return ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

	# Remember to always return the cleaned data.
	return data
class RenewBookForm(ModelForm):

	class Meta:
		model = BookInstance
		fields = ['due_back']
		labels = {'due_back':(_('New renewal date'))} #we override these fields in mata,
		help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')} # The Meta below shows you how to override these fields,
		# formfield_callback = clean_renewal_date
		# Note: You can also include all fields in the form using fields = '__all__', 
		# or you can use exclude (instead of fields) to specify the fields not to include from the model).
