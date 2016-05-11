from __future__ import unicode_literals
from django.db import models
from django.utils.text import slugify
from account.models import UserProfile
from taggit.managers import TaggableManager
#from abcd import Item

class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey('categories.Category', null=True, blank=True)
    image = models.ImageField(upload_to="uploads/shop/items/")
    keywords = TaggableManager()
    def __unicode__(self):
       return self.title
    class Meta:
        verbose_name = 'Item'

class Sale(models.Model):
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, editable=True)
    seller  = models.ForeignKey(UserProfile, blank=True, editable=True)
    item = models.OneToOneField(Item, blank=True, editable=True)

class Auction(Sale):
    last_bidder = models.ForeignKey(UserProfile, null=True, blank=True)
    reserved_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    def __unicode__(self):
        return self.item.title
    class Meta:
        verbose_name = 'Auction'
    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = slugify(self.item.title)
            self.slug = "-".join((self.slug, str(self.item.id)))
        super(Auction, self).save(*args, **kwargs)

class BuyItNow(Sale):
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __unicode__(self):
        return self.item.title
    class Meta:
        verbose_name = 'BuyItNow'
    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = slugify(self.item.title)
            self.slug = "-".join((self.slug, str(self.item.id)))
        super(BuyItNow, self).save(*args, **kwargs)

class SaleResult(Sale):
    buyer = models.OneToOneField(UserProfile)
    sold_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(auto_now=False, auto_now_add=True)
    #shipping_address = models.ForeignKey(UserProfile.address)
    #delivery_address = models.ForeignKey(UserProfile.address)
    shipping_date = models.DateField(auto_now=False, auto_now_add=False)
    delivery_date = models.DateField(auto_now=False, auto_now_add=False)

class Watch_list(models.Model):
    item = models.ForeignKey(Item)
    watch_by = models.ForeignKey(UserProfile)
    notify_new_bid=models.BooleanField(default=False)
    notify_in_stock=models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Watch List'


