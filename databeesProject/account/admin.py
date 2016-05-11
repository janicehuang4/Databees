from django.contrib import admin

from django.contrib import admin

from .models import Individual, Company, Address, Rating

admin.site.register(Individual)
admin.site.register(Company)
admin.site.register(Address)
admin.site.register(Rating)

