from django.shortcuts import render
from django.http import HttpResponse
import requests
from travelPyLands.models import City,Country,Continent
from travelPyUserStory.models import Story

# Create your views here.


api_token = 'AD0zQHhnAO27dR8Slqocm2FSH4mA4cKp8oSSCh5H'


# send data from api to be rendered in index.html
def home(request):

    indexData_dict = {'topCountries': getTop('country'),
                      'topCities': getTop('city'),
                       'continents': getContinents(),
                      }
    return render(request, "travelPyLands/index.html", context=indexData_dict)


# get one image from api media with any id
def getImageFromApi(id): #-> get high image
    response = requests.get(f'https://api.sygictravelapi.com/1.1/en/places/{id}/media',
                            None, headers={
            'x-api-key': api_token
        })
    imagesData = response.json()
    if len(imagesData["data"]["media"]):
        return imagesData["data"]["media"][0]["url"]
    else:
        return "https://i5.walmartimages.com/asr/f752abb3-1b49-4f99-b68a-7c4d77b45b40_1.39d6c524f6033c7c58bd073db1b99786.jpeg?odnHeight=450&odnWidth=450&odnBg=FFFFFF"

# get top data from api
def getTop(level):
    response = requests.get(f'https://api.sygictravelapi.com/1.1/en/places/list?levels={level}&limit=6',
                                  None, headers={
            'x-api-key': api_token
        })
    data = response.json()
    dataList = addImagesToList(data["data"]["places"])
    return dataList


# add image  from api to any list of dict with image-> as a key and return list with that image
def addImagesToList(lst):
    for items in lst:
        items["image"] = getImageFromApi(items['id'])
    return lst

# get  8 entities from api and return list of them
def getApiList(parent, parentId, level,limit = 9):
    response = requests.get(f'https://api.sygictravelapi.com/1.1/en/places/list?parent={parent}:{parentId}&levels={level}&limit={limit}',
                            None, headers={
            'x-api-key': api_token
        })
    apiData = response.json()
    apiDataList = addImagesToList(apiData["data"]["places"])
    return apiDataList


# send cityPoi from api to be rendered in cityPoi.html
def cityPoi(request,cityId):
    cityId = int(cityId[5:])
    city_stories = Story.objects.filter(city_id = cityId)
    cityPoiData_dict = {'poi':getCityPlacesApi('sightseeing',cityId),
                        'hotels':getCityPlacesApi('sleeping',cityId),
                        # 'cityName':City.objects.filter(id=cityId).first().city_name,
                        'city_stories':city_stories,
                        'cityName':City.objects.filter(id=cityId).first().city_name,
                        'cityId':cityId,
                        'continents': getContinents()}
    return render(request,"travelPyLands/cityPoi.html",context=cityPoiData_dict)



def poiDescription(request,cityId,poiId,poiName):
    poiDesResponse = requests.get(
        f'https://api.sygictravelapi.com/1.1/en/places/{poiId}',
        None, headers={
            'x-api-key': api_token
        })
    print("hoteldes->"+poiName)
    poiDesData = poiDesResponse.json()
    poiDesPlace = poiDesData["data"]["place"]
    poiDesMediaImg = poiDesData["data"]["place"]["main_media"]["media"][0]["url"]
    poiDesData_dict = {'poiDesPlaces':poiDesPlace,
                       'DesMediaImg':poiDesMediaImg,
                       'cityId':cityId,
                       'poiName':poiName,
                       'continents': getContinents()}
    return render(request,"travelPyLands/poiDes.html",context=poiDesData_dict)


def getcountries(request,continentId):
    countriesData_dict = {'countries':getApiList('continent',continentId,'country'),
                          'continents': getContinents()}
    return render(request, "travelPyLands/countries.html",  context=countriesData_dict)


def getcities(request,countryId):
    countryIdInt = int(countryId[8:])
    print(countryId)
    citiesData_dict={'cities':getApiList('country',countryIdInt,'city'),
                     'continents': getContinents()}
    return render(request, "travelPyLands/cities.html", context=citiesData_dict)

def getContinents():
    return Continent.objects.all()

# https://api.sygictravelapi.com/1.1/en/places/list?parents=city:40&categories=sleeping&limit=10

def getCityPlacesApi(category,cityId):
    response = requests.get(
        f'https://api.sygictravelapi.com/1.1/en/places/list?parents=city:{cityId}&categories={category}&limit=9',
        None, headers={
            'x-api-key': api_token
        })
    cityPlacesData = response.json()
    cityPlacesDataList = addImagesToList(cityPlacesData["data"]["places"])
    return cityPlacesDataList
