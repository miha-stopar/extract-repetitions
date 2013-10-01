About
=====

Extractor library provides automatic extraction of repeated entities (sequence of HTML tags) on web pages.

The library can be used as follows (see *tests* folder):
::

	from entextractor.extractor import Extractor
	
	url = "https://news.ycombinator.com/"
	extractor = Extractor()
	clusters = extractor.extract(url)
	
	print "clusters: %s" % len(clusters)
	for label, units in clusters.iteritems():
	    print "%s : %s" % (label, len(units))
	    if len(units) == 30: # 30 news articles on the page
	        for u in units:
	            print str(u)[:200]
	           
The output should be something like:
::

	clusters: 2
	6 tr td tr : 2
	9 tr td td td tr td td tr : 30
	1.  A 3D printed toothbrush for all your teeth (3ders.org)  121 points by jschwartz11 1 hour ago  | 64 comments
	2.  Fingerprints are Usernames, not Passwords (dustinkirkland.com)  57 points by jcastro 1 hour ago  | 20 comments
	3.  How traffic actually works (jliszka.github.io)  125 points by jliszka 3 hours ago  | 99 comments
	4.  Monitor your Website’s Uptime with Google Docs (labnol.org)  115 points by blueatlas 3 hours ago  | 32 comments
	5.  The Six Stages of Debugging (2012) (plasmasturm.org)  41 points by wodow 2 hours ago  | 4 comments
	6.  D3.js: How to handle dynamic JSON Data (pothibo.com)  100 points by pothibo 4 hours ago  | 11 comments
	7.  Rethinking Agile in an office-less world (37signals.com)  27 points by mh_ 1 hour ago  | 13 comments
	8.  Write less (getnashty.com)  28 points by bgnm2000 1 hour ago  | 24 comments
	9.  Computational Synesthesia: Audio Analysis with Image Processing Algorithms (minardi.org)  57 points by doctoboggan 3 hours ago  | 14 comments
	10.  Show HN: Ridiculously fast and responsive notetaking meets semantic search (hiroapp.com)  8 points by sushimako 10 minutes ago  | discuss
	11.  JavaScript Allongé is free (braythwayt.com)  76 points by raganwald 4 hours ago  | 31 comments
	12.  Easing Functions Cheat Sheet (easings.net)  40 points by bpierre 2 hours ago  | 11 comments
	13.  Firefox fixes save gigabytes of memory on image-heavy pages (mozilla.org)  295 points by AndrewDucker 10 hours ago  | 101 comments
	14.  Conscientiousness and online education (gwern.net)  48 points by gwern 3 hours ago  | 17 comments
	15.  Ask HN: Who is hiring? (October 2013)  249 points by whoishiring 5 hours ago  | 330 comments
	16.  Goodbye Wholesale Brands (jamiequint.com)  25 points by jamiequint 2 hours ago  | 10 comments
	17.  Using ElasticSearch and Logstash to Serve Billions of Searchable Events (elasticsearch.org)  26 points by twakefield 2 hours ago  | 16 comments
	18.  Show HN: Anomalous – Real-time monitoring for servers, applications, and logs (getanomalous.com)  29 points by toddpersen 2 hours ago  | 19 comments
	19.  Why we use Balanced for payments. (apixchange.com)  15 points by jsonne 1 hour ago  | 4 comments
	20.  Unicorns at GitHub (github.com)  22 points by lukashed 1 hour ago  | 22 comments
	21.  Ruby Association: ruby-lang.org Design Contest (ruby.or.jp)  13 points by jgnatch 1 hour ago  | 5 comments
	22.  Scribd Challenges Amazon and Apple With ‘Netflix for Books’ (wired.com)  46 points by gotosleep 4 hours ago  | 29 comments
	23.  Memory – Part 4: Intersec’s custom allocators (intersec.com)  106 points by fruneau 8 hours ago  | 45 comments
	24.  Google Web Designer (google.com)  1010 points by jaysonlane 1 day ago  | 412 comments
	25.  AngelList – Do Or Do Not, There is No Try (foundrygroup.com)  43 points by elias12 5 hours ago  | 2 comments
	26.  A case for something, anything more simple than WordPress (getbarley.com)  20 points by cdevroe 3 hours ago  | 20 comments
	27.  Lego Calendar syncs with Google Calendar (creativeapplications.net)  86 points by thecosas 7 hours ago  | 20 comments
	28.  Naked mole rats have more than one weapon against aging (nationalgeographic.com)  59 points by bane 5 hours ago  | 11 comments
	29.  Rubber Ducky Logs (jamie-wong.com)  19 points by phleet 3 hours ago  | 6 comments
	30.  Challenging the Bing It On Challenge (freakonomics.com)  89 points by msrpotus 2 hours ago  | 40 comments

Cluster represents a group of repeated entities / units. 
Each unit in a cluster contains the same set of HTML tags and has the following attributes:

* level information (how deep in the HTML structure it is)
* type (type 0 - all tags are of the same depth; type 1 - tags are of the two different levels - parents and their children one level below)
* pattern (for example *tr td td* - the sequence of HTML tags that was found to be repeated)
* parent_tag_indices (indices of the tags which are parents)
* irregular (if True, the unit's pattern is slightly different from the others in cluster, but it appears to be of the very similar structure - for example a cluster of articles might contain one article which doesn't have an image, while the others have it (it lacks the *img* tag) - however, the algorithm doesn't work well if the sequence contains more irregularities)

The code above finds two clusters - the second one is the one that contains actual news, 
the first one is to be ignored (just two occurrences of *tr td tr* pattern which do not represent any meaningful 
entities on the web page).
Usually, some such meaningless clusters appear - 
it is up to the programmer to filter out the unneeded clusters.
Frequently, some clusters related to web page menus appear too.

Another example might be extracting news from DZone:
::

	from entextractor.extractor import Extractor
	
	url = "http://www.dzone.com/links/index.html"
	extractor = Extractor()
	clusters = extractor.extract(url)
	
	print "clusters: %s" % len(clusters)
	for label, units in clusters.iteritems():
	    print "%s : %s" % (label, len(units))
	    if len(units) == 25:
	        for u in units:
	            print str(u)[:100]


Here we receive even more clusters, however, among them there is one with actual news:
::

	div div div div div : 25
	5  0   Add Geolocation feature in your Windows Mobile App        vickytambule via api.shephertz.com 
	6  0   Pro T-SQL 2012 Programmer’s Guide        Kaostricks12 via i-programmer.info    Promoted: Oc
	9  0   Git + Dropbox, The Easy Way        piccoloprincipe via nosleep.ca    Promoted: Oct 01 / 10:37
	6  0   80+ Best jQuery Plugin &amp; Tutorial with Demo of September 2013        sanchitsoni via jque
	12  0   The 10x developer is NOT a myth        dotCore via brikis98.blogspot.com    Promoted: Oct 01
	4  0   World’s Smallest NoSQL Database: Persistent Data        mitchp via architects.dzone.com    
	4  0   JVM Toolkit &quot;Ratpack&quot; and Neo4j        mitchp via java.dzone.com    Promoted: Oct 0
	4  0   Aggregation Vs Composition Vs Association        swetagupta via guruzon.com    Promoted: Oct 
	5  0   Ripple is officially open-source!        dotCore via ripple.com    Promoted: Oct 01 / 08:49.
	5  0   A quick post about depression and software development        mswatcher via tosbourn.com    P
	3  1   Menus with Apache Digester        mitchp via java.dzone.com    Promoted: Oct 01 / 08:49.
	4  0   Making HTTPs Requests in Ruby &amp; JavaScript w/ Node.js        mitchp via ruby.dzone.com   
	3  0   OpenStack: The Community Today        mitchp via architects.dzone.com    Promoted: Oct 01 / 0
	3  0   Software Defined (In-) Security        mitchp via server.dzone.com    Promoted: Oct 01 / 08:4
	6  0   Migrating Real-World Million-Line Code Bases to Java 7        martinig via java-tv.com    Pro
	5  0   What’s new for ALM in Visual Studio 2013 and Team Foundation Server 2013        martinig vi
	7  0   Applying machine learning to improve your algos        ivom2gi via plumbr.eu    Promoted: Oct
	7  0   Extreme Reality SDK open to all Developers        mannt8 via iapplehow.com    Promoted: Oct 0
	12  0   JavaOne 2013 - Mark Reinhold explains Lambda in Java Technical keynote        markee174 via 
	12  1   10 Web Development Tools for Developers        gavin_dm via codegeekz.com    Promoted: Oct 0
	11  0   Apple Releases iOS 7.0.2 To Fix a pair of Screen Security Bugs        Kaostricks12 via iappl
	17  0   59 Hilarious but True Programming Quotes for Software Developers        garibbu via theprofe
	7  1   Programming languages for web development        sbp_romania via sbp-romania.com    Promoted:
	6  0   5 ways devops can benefit IT        vcmilazzo via networkworld.com    Promoted: Oct 01 / 03:1
	7  0   How Google Converted Language Translation Into a Problem of Vector Space Mathematics        

Algorithm
======

Repeated entities are discovered using slightly extended REPS algorithm:

Jinbeom Kang, Jaeyoung Yang, Joongmin Choi, “Repetition-based Web Page Segmentation by 
Detecting Tag Patterns for Small-Screen Devices”, IEEE Transactions on Consumer Electronics, 
IEEE, vol. 56, no. 2, pp.980-986, 2010. 

Install
======

::

	pip install -e git://github.com/miha-stopar/extract-repetitions#egg=entextractor



