from entextractor.extractor import Extractor

url = "https://news.ycombinator.com/"
extractor = Extractor()
clusters = extractor.extract(url)

print "clusters: %s" % len(clusters)
for label, units in clusters.iteritems():
    print "------------------------------------"
    print "%s : %s" % (label, len(units))
    if len(units) == 30: # 30 news articles on the page
        for u in units:
            print str(u)[:200]