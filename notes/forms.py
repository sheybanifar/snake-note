from django import forms

from .models import Note, Category

class NoteCreateForm(forms.ModelForm):
    existing_category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        label='Select a category'
    )

    new_category = forms.CharField(
        required=False,
        label='Or create a new category'
    )

    class Meta:
        model = Note
        fields = ['title', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.pop('user', None)

        if self.user:
            self.fields['existing_category'].queryset = Category.objects.filter(user=self.user)

    def clean(self):
        super().clean()

        existing = self.cleaned_data.get('existing_category')
        new_category = self.cleaned_data.get('new_category')

        if not existing and not new_category:
            forms.ValidationError(
                'Error! You should select a category, or create one!'
            )

        if existing:
            self.cleaned_data['final_category'] = existing
        else:
            self.cleaned_data['final_category'] = new_category

        return self.cleaned_data

    def save(self, commit = True):
        instance = super().save(False)
        cd_category = self.cleaned_data.get('final_category')

        if isinstance(cd_category, Category):
            instance.category = cd_category
        else:
            instance.category = Category.objects.create(
                name=cd_category, user=self.user
            )

        if commit:
            instance.save()
        return instance