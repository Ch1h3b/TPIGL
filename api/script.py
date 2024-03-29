from re import sub
from json import loads
from requests import post
from datetime import datetime
strptime = datetime.strptime

LASTSCRAP = "2022-12-10"
TYPES = {"terrain", "appartement", "maison", "villa"}
CATEGS = {"location", "echange", "vente"}
URL = "https://api.ouedkniss.com:443/graphql"


def callAPI(jsonon):
	return loads(post(URL, json=jsonon).text)

def getOne(id):
	
	json={"operationName": "AnnouncementGet", "query": "query AnnouncementGet($id: ID!) {\n  announcement: announcementDetails(id: $id) {\n    id\n    reference\n    title\n    slug\n    description\n    orderExternalUrl\n    createdAt: refreshedAt\n    price\n    pricePreview\n    oldPrice\n    priceType\n    exchangeType\n    priceUnit\n    hasDelivery\n    deliveryType\n    hasPhone\n    hasEmail\n    quantity\n    status\n    street_name\n    category {\n      slug\n      name\n      __typename\n    }\n    defaultMedia(size: ORIGINAL) {\n      mediaUrl\n      __typename\n    }\n    medias(size: LARGE) {\n      mediaUrl\n      mimeType\n      thumbnail\n      __typename\n    }\n    categories {\n      id\n      name\n      slug\n      __typename\n    }\n    specs {\n      specification {\n        label\n        codename\n        type\n        __typename\n      }\n      value\n      valueText\n      __typename\n    }\n    user {\n      id\n      username\n      displayName\n      avatarUrl\n      __typename\n    }\n    isFromStore\n    store {\n      id\n      name\n      slug\n      description\n      imageUrl\n      url\n      followerCount\n      announcementsCount\n      locations {\n        location {\n          address\n          region {\n            slug\n            name\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      categories {\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    cities {\n      id\n      name\n      region {\n        id\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    isCommentEnabled\n    noAdsense\n    variants {\n      id\n      hash\n      specifications {\n        specification {\n          codename\n          label\n          __typename\n        }\n        valueText\n        value\n        mediaUrl\n        __typename\n      }\n      price\n      oldPrice\n      quantity\n      __typename\n    }\n    showAnalytics\n    __typename\n  }\n}\n", "variables": {"id": id}}
	data= callAPI(json)
	data=data["data"]["announcement"]
	

	#General Informations
	title =data["title"]
	price = data["pricePreview"]*1000
	description = data["description"]
	
	space = sub("[^0-9]", "", data["specs"][0]["valueText"][0]) 
	c,w,s = data["cities"][0]["name"] ,data["cities"][0]["region"]["name"],data["street_name"]
	
	#Image Links
	typ="appartement"
	for t in TYPES:
		if t in data["slug"].lower():typ=t
	ctg="vente"
	for t in CATEGS:
		if t in data["slug"].lower():ctg=t


	links = [ media["mediaUrl"] for media in data["medias"]]

	# Lastly, phone and email
	json={"operationName": "UnhidePhone", "query": "query UnhidePhone($id: ID!) {\n  phones: announcementPhoneGet(id: $id) {\n    id\n    phone\n    __typename\n  }\n}\n", "variables": {"id": id}}
	data= callAPI(json)
	phone = data["data"]["phones"][0]["phone"]
	json={"operationName": "UnhideEmail", "query": "query UnhideEmail($id: ID!) {\n  email: announcementEmailGet(id: $id)\n}\n", "variables": {"id": "1266926"}}
	data=callAPI(json)
	email = data["data"]["email"]

	json = {
	"title":title,
    "price":price,
    "description":description.replace("\\n", "\n"),
    "space":space,
    "phone":phone, 
    "email":email,
    "localisation":", ".join([c,w,s]),
    "type":typ,
	"category":ctg,
	"pics":",".join(links),
	
	}
	
	return json

def getAll(l=LASTSCRAP,  total=1, page=1, count=60):
	print("Scrapping now... Operation may take time")
	json={"operationName": "SearchQueryWithoutFilters", "query": "query SearchQueryWithoutFilters($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {\n  search(q: $q, filter: $filter) {\n    announcements {\n      data {\n        ...AnnouncementContent\n        smallDescription {\n          valueText\n          __typename\n        }\n        noAdsense\n        __typename\n      }\n      paginatorInfo {\n        lastPage\n        hasMorePages\n        __typename\n      }\n      __typename\n    }\n    active {\n      category {\n        id\n        name\n        delivery\n        slug\n        __typename\n      }\n      count\n      __typename\n    }\n    suggested {\n      category {\n        id\n        name\n        slug\n        __typename\n      }\n      count\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AnnouncementContent on Announcement {\n  id\n  title\n  slug\n  createdAt: refreshedAt\n  isFromStore\n  isCommentEnabled\n  userReaction {\n    isBookmarked\n    isLiked\n    __typename\n  }\n  hasDelivery\n  deliveryType\n  likeCount\n  description\n  status\n  cities {\n    id\n    name\n    slug\n    region {\n      id\n      name\n      slug\n      __typename\n    }\n    __typename\n  }\n  store {\n    id\n    name\n    slug\n    imageUrl\n    __typename\n  }\n  user {\n    id\n    __typename\n  }\n  defaultMedia(size: $mediaSize) {\n    mediaUrl\n    __typename\n  }\n  price\n  pricePreview\n  priceUnit\n  oldPrice\n  priceType\n  exchangeType\n  __typename\n}\n", "variables": {"filter": {"categorySlug": "immobilier", "cityIds": [], "connected": False, "count": count, "delivery": None, "exchange": False, "fields": [], "hasPictures": False, "hasPrice": False, "origin": None, "page": page, "priceRange": [None, None], "priceUnit": None, "regionIds": []}, "mediaSize": "MEDIUM", "q": None}}
	answer = callAPI(json)	
	
	nice = answer["data"]["search"]["announcements"]["data"]
	
	all = []
	t = 0
	for one in nice:
		createdAt = one["createdAt"]
		id = one["id"]
		
		if strptime(createdAt[:10], "%Y-%m-%d")  > strptime(l, "%Y-%m-%d"):
			tosend=getOne(id)
			tosend["createdAt"]=one["createdAt"][:10]
			all.append(tosend)
			t+=1
			if t==total:break # Remove this break for actual scrapping
 			
	
	return all
