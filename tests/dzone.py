from entextractor.extractor import Extractor

url = "http://www.dzone.com/links/index.html"
extractor = Extractor()
clusters = extractor.extract(url)

print "clusters: %s" % len(clusters)
for label, units in clusters.iteritems():
    print "------------------------------------------------------------------"
    print "%s : %s" % (label, len(units))
    if len(units) == 25:
        for u in units:
            print str(u)[:100]