from django import forms

from .models import Video, Comment


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['content', 'thumbnail', 'title', 'description', 'is_public']


        widgets = {
            "content": forms.FileInput(attrs={"class": "form-control"}),
            "thumbnail": forms.FileInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Title", 'maxlength': '50'}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Description", 'maxlength': '350'}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class VideoEditForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['thumbnail', 'title', 'description', 'is_public']

        widgets = {
            "thumbnail": forms.FileInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Title", 'maxlength': '50'}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Description", 'maxlength': '350'}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({"class": "form-control", "placeholder": "Comment"})


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, max_length=50)
    contact_email = forms.EmailField(required=True, max_length=50, widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your email"}))
    content = forms.CharField(required=True, max_length=200, widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Message"}))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "Message"

        self.fields['contact_name'].widget.attrs.update({"class": "form-control", "placeholder": "Your name"})
