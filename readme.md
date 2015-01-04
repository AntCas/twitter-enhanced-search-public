============
Dependencies: 
============
Flask http://flask.pocoo.org/
twitter https://pypi.python.org/pypi/twitter

========
API Keys
========

You will need to get API keys from Twitter and Google and insert them where
indicated in app.py and template/index.html respectively

====================================
Twitter Streaming Search API Wrapper
====================================

This is a web application made with Flask that wraps the Twitter Search API.
It can support a total of 180 api requests to Twitter per 15 minute window.

If this ever gets traffic (or just for kicks) then twitter supports per-user
authorization which can be implemented by redirecting the user to Twitter to sign in.

Features

	- Search Criteria
		+ include
		+ exclude
		+ @mentions
		+ #hashtags

	- Tweets: Up to 100 tweets matching search displayed at a time

	- Map: All Tweets with location data get plotted on a Google Map


