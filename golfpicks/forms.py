from django import forms
from golfpicks.models import Pick
from django.core.exceptions import ValidationError

class PickForm(forms.ModelForm):
    class Meta:
        model = Pick
        fields = ['event', 'punter', 'picks']

    def clean(self):
        """
        Check there's exactly 3 picks
        """
        cleaned_data=super(PickForm, self).clean()
        picks = self.cleaned_data.get('picks')

        if len(picks) != 3:
            raise ValidationError("Should have exactly 3 picks")

        return cleaned_data