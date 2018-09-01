import discord
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
		#self.__playlistinfo = []

	#-----------------------------------------------------------------------------------------------------------------

	def playlist_queue(self):
			
		if self.__playlist != []:

			self.__playlist.pop(0)
			#self.__playlistinfo.pop(0)

			self.__playlist[0][0].start()

	#-----------------------------------------------------------------------------------------------------------------

	def isPlaying(self):

		if self.__playlist[0][0].is_playing():

			return True

		else:
			return False

	#-----------------------------------------------------------------------------------------------------------------

	def play(self, player, title):

		#player = await self.voice_client.create_ytdl_player(url)

		playerData = [player, title]

		if self.__playlist == []:

			self.__playlist.append(playerData)
			#self.__playlistinfo.append(title)
			self.__playlist[0][0].start()

		else:

			self.__playlist.append(playerData)
			#self.__playlistinfo.append(title)

	#-----------------------------------------------------------------------------------------------------------------

	def pause(self):

		self.__playlist[0][0].pause()

	#-----------------------------------------------------------------------------------------------------------------

	def resume(self):

		self.__playlist[0][0].resume()

	#-----------------------------------------------------------------------------------------------------------------

	def stop(self):

		self.__playlist[0][0].pause()
		
		for i in range(len(self.__playlist)):

			self.__playlist.pop(i)
			#self.__playlistinfo.pop(i)

	#-----------------------------------------------------------------------------------------------------------------

	def skip(self):

		self.__playlist[0][0].pause()
		self.__playlist.pop(0)

	#-----------------------------------------------------------------------------------------------------------------

	def remove(self, lista):

		tempPlaylist = self.__playlist
		#tempPlaylistinfo = self.__playlistinfo

		count = 0

		for i in lista:

			i = int(i)
			i = i - count
			
			if i != 0: 
				
				tempPlaylist.pop(i)
				#tempPlaylistinfo.pop(i)

				count += 1 

		self.__playlist = tempPlaylist
		#self.__playlistinfo = tempPlaylistinfo

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

		if self.__playlist != []:

			embed = discord.Embed(

				#title = "",
				description = "\n",
				color = discord.Color.red() 

				)

			#embed.set_author(name= "Queue List")
			#embed.set_footer(text= "This is a fotter")

			embed.add_field(name= "Current playing: ", value= self.__playlist[0][1], inline=False)

			if len(self.__playlist) > 1:

				for i in range(len(self.__playlist)):

					if i != 0:

						embed.add_field(name= str(i) + ": ", value= self.__playlist[i][1], inline=False)

			return embed

		else:
			return "There are no song playing"