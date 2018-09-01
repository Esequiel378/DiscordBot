import requests

def getSearch(search):

	'''get url and title'''

	NO_RESULT = False

	maxResults = 20
	cout = False

	url_check = ["https://","www.",".com"]
	#bTitle = ["(", ")", "[", "]"] #Characters to delete

	API_KEY = "APIKEY" #add your API KEY

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

			break
	
		except:
			NO_RESULT = True

	if not NO_RESULT:

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

		for i in range(len(urlTitle)): #delete double blank spaces

			if "  " in urlTitle:

				a = urlTitle.find("  ")
				b = a + 2
				
				urlTitle = list(urlTitle)

				for i in range(a, b):
					urlTitle.pop(a)

				urlTitle = "".join(urlTitle)

		return url, urlTitle

	else:
		return "ERROR", "ERROR"

if __name__ == "__main__":

	print(getSearch("huege laurence unchain my heart")) #error!
