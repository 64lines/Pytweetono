#!/usr/bin/env python
##############################################
# Author: Julian Alexander Murillo
##############################################
# Lexinerus (GitHub)
##############################################
# Application: Pytweetono 
# PYthon TWEEt TOpic NOtification
# Application that looking for tweets and 
# shows in notifications each certain time.
##############################################
# Date: 22-Oct-2011
##############################################
import feedparser
import os
import sys
import settings
import config
import time
import urllib
from subprocess import Popen, PIPE

class Pytweetono():
	__source = settings.FEED_SOURCE
	__search_word = settings.SEARCH_WORD
	
	# List of all tweets with specified word on
	# settings file.
	def list_tweets(self):
		lst_tweets = []
		encode_word = urllib.urlencode({config.Q_STRING: self.__search_word}) 

		for page in config.PAGE_RANGE:
			feed = feedparser.parse(self.__source % (page, encode_word))
			lst_tweets += feed.entries

		return lst_tweets

	# Show tweet into a notification
	def show_tweet_notification(self, avatar_url, author, tweet):
		temp_path = config.TEMP_PATH
		image_url = avatar_url.split(config.SLASH)
		image_url = image_url[len(image_url) - config.ONE]
		image_url = config.PATH_DIR % (temp_path, image_url)
				
		# Download the image to put on tweet
		image_command = config.WGET_COMMAND % (temp_path, avatar_url)
		os.system(image_command)

		# Show the notification	
		image_url = config.ICON_ARG % image_url	
		args = [author, tweet, image_url]

		command = ExternalApp()
		command.executeCommand(config.NOTIFY_APP, args)

	# Show all tweets on notifications.
	def show_tweets(self, list_tweets):
		for entry in list_tweets:
			avatar_url = entry.links[config.ONE].href
			author = entry.author
			tweet = entry.description
			self.show_tweet_notification(avatar_url, author, tweet)
			time.sleep(settings.SECONDS_BETWEEN_TWEET)

class ExternalApp():
	def executeCommand(self, command, args):
		return Popen([command] + args, stdin=PIPE, stdout=PIPE)

if __name__ == "__main__":
	pytweetono = Pytweetono()
	list_tweets = pytweetono.list_tweets()
	pytweetono.show_tweets(list_tweets)
