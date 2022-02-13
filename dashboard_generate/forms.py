from django import forms


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class ReportDateRangeForm(forms.Form):
    From = forms.DateField(widget=DatePickerInput)
    To = forms.DateField(widget=DatePickerInput)

    def __init__(self, *args, **kwargs):
        super(ReportDateRangeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
