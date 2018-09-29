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
		self.__playlistinfo = []

	#-----------------------------------------------------------------------------------------------------------------

	def playlist_queue(self):
			
		if self.__playlist != []:

			self.__playlist.pop(0)
			self.__playlistinfo.pop(0)

			self.__playlist[0].start()

	#-----------------------------------------------------------------------------------------------------------------

	def play(self, player, title):

		#player = await self.voice_client.create_ytdl_player(url)

		if self.__playlist == []:

			self.__playlist.append(player)
			self.__playlistinfo.append(title)
			self.__playlist[0].start()

		else:

			self.__playlist.append(player)
			self.__playlistinfo.append(title)

	#-----------------------------------------------------------------------------------------------------------------

	def pause(self):

		self.__playlist[0].pause()

	#-----------------------------------------------------------------------------------------------------------------

	def resume(self):

		self.__playlist[0].resume()

	#-----------------------------------------------------------------------------------------------------------------

	def stop(self):

		self.__playlist[0].pause()
		
		for i in range(len(self.__playlistinfo)):

			self.__playlist.pop(i)
			self.__playlistinfo.pop(i)

	#-----------------------------------------------------------------------------------------------------------------

	def skip(self):

		self.__playlist[0].stop()
		self.__playlistinfo.pop(0)

	#-----------------------------------------------------------------------------------------------------------------

	def remove(self, lista):

		tempPlaylist = self.__playlist
		tempPlaylistinfo = self.__playlistinfo

		count = 0

		for i in lista:

			i = int(i)
			i = i - count
			
			if i != 0 : 
				
				tempPlaylist.pop(i)
				tempPlaylistinfo.pop(i)

				count += 1 

		self.__playlist = tempPlaylist
		self.__playlistinfo = tempPlaylistinfo

	#-----------------------------------------------------------------------------------------------------------------

	def queue(self):

		if self.__playlistinfo != []:

			embed = discord.Embed(

				#title = "",
				description = "\n",
				color = discord.Color.red() 

				)

			#embed.set_author(name= "Queue List")
			#embed.set_footer(text= "This is a fotter")

			embed.add_field(name= "Current playing: ", value= self.__playlistinfo[0], inline=False)

			if len(self.__playlistinfo) > 1:

				for i in range(len(self.__playlistinfo)):

					if i != 0:

						embed.add_field(name= str(i) + ": ", value= self.__playlistinfo[i], inline=False)

			return embed

		else:
			return "There are no song playing"

	#----------------------------------------------------------------------

	def randomList(self):

		auxList = []

		for i in range(len(self.__playlistinfo)):

			rndElement = rnd.choice(lista)

			lista.remove(rndElement)
			auxList.append(rndElement)

		return auxList