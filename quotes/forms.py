from django import forms
from .models import Quote, GENRE_CHOICES
from django.core.exceptions import ValidationError
from django.db.models import Count

class QuoteForm(forms.ModelForm):
    genre = forms.ChoiceField(choices=GENRE_CHOICES)
    text = forms.CharField(widget=forms.Textarea, max_length=5000)
    weight = forms.IntegerField(min_value=1, max_value=10**9, initial=1)

    class Meta:
        model = Quote
        fields = ["text", "source_name", "genre", "author_name", "weight"]

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if not text:
            raise ValidationError("Цитата не может быть пустой")
        if Quote.objects.filter(text__iexact=text).exists():
            raise ValidationError("Такая цитата уже есть")
        return text

    def clean(self):
        cleaned_data = super().clean()
        source_name = cleaned_data.get("source_name")
        if source_name:
            count = Quote.objects.filter(source_name__iexact=source_name).count()
            if count >= 3:
                raise ValidationError("У этого источника уже есть 3 цитаты")
        return cleaned_data