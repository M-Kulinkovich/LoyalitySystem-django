# LoyalitySystem-django | Система лояльности бонусных карт

## Installation

### 1. Сlone Repository & Install Packages
```
git clone https://github.com/M-Kulinkovich/LoyalitySystem-django.git
pip install -r requirements.txt
```
### 2. Run tests
```
python manage.py test
```
### 3. Migrate & Start Server
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
### 4. Fill the database with test data
```
python manage.py upload_data
```

## Application Features
* List of cards with fields: series, number, issue date, activity end date, status
* Field search
* View the profile of the card with the history of purchases on it
* Activation & Deactivation cards
* Deleting cards
* Card generator, indicating the series and number of generated cards, and the period of activity
* Changing the status of the card to expired if the validity period has end
