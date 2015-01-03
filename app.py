import twitter
import json
import random

from flask import (Flask, render_template, request, 
				   make_response, url_for, redirect)

app = Flask(__name__)

# Twitter Authentication Keys and Tokens
CONSUMER_KEY = 'GET THIS FROM APPS.TWITTER.COM'
CONSUMER_SECRET = 'GET THIS FROM APPS.TWITTER.COM'
OAUTH_TOKEN = 'GET THIS FROM APPS.TWITTER.COM'
OAUTH_TOKEN_SECRET = 'GET THIS FROM APPS.TWITTER.COM'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)


# This will come from the user
def get_query():
	query = ""
	data = get_cookie_data()
	
	if data.has_key('terms') and data['terms'].replace(' ', ''):
		data['terms'] = ('+' + data['terms'].replace(' ', '+')
											.replace('#', '%23')
											.replace('%', '%40'))

	if data.has_key('anti-terms') and data['anti-terms'].replace(' ', ''):
		data['anti-terms'] = ('-' +	data['anti-terms'].replace(' ', '-')
												 	  .replace('#', '%23')
												  	  .replace('%', '%40'))

	if data.has_key('hashtags') and data['hashtags'].replace(' ', ''):
		for item in data['hashtags'].split(' '):
			if not '#' in item:
				item = '#' + item
			data['hashtags'] = '+' + item.replace('#', '%23')
		
	if data.has_key('mentions') and data['mentions'].replace(' ', ''):
		for item in data['mentions'].split(' '):
			if not '@' in item:
				item = '@' + item
			data['mentions'] = '+' + item.replace('@', '%40')
			
	for item in data:
		query += data[item]

	print query
	return query


# API request to twitter for count tweets matching query
def get_tweet_data(query, count):
	print 'twitter search api called'
	# can throw twitter.api.TwitterHTTPError
	return twitter_api.search.tweets(q=query, count=count)


# Get's query data specified by user
def get_cookie_data():
	try:
		data = json.loads(request.cookies.get('query'))
	except TypeError:
		data = {}
	return data


# Returns embeddable tweet code for tweets in a json object
def get_embed(data):
	tweets = []
	for tweet in data['statuses']:
		# can throw twitter.api.TwitterHTTPError
		tweets.append(twitter_api.statuses.oembed(_id=tweet['id'])['html'])
	return tweets


# Returns tweetIDs for all tweets in a twitter json object
def get_tweetIDs(data):
	tweetIDs = []
	for tweet in data['statuses']:
		tweetIDs.append(str(tweet['id_str']))
	return tweetIDs


# Takes json tweet data and all coordinates associated with tweets and returns a list of lists
# of lat lng tuples and associated tweet index [[(lat, lng), index], ...]
# geo data used if not equal to [0.0, 0.0] else the center of the bouding_box of the users' city
def get_locations(data):
	locations = []  # a list of (lat, lng) tuples
	index = 0  # count the number of tweets to make internal links on markers
	for tweet in data['statuses']:
		if tweet['geo'] and tweet['geo']['coordinates'] != [0.0, 0.0]:
			locations.append([tuple(tweet['geo']['coordinates']), index])
		elif tweet['place']:
			locations.append([get_center(tweet['place']['bounding_box']['coordinates']), index])
		index += 1
	return locations


# returns the center of a Twitter bounding box as a (lat, lng) tuple with some random offset
# to prevent overlapping markers
def get_center(box_coords):
	point_A = box_coords[0][0]  # South-West corner of box
	point_B = box_coords[0][1]  # South-East corner of box
	point_D = box_coords[0][3]  # North-West corner of box

	random.seed()  # bookkeaping, seed default is system time
	offset = 0.1  # max offset from center of bounding box

	# Twitter bounding box coords are saved as [longitude, latitude], they are switched back
	# here to work with the google maps api
	latitude = ((point_A[1] + point_D[1]) / 2) + random.random() * offset
	longitude = ((point_A[0] + point_B[0]) / 2) + random.random() * offset

	return (latitude, longitude)
	

@app.route('/')
def index():
	count = 100  # number of tweets to retrieve
	
	# generate dict of tweetIDs
	query = get_query()
	tweetIDs = [] 
	locations = []
	if query:
		tweet_data = get_tweet_data(query, count)
		tweetIDs = get_tweetIDs(tweet_data)
		locations = get_locations(tweet_data)

	print "tweets found: {}/{}".format(len(tweetIDs), count)
	print "locations: {}".format(locations)

	return render_template(
		'index.html', 
		tweetIDs=tweetIDs,
		locations=locations,
		saves=get_cookie_data()
	)

@app.route('/save', methods=['POST'])
def save():	# save query data in cookie
	response = make_response(redirect(url_for('index')))
	data = get_cookie_data()
	data.update(dict(request.form.items()))
	response.set_cookie('query', json.dumps(data))	
	return response


# must set debug=False before public hosting
app.run(debug=True, host='0.0.0.0', port=8000)
