from aylienapiclient import textapi
client = textapi.Client("5d834bba", "af862fd166c8a114cdc864a65ce00b8e")

def suggest(text):
    hashtags = client.Hashtags({"text": text})
    hashtags=', '.join(hashtags['hashtags'])
    if len(hashtags)<2:
        hashtags="No major topics discussed"
    return hashtags
