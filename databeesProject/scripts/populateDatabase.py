from categories.models import Category
from transaction.models import Auction, BuyItNow, Item
from account.models import Individual
import random
import sys
import requests
import json
import urllib2
from django.core.files.base import ContentFile
from PIL import Image
from StringIO import StringIO
import datetime
import calendar

# Global Vars
devKey = "DaniyarY-databees-PRD-e38ccab7b-42581944"
itemsPerPage = "50"
dataFormat = "json"

names = ["Bob", "Thomas", "Jeff", "Mark", "Barak"]
lasts = ["Johnson", "Liam", "Carpet", "Obama", "Bush"]

sellersPopulated = True
categoriesPopulated = True
itemsPopulated = False

def download_image(name, image, url):
    try:
        input_file = StringIO(urllib2.urlopen(url).read())
    except urllib2.HTTPError:
        print 'No image for ' + name
    output_file = StringIO()
    img = Image.open(input_file)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(output_file, "JPEG")
    image.save(name+".jpg", ContentFile(output_file.getvalue()), save=False)

def give_random_date():
    sourcedate = datetime.date.today()
    months = random.randrange(1, 12)
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)

totalCategoryIDs = ["15687", "15689", "3001", "11484", "11507", "63861", "11554", "63863", "11538", "11536", "175628", "178962", "163526", "175629", "105417", "155241", "163142", "155252", "155253", "163146", "159037", "36249", "73943", "177909", "73937", "181130", "181153", "181129", "181128", "83041", "179950", "179946", "179973", "180001", "179985", "177831", "158990", "177832", "22679", "177840", "112529", "73839", "15053", "15054", "96954", "175716", "48610", "156955",
                    "168105", "60207", "11711", "14954", "14955", "3314", "38331", "11071", "39804", "175711", "11725", "96969", "176990", "133693", "108298", "176991", "134640", "2032", "75578", "177032", "20498", "177017", "41968", "3187", "20595", "41976", "41986", "20469", "20445", "20450", "175750", "43397", "83880", "74927", "162485", "74922", "162044", "29994", "162045", "29967", "155707", "107894", "182077", "15230", "4201", "29973", "29980", "48515", "69573", "89161", "121464", "155823"]
totalCategoryStrings = ["T-Shirts", "Shorts", "Suits", "Sweaters","Underwear","Dresses", "Jeans", "Pants", "Sweaters","Skirts","Aprons", "Coveralls & Jumpsuits", "Hats", "Jackets & Vests","Lab Coats","Africa", "Europe", "Latin America", "Middle East","Native American","Bowhunting", "Decoys", "Gun Parts", "Blinds & Treestrands","Gun Storage","Golf Clothing, Shoes & Accs", "Golf Clubs & Equipment", "Golf Training Aids", "Golf Accessories","Vintage Golf Equipment","Reels", "Rods", "Terminal Tackle", "Vintage","Fishing Equipment","Bicycles", "Cycling Clothing", "Bicycle Accessories", "Bicycle Frames","Bicycle Electronics","Headphones", "iPods & MP3 Players", "Personal Cassette Players", "Personal CD Players","Portable AM/FM Radios","Car Audio", "Car Alarms & Security", "GPS Units", "Marine Audio","Car Electronics Accessories","Calculators", "Laser Pointers", "Metal Detectors", "Pagers","PDAs","Televisions", "Cable TV Boxes", "DVD & Blu-ray Players", "DVRs, Hard Drive Recorders","Satellite TV Receivers","Bath Accessory Sets", "Mirrors", "Scales", "Medicine Cabinets","Tumblers","Gardening Supplies", "Bird & Wildlife Accessories", "Garden Fencing", "Garden Décor","Garden Structures & Shade","Home Security", "Building & Hardware", "Electrical & Solar", "Doors & Door Hardware","Heating, Cooling & Air","Bed-in-a-Bag", "Bed Pillows", "Bed Skirts", "Blankets & Throws","Pillow Shams","Binoculars & Monoculars", "Telescopes", "Binocular Cases & Accessories", "Telescope Parts & Accessories","Other Binoculars & Telescopes","Accessory Bundles", "Batteries", "Battery Grips", "Cables & Adapters","Cases, Bags & Covers","Darkroom & Developing", "Film Cameras", "Film", "Film Backs & Holders","Lens Boards","Flashes", "Flash Adapters", "Flash Brackets", "Flash Diffusers","Sync Cords"]
categories_list =  [
                            ["Clothing, Shoes & Accessories", 
                                ["Men's Clothing", ["T-Shirts", "Shorts", "Suits", "Sweaters","Underwear"]], 
                                ["Women's Clothing", ["Dresses", "Jeans", "Pants", "Sweaters","Skirts"]], 
                                ["Uniforms & Work Clothing", ["Aprons", "Coveralls & Jumpsuits", "Hats", "Jackets & Vests","Lab Coats"]], 
                                ["Cultural & Ethnic Clothing", ["Africa", "Europe", "Latin America", "Middle East","Native American"]]
                            ],
                            ["Sporting Goods", 
                                ["Hunting", ["Bowhunting", "Decoys", "Gun Parts", "Blinds & Treestrands","Gun Storage"]], 
                                ["Golf", ["Golf Clothing, Shoes & Accs", "Golf Clubs & Equipment", "Golf Training Aids", "Golf Accessories","Vintage Golf Equipment"]], 
                                ["Fishing", ["Reels", "Rods", "Terminal Tackle", "Vintage","Fishing Equipment"]], 
                                ["Cycling", ["Bicycles", "Cycling Clothing", "Bicycle Accessories", "Bicycle Frames","Bicycle Electronics"]]
                            ],
                            ["Consumer Electronics", 
                                ["Portable Audio & Headphones", ["Headphones", "iPods & MP3 Players", "Personal Cassette Players", "Personal CD Players","Portable AM/FM Radios"]], 
                                ["Vehicle Electronics & GPS", ["Car Audio", "Car Alarms & Security", "GPS Units", "Marine Audio","Car Electronics Accessories"]], 
                                ["Gadgets & Other Electronics", ["Calculators", "Laser Pointers", "Metal Detectors", "Pagers","PDAs"]], 
                                ["TV, Video & Home Audio", ["Televisions", "Cable TV Boxes", "DVD & Blu-ray Players", "DVRs, Hard Drive Recorders","Satellite TV Receivers"]]
                            ],
                            ["Home & Garden", 
                                ["Bath", ["Bath Accessory Sets", "Mirrors", "Scales", "Medicine Cabinets","Tumblers"]], 
                                ["Yard & Garden", ["Gardening Supplies", "Bird & Wildlife Accessories", "Garden Fencing", "Garden Décor","Garden Structures & Shade"]], 
                                ["Home Improvement", ["Home Security", "Building & Hardware", "Electrical & Solar", "Doors & Door Hardware","Heating, Cooling & Air"]], 
                                ["Bedding", ["Bed-in-a-Bag", "Bed Pillows", "Bed Skirts", "Blankets & Throws","Pillow Shams"]]
                            ],
                            ["Cameras & Photo", 
                                ["Binoculars & Telescopes", ["Binoculars & Monoculars", "Telescopes", "Binocular Cases & Accessories", "Telescope Parts & Accessories","Other Binoculars & Telescopes"]], 
                                ["Camera & Photo Accessories", ["Accessory Bundles", "Batteries", "Battery Grips", "Cables & Adapters","Cases, Bags & Covers"]], 
                                ["Film Photography", ["Darkroom & Developing", "Film Cameras", "Film", "Film Backs & Holders","Lens Boards"]], 
                                ["Flashes & Flash Accessories", ["Flashes", "Flash Adapters", "Flash Brackets", "Flash Diffusers","Sync Cords"]]
                            ]

                        ]

categories_list_ID =  [
                            ["Clothing, Shoes & Accessories", 
                                ["Men's Clothing", ["15687", "15689", "3001", "11484","11507"]], 
                                ["Women's Clothing", ["63861", "11554", "63863", "11538","11536"]], 
                                ["Uniforms & Work Clothing", ["175628", "178962", "163526", "175629","105417"]], 
                                ["Cultural & Ethnic Clothing", ["155241", "163142", "155252", "155253","163146"]]
                            ],
                            ["Sporting Goods", 
                                ["Hunting", ["159037", "36249", "73943", "177909","73937"]], 
                                ["Golf", ["181130", "181153", "181129", "181128","83041"]], 
                                ["Fishing", ["179950", "179946", "179973", "180001","179985"]], 
                                ["Cycling", ["177831", "158990", "177832", "22679","177840"]]
                            ],
                            ["Consumer Electronics", 
                                ["Portable Audio & Headphones", ["112529", "73839", "15053", "15054","96954"]], 
                                ["Vehicle Electronics & GPS", ["175716", "48610", "156955", "168105","60207"]], 
                                ["Gadgets & Other Electronics", ["11711", "14954", "14955", "3314","38331"]], 
                                ["TV, Video & Home Audio", ["11071", "39804", "175711", "11725","96969"]]
                            ],
                            ["Home & Garden", 
                                ["Bath", ["176990", "133693", "108298", "176991","134640"]], 
                                ["Yard & Garden", ["2032", "75578", "177032", "20498","177017"]], 
                                ["Home Improvement", ["41968", "3187", "20595", "41976","41986"]], 
                                ["Bedding", ["20469", "20445", "20450", "175750","43397"]]
                            ],
                            ["Cameras & Photo", 
                                ["Binoculars & Telescopes", ["83880", "74927", "162485", "74922","162044"]], 
                                ["Camera & Photo Accessories", ["29994", "162045", "29967", "155707","107894"]], 
                                ["Film Photography", ["182077", "15230", "4201", "29973","29980"]], 
                                ["Flashes & Flash Accessories", ["48515", "69573", "89161", "121464","155823"]]
                            ]

                        ]

if categoriesPopulated == False:
    # Populating Categories
    for x in range(0, 5):
        parent = Category(name=categories_list[x][0])
        parent.save()
        for i in range(1, 5):
            child = Category(name=categories_list[x][i][0], parent=parent)
            child.save()
            for j in range(0, 5):
                subChild = Category(name=categories_list[x][i][1][j], parent=child)
                subChild.save()
    print "Finished Populating Categories"

if sellersPopulated == False:
    # Creating Pseudo-Sellers
    seller = []
    for i in range(5):
        individ = Individual(username="seller"+str(i)+"@gmail.com", email="seller"+str(
            i)+"@gmail.com", first_name=names[i], last_name=lasts[i], password="123")
        individ.save()
        seller.append(individ)
    print "Finished Creating Pseudo-Sellers"


def populateItemsWithCategoryID(categoryID):
    # Getting items from Ebay
    requestLink = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.0.0&SECURITY-APPNAME="+devKey+"&RESPONSE-DATA-FORMAT="+dataFormat + \
        "&REST-PAYLOAD&itemFilter(0).name=ListingType&itemFilter(0).value=AuctionWithBIN&itemFilter(1).name=MinPrice&itemFilter(1).value=1.00&itemFilter(1).paramName=Currency&itemFilter(1).paramValue=USD&itemFilter(2).name=HideDuplicateItems&itemFilter(2).value=true&itemFilter(3).name=LocatedIn&itemFilter(3).value=US&categoryId=" + \
        categoryID+"&paginationInput.entriesPerPage="+itemsPerPage + \
        "&outputSelector=PictureURLLarge&descriptionSearch=True"
    reqJSON = requests.get(requestLink).json()
    itemsJSON = reqJSON['findItemsAdvancedResponse'][
        0]['searchResult'][0]['item']
    # Get category name and check if it exists
    category = Category.objects.filter(name=totalCategoryStrings[totalCategoryIDs.index(categoryID)])
    ###
    if Item.objects.filter(category=category[0]).count() < 20:
        for item in itemsJSON:
            title = item['title'][0]
            if 'pictureURLLarge' not in item:
                continue
            picUrl = item['pictureURLLarge'][0]  # picture url
            address = item['location'][0]
            if 'postalCode' in item:
                zip = item['postalCode'][0]
            price = item['listingInfo'][0][
                'buyItNowPrice'][0]['__value__']  # Price
            if not Item.objects.filter(title=title):
                itemEntry = Item(
                    title=title, description=title, category=category[0])
                download_image(itemEntry.title, itemEntry.image, picUrl)
                itemEntry.save()
                for tag in title.lower().replace("--", "").split():
                    itemEntry.keywords.add(tag)
                seller = Individual.objects.filter(email="seller"+str(random.randrange(0, 4))+"@gmail.com")[0]
                if random.randrange(1, 3) == 1:
                    current_bid = float(price)-(float(price)*0.4)
                    AuctionEntry = Auction(seller=seller, item=itemEntry, reserved_price=price, current_bid=current_bid, end_date=give_random_date())
                    AuctionEntry.save()
                else:
                    BuyItNowEntry = BuyItNow(
                        seller=seller, item=itemEntry, sale_price=price)
                    BuyItNowEntry.save()


print "Started populating items. Please wait at least 5 mins. This will take time"
for categoryID in totalCategoryIDs:
    populateItemsWithCategoryID(categoryID)

print "Finished populating items"
