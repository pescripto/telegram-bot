import feedparser
print("ok import")
feed = feedparser.parse("https://br.cointelegraph.com.br/rss
")
print(len(feed.entries))