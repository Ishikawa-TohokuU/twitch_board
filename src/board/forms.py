from django import forms
from .models import StreamModel
from bootstrap_datepicker_plus.widgets import DatePickerInput
# from bootstrap_datepicker_plus.widgets import DateTimePickerInput
# import bootstrap_datepicker_plus as datetimepicker



class StreamFormClass(forms.Form):
    content = forms.CharField(label='投稿内容', widget=forms.Textarea(attrs={'placeholder':'投稿内容を入力'}))

    # def __init__(self, *args, **kwargs):
    #     print(self.base_fields)
    #     self.base_fields["title"].initial = "base_fields title"
    #     super().__init__(*args, **kwargs)

    def __init__(self, user=None, *args, **kwargs): # Bootstrapのclassをフォームに適用
        # print(self.base_fields["title"])
        for field in self.base_fields.values():
            field.widget.attrs.update({"class":"form-control"})
        self.user = user
        super().__init__(*args, **kwargs) #継承元を引き継ぐ

