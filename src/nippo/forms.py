from django import forms
from .models import NippoModel
from bootstrap_datepicker_plus.widgets import DatePickerInput
# from bootstrap_datepicker_plus.widgets import DateTimePickerInput
# import bootstrap_datepicker_plus as datetimepicker

class NippoModelForm(forms.ModelForm):
    date = forms.DateField(
        label="作成日",
        # widget=DateTimePickerInput(format='%Y-%m-%d')
        widget=DatePickerInput(format='%Y-%m-%d')
    )

    class Meta:
        model = NippoModel
        # fields = "__all__"
        # fields = ["title"]
        exclude = ["user"] # user以外を表示

    def __init__(self, user=None, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs["class"] = "form-control"
        self.user = user
        print(self.user)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        nippo_obj = super().save(commit=False)
        if self.user:
            nippo_obj.user = self.user
        if commit:
            nippo_obj.save()
        return nippo_obj

class NippoFormClass(forms.Form):
    title = forms.CharField(label='タイトル', widget=forms.TextInput(attrs={'placeholder':'タイトル...'})) #labelでformの外の表記を変更
    content = forms.CharField(label='内容', widget=forms.Textarea(attrs={'placeholder':'内容...'}))

    # def __init__(self, *args, **kwargs):
    #     print(self.base_fields)
    #     self.base_fields["title"].initial = "base_fields title"
    #     super().__init__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        # print(self.base_fields["title"])
        for field in self.base_fields.values():
            field.widget.attrs.update({"class":"form-control"})
        super().__init__(*args, **kwargs) #継承元を引き継ぐ

