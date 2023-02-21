from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import CardsForm
from .models import *
import random


def index_page(request):
    cards = Cards.objects.all()

    search = request.GET.get('search', '')
    if search:
        cards = Cards.objects.filter(Q(number_card__icontains=search) |
                                     Q(series_card__icontains=search) |
                                     Q(status_card__icontains=search) |
                                     Q(create_date_card__icontains=search) |
                                     Q(ending_date_card__icontains=search)
                                     )
    else:
        cards = Cards.objects.all()
    return render(request, 'index.html', {'cards': cards})


def remote_cards_page(request):
    cards = Cards.objects.all()
    return render(request, 'remoteCard.html', {'cards': cards})


def generate_cards_page(request):
    error = ''
    if request.method == 'POST':
        form = CardsForm(request.POST)
        if form.is_valid():
            series = form.cleaned_data['series_card']
            number = form.cleaned_data['number_card']
            create_date = form.cleaned_data['create_date_card']
            ending_date = form.cleaned_data['ending_date_card']
            cards = []
            for i in range(number):
                card_number = random.randint(10000, 99999)
                card = Cards(series_card=series, number_card=card_number, create_date_card=create_date, ending_date_card=ending_date)
                card.save()
                cards.append(card)
            return redirect('index')
    else:
        form = CardsForm()
        data = {
                'form': form,
                'error': error
            }
    return render(request, 'generateCard.html', {'form': form})


def cards_info(request, cards_id):
    cards = get_object_or_404(Cards, id=cards_id)
    cards.update_status()
    orders = cards.orders.all()
    products = [product for order in orders for product in order.products.all()]
    if request.method == "POST":
        if "active" in request.POST:
            cards.status_card = Cards.ACTIVE
        elif "inactive" in request.POST:
            cards.status_card = Cards.INACTIVE
        elif "delete" in request.POST:
            cards.delete()
            return redirect('/')
        cards.save()
    return render(request, "cards.html", {"cards": cards, "orders": orders, 'products': products})
