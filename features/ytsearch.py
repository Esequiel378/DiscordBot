import requests

def getSearch(search, embed_search=False):

	'''get url and title'''

	NO_RESULT = False

	maxResults = 10
	cout = False

<<<<<<< HEAD
	search_results = []

	url_check = ["https://","www.",".com"]
	
	API_KEY = "AIzaSyAp6LDki7q5NePgwJniTFdxtnKFc1tOazU" #add your API KEY
=======
	url_check = ["https://","www.",".com"]
	#bTitle = ["(", ")", "[", "]"] #Characters to delete

	API_KEY = "APIKEY" #add your API KEY
>>>>>>> 00161010fa5dcaec0a7366f877b2fee761796d00

	for i in range(len(url_check)):

		'''system to detect if its a link or search'''
          
		if url_check[i] in search:

			cout = True
		
			break

	if cout:
		search = search[32:]

	else:
		search = list(search.split(" "))
		search = "+".join(search)

	r = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={}&q={}&key={}"
		.format(maxResults, search, API_KEY)).json() #get data from video link (json)

	for i in range(maxResults):
		
		'''get url and title'''

		try:

			urlId = r['items'][i]['id']['videoId']
			url = "http://www.youtube.com/watch?v=" + urlId

			urlTitle = r['items'][i]['snippet']['title']

			url_info = [url, urlTitle]

			search_results.append(url_info)

		except:
			
			pass
			
	if search_results != []:

		if not embed_search:

			return search_results[0][0], fancy_title(search_results[0][1])
		
		else:

			for i in range(len(search_results)):

				search_results[i][1] = fancy_title(search_results[i][1])

			return search_results

	else:
		return "ERROR", "ERROR"

def fancy_title(urlTitle):

	if "(" and ")" in urlTitle: #delete whatever is inside of brackets
		
		a = urlTitle.find("(")
		b = urlTitle.find(")")

		urlTitle = list(urlTitle)

		for i in range(a,b+1):
			urlTitle.pop(a)

		urlTitle = "".join(urlTitle)

	if "[" and "]" in urlTitle: #delete whatever is inside of square brackets
		
		a = urlTitle.find("[")
		b = urlTitle.find("]")

		urlTitle = list(urlTitle)

		for i in range(a,b+1):
			urlTitle.pop(a)

		urlTitle = "".join(urlTitle)

	if "HD" in urlTitle: #delete HD

		a = urlTitle.find("HD")
		b = a + 2
		
		urlTitle = list(urlTitle)

		for i in range(a, b):
			urlTitle.pop(a)

		urlTitle = "".join(urlTitle)

	if "|" in urlTitle: #delete | simbol

		a = urlTitle.find("|")
		b = a + 1
		
		urlTitle = list(urlTitle)

		for i in range(a, b):
			urlTitle.pop(a)

		urlTitle = "".join(urlTitle)

	if "/" in urlTitle: #delete slash

		a = urlTitle.find("/")
		b = a + 1
		
		urlTitle = list(urlTitle)

		for i in range(a, b):
			urlTitle.pop(a)

		urlTitle = "".join(urlTitle)

	for i in range(len(urlTitle)): #delete double blank spaces

		if "  " in urlTitle:

			a = urlTitle.find("  ")
			b = a + 1
			
			urlTitle = list(urlTitle)

			for i in range(a, b):
				urlTitle.pop(a)

			urlTitle = "".join(urlTitle)

	return urlTitle

if __name__ == "__main__":

<<<<<<< HEAD
	print(getSearch("chloe staffler", embed_search=True))
	print(getSearch("huege laurence unchain my heart")) #error!
=======
	print(getSearch("huege laurence unchain my heart")) #error!
>>>>>>> 00161010fa5dcaec0a7366f877b2fee761796d00
