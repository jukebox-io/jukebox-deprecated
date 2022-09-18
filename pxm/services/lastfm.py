import pylast

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm
API_KEY = "b25b959554ed76058ac220b7b2e0a026"  # this is a sample key
API_SECRET = "425b55975eed76058ac220b7b4e8a054"

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
)

# Enable cache handling mechanism to avoid duplicate calls to the API endpoint
network.enable_caching()

# Enable rate limiting to ensure uninterrupted services without hitting the max request limit
network.enable_rate_limit()
