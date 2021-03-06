
# # Populating travelpydb with some data from Sygic Travel api 

# def getImageFromApi(id): #-> get high image
#     response = requests.get(f'https://api.sygictravelapi.com/1.1/en/places/{id}/media',
#                             None, headers={
#             'x-api-key': api_token
#         })
#     imagesData = response.json()
#     return imagesData["data"]["media"][0]["url"]

# # add image  from api to any list of dict with image-> as a key and return list with that image
# def addImagesToList(lst):
#     for items in lst:
#         items["image"] = getImageFromApi(items['id'])
#     return lst


# # get top data from api
# def getTop(level):
#     response = requests.get(f'https://api.sygictravelapi.com/1.1/en/places/list?levels={level}&limit=6',
#                                   None, headers={
#             'x-api-key': api_token
#         })
#     data = response.json()
#     dataList = addImagesToList(data["data"]["places"])
#     return dataList



# # get  8 entities from api and return list of them
# def getApiList(parent, parentId, level):
#     response = requests.get(f'https://api.sygictravelapi.com/1.1/en/places/list?parent={parent}:{parentId}&levels={level}&limit=9',
#                             None, headers={
#             'x-api-key': api_token
#         })
#     apiData = response.json()
#     print(apiData["data"]["places"][0]["id"])
#     apiDataList = addImagesToList(apiData["data"]["places"])
#     return apiDataList

# # send cityPoi from api to be rendered in cityPoi.html
# def cityPoi(request,cityName):
#     city = City.objects.filter(city_name=cityName)
#     cityPoiData_dict = {'poi':getApiList('city',city[0].id,'poi'),
#                         'cityName':cityName,
#                         'continents': getContinents()}
#     return render(request,"travelPyLands/cityPoi.html",context=cityPoiData_dict)

# def poiDescription(request,poiId):
#     poiDesResponse = requests.get(
#         f'https://api.sygictravelapi.com/1.1/en/places/{poiId}',
#         None, headers={
#             'x-api-key': api_token
#         })
#     poiDesData = poiDesResponse.json()
#     poiDesPlace = poiDesData["data"]["place"]
#     poiDesMediaImg = poiDesData["data"]["place"]["main_media"]["media"][0]["url"]
#     poiDesData_dict = {'poiDesPlaces':poiDesPlace,
#                        'DesMediaImg':poiDesMediaImg,
#                        'continents': getContinents()}
#     return render(request,"travelPyLands/poiDes.html",context=poiDesData_dict)



from travelPyLands.models import City,Country,Continent
# 1 - fill continent 
# 2 - fill country in each continent 
# 3 - fill city in each country
# 4 - fill poi in each city


