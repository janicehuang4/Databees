from django.contrib.auth.models import AbstractUser, User
from decimal import Decimal
from django.db import models


class Address(models.Model):
    local_address = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

class UserProfile(AbstractUser):
    telephone = models.CharField(max_length=19, null=True, blank=True)
    profile_description = models.CharField(max_length=1000, null=True, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True)

class Individual(UserProfile):
    GENDER_OPTIONS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )
    gender = models.CharField(max_length=1, choices=GENDER_OPTIONS, null=True, blank=True)
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    annual_income = models.DecimalField(max_digits=7, decimal_places=0, null=True, blank=True)
    class Meta:
        verbose_name = 'Individual'

class Company(UserProfile):
    #Remove first_name last_name
    company_name = models.CharField(max_length=100)
    revenue = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    company_category = models.CharField(max_length=60)
    class Meta:
        verbose_name = 'Company'

class Credit_card(models.Model):
    user=models.ForeignKey(UserProfile)
    number=models.CharField(max_length=50) #I don't think it should be a int. field
    card_type=models.CharField(max_length=10)
    expiration_date=models.DateField(auto_now=False, auto_now_add=False) #can change to MM/YYYY?
    ccv_number=models.CharField(max_length=3) #I don't think it should be a int. field
    class Meta:
        verbose_name = 'credit card'

class Rating(models.Model):
    user=models.ForeignKey(UserProfile)
    given_rating=models.CharField(max_length=100, null=True, blank=True)
    ratee_description=models.CharField(max_length=100, null=True, blank=True)
    rater=models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        verbose_name = 'rating'

class Preferences(models.Model):

    COLOR_OPTIONS = (
        ('White','white'),
        ('Gray', 'Gray'),
        ('Cyan', 'Cyan')
    )

    LANGUAGE_OPTIONS = (
        ('English', 'English'), 
        ('Spanish', 'Spanish')
    )

    user=models.ForeignKey(UserProfile)
    color_scheme=models.CharField(max_length=10, choices=COLOR_OPTIONS, null=True, blank=True)
    lauguage_preference=models.CharField(max_length=10, choices=LANGUAGE_OPTIONS, null=True, blank=True)
    save_search=models.BooleanField(default=False)
    class Meta:
        verbose_name = 'preferences'
