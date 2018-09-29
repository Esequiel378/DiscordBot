import random as rnd
import youtube_dl

def create_media(server, channel):

	server = mediaPlayer(server, channel)

	return server

class mediaPlayer():
	
	def __init__(self, server, channel):

		self.__server = server
		self.__channel = channel
		self.__playlist = []

	#-----------------------------------------------------------------------------------------------------------------

	def playlist_queue(self):
		
		self.__playlist.pop(0)

		self.__playlist[0][0].start()

	#-----------------------------------------------------------------------------------------------------------------

	def isPlaying(self):

		if self.__playlist[0][0].is_playing():

			return True

		else:
			return False

	#-----------------------------------------------------------------------------------------------------------------

	def play(self, player, title):

		playerData = [player, title]

		if self.__playlist == []:

			self.__playlist.append(playerData)
			self.__playlist[0][0].start()

		else:

			self.__playlist.append(playerData)

	#-----------------------------------------------------------------------------------------------------------------

	def pause(self):

		self.__playlist[0][0].pause()

	#-----------------------------------------------------------------------------------------------------------------

	def resume(self):

		self.__playlist[0][0].resume()

	#-----------------------------------------------------------------------------------------------------------------

	def stop(self):

		self.__playlist[0][0].stop()
		
		for i in range(len(self.__playlist)):

			self.__playlist.pop(i)

	#-----------------------------------------------------------------------------------------------------------------

	def skip(self):

		self.__playlist[0][0].stop()
		self.__playlist.pop(0)

	#-----------------------------------------------------------------------------------------------------------------

	def remove(self, lista):

		tempPlaylist = self.__playlist

		count = 0

		for i in lista:

			try:

				i = int(i)
				i = i - count

			except:
				continue
			
			if i != 0: 
				
				tempPlaylist.pop(i)

				count += 1 

		self.__playlist = tempPlaylist

	#----------------------------------------------------------------------

	def sort(self):

		auxList = []
		auxPList = self.__playlist

		auxList.append(auxPList[0])
		auxPList.pop(0)

		for i in range(len(auxPList)):

			rndElement = rnd.choice(auxPList)

			auxPList.remove(rndElement)
			auxList.append(rndElement)

		self.__playlist = auxList

	#-----------------------------------------------------------------------------------------------------------------

	def queue(self):

		return self.__playlist

	#-----------------------------------------------------------------------------------------------------------------

	def isEmpty(self):

		if self.__playlist == []:

			return True

		else:
			return False