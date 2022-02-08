from django import forms


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class ReportDateRangeForm(forms.Form):
    From = forms.DateField(widget=DatePickerInput)
    To = forms.DateField(widget=DatePickerInput)
