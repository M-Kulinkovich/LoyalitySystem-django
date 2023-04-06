from polls.models import Cards
from django.forms import ModelForm


class CardsForm(ModelForm):
    class Meta:
        model = Cards
        fields = ['series_card', 'number_card', 'create_date_card', 'ending_date_card']


