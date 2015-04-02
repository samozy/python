#!/usr/bin/python

# Outputs "periscope_wall.htm" which should be opened with Safari.
# Doesn't seem to work with any other browser for now. Then Safari crashes *shrug*

import json
import sys
from StringIO import StringIO
import commands
import urllib2

# Get these from: https://dev.twitter.com/oauth/
# Need to create an "app" then use OAuth Generator Tool. Figure it out.
oauth_consumer_key = 'NOPE' # Never changes.
oauth_nonce = 'NAH'
oauth_signature = 'LOLWUT'
oauth_token = 'OMGPWNIES' # Never changes.
oauth_timestamp = 'IAMANUMBER'

# Stream configs
max_vids_per_line=10
sounds='muted="muted"' # Blank this var out for.... sounds. Why would you do that?
show_fail=0 # Do you want to see streams that are gone scroll by while the script runs?

# Yep, too lazy to use urllib here
request = commands.getoutput("curl -sS --get 'https://api.twitter.com/1.1/search/tweets.json' --data 'count=100&q=%22LIVE+on+%23Periscope%22&result_type=recent' --header 'Authorization: OAuth oauth_consumer_key=\""+oauth_consumer_key+"\", oauth_nonce=\""+oauth_nonce+"\", oauth_signature=\""+oauth_signature+"\", oauth_signature_method=\"HMAC-SHA1\", oauth_timestamp=\""+oauth_timestamp+"\", oauth_token=\""+oauth_token+"\", oauth_version=\"1.0\"'")

result = request
io = StringIO(str(result))
data = (json.load(io))
urls = []

# Yeah yeah, whatever.
if 'statuses' in data:
  newdata = data['statuses']
  for chunk in newdata:
    try:
      url = (list(chunk['entities']['urls'])[0]['expanded_url']) # omg so dirty.
      if 'periscope.tv' in url:
	    urls.append(url)
    except:
	  # We're done. Don't judge.
	  pass
else:
  print "Your OAUTH creds probably expired."
  sys.exit(1)

print "We have %s possible Periscope streams." % (len(urls))
print "Processing..."

video_urls = []

for link in urls:
  urlswap = link.replace("https://www.periscope.tv/w/", "https://api.periscope.tv/api/v2/getAccessPublic?token=")
  try:
    get_video_url = urllib2.urlopen(urlswap)
  except urllib2.HTTPError, e:
    if show_fail: print "%s %s" % (e.fp.read(), urlswap)
    continue

  data = json.loads(get_video_url.read());
  video_urls.append(data["hls_url"])

# Sort and de-dup list:
video_urls = sorted(set(video_urls))
print "We have %s actual Periscope streams." % (len(video_urls))

wall = open("periscope_wall.htm", "w")
wall.write('<html><body bgcolor="#000000"><table width="100%"><tr>\n')

counter = 0
for vid in video_urls:
  wall.write('<td align="left" valign="top"><video src='+vid+' type="video/mp4" height="320" width="168" autoplay="autoplay" controls '+sounds+'></video></td>\n')
  counter+=1

  # Max videos per line
  if counter == max_vids_per_line:
    wall.write('<tr>\n')
    counter=0

# We're done, lets finish the file.
wall.write('</tr></table></body></html>')
wall.close()

print "Now open 'periscope_wall.htm' with Safari."



