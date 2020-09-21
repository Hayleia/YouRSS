# python 3.7

import os
import json
from requests import get
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import commands

jsonName = 'latestVideos.json'
confName = 'config.json'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# read configuration
if not os.path.exists(confName) or not os.path.isfile(confName):
	print('CONF PATH IS NOT A FILE')
	exit()
with open(confName) as json_file:
	conf = json.load(json_file)
	userIds = conf['users']
	channels = conf['channels']

# read a json that describes what the last video id is for every channel in the list
latestVideos = {}
if os.path.exists(jsonName):
	if not os.path.isfile(jsonName):
		print('JSON PATH IS NOT A FILE')
		exit()
	with open(jsonName) as json_file:
		latestVideos = json.load(json_file)

# get latest videos from channels and check if they match those in json
newVideos = []
for channelId, channelName in channels:
	if channelId == '': continue
	print(f'Processing {channelName}')
	resp = get(f'https://www.youtube.com/feeds/videos.xml?channel_id={channelId}')
	soup = BeautifulSoup(resp.text, "lxml")
	entry = soup.find("entry") # the first one is the most recent
	if entry == None: continue
	videoTitle = entry.find("title").text
	videoId = entry.find("id").text
	videoId = videoId[9::] # remove the 'yt:videoId'
	print(f'Last video: {videoId} -- {videoTitle}')
	if channelId not in latestVideos or latestVideos[channelId] != videoId:
		newVideos.append((channelId, channelName, videoId, videoTitle))

# send messages and update json file
if len(newVideos) != 0:
	async def getDmChannel(user):
		dm_channel = user.dm_channel
		if dm_channel == None: dm_channel = await user.create_dm()
		return dm_channel

	bot = commands.Bot(command_prefix=('notarealbot!'))

	@bot.event
	async def on_ready():
		print('bot has connected')
		for channelId, channelName, videoId, videoTitle in newVideos:
			print(f'New video from {channelName}: {videoTitle}')
			latestVideos[channelId] = videoId
			for userId in userIds:
				if userId == 0: continue
				user = bot.get_user(userId)
				channel = await getDmChannel(user)
				await channel.send(f'New video from {channelName} -- {videoTitle}: <https://youtu.be/{videoId}>')
		await bot.close()

	bot.run(TOKEN)

	with open(jsonName, 'w') as outfile:
		json.dump(latestVideos, outfile)
