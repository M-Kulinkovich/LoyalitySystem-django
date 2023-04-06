from rest_framework import serializers
from polls.models import Cards


class CardsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cards
        fields = '__all__'
