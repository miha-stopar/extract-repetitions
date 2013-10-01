About
=====

Extractor library provides automatic extraction of repeated entities on web pages.

The library can be used as follows (see *tests* folder):
::

	from entextractor.extractor import Extractor
	
	url = "https://news.ycombinator.com/"
	extractor = Extractor()
	clusters = extractor.extract(url)
	
	print "clusters: %s" % len(clusters)
	for label, units in clusters.iteritems():
	    print "------------------------------------------------------------------"
	    print "%s : %s" % (label, len(units))
	    if len(units) == 30: # 30 news articles on the page
	        for u in units:
	            print str(u)[:200]
	           
The output should be something like:
::

	clusters: 2
	6 tr td tr : 2
	9 tr td td td tr td td tr : 30
	1.  Joblint: test tech jobs for sexism, culture, expectations, and recruiter fails (github.com)  80 points by rowanmanning 1 hour ago  | 35 comments
	2.  Programming is Terrible (pastebin.com)  60 points by ibadeyes 2 hours ago  | 37 comments
	3.  Tessel: The end of web development as we know it (slideshare.net)  338 points by Frijol 9 hours ago  | 261 comments
	4.  How to get bias into a Wikipedia article (wikipedia.org)  120 points by dmerfield 6 hours ago  | 46 comments
	5.  Researchers Develop Method for Getting High-Quality Photos from Crappy Lenses (petapixel.com)  89 points by Xcelerate 6 hours ago  | 31 comments
	6.  App Store Pricing: Worth Less than a Cup of Coffee (floriankugler.com)  9 points by floriankugler 1 hour ago  | discuss
	7.  A negative captcha (github.com)  117 points by capex 8 hours ago  | 67 comments
	8.  16-Year Old Arrested Over World’s Biggest Cyber Attack (blog.insecure.in)  16 points by i-hacker 2 hours ago  | 7 comments
	9.  How the FBI found Miss Teen USA’s webcam spy (wired.co.uk)  8 points by r0h1n 1 hour ago  | 3 comments
	10.  Free HTML Starter Templates for Bootstrap (startbootstrap.com)  363 points by jalan 17 hours ago  | 73 comments
	11.  Procrastination should be solved by lighting fires, not filling buckets (visakanv.com)  14 points by visakanv 2 hours ago  | 1 comment
	12.  The Indian and his insatiable appetite for the college degree (medium.com)  67 points by stephenhacking 6 hours ago  | 56 comments
	13.  Gartner tells IT shops that it's 'game over' for BlackBerry (computerworld.com)  15 points by josteink 3 hours ago  | 21 comments
	14.  Turns mailto links into clean contact forms (squaresend.com)  27 points by cmstoken 5 hours ago  | 18 comments
	15.  Devopsdays TLV livestream (livestream.com)  7 points by rantav 1 hour ago  | 1 comment
	16.  An electric superbike (mission-motorcycles.com)  13 points by kvprashant 3 hours ago  | 11 comments
	17.  Newly Declassified Documents Show How the Surveillance State was Born (newrepublic.com)  143 points by tokenadult 13 hours ago  | 25 comments
	18.  Freelan - an open-source, multi-platform, peer-to-peer VPN software (freelan.org)  130 points by bowyakka 14 hours ago  | 59 comments
	19.  What I Wish I Knew Before Studying Computer Security in College (matthewdfuller.com)  70 points by cddotdotslash 10 hours ago  | 49 comments
	20.  Pudb – A full-screen, console-based Python debugger (python.org)  92 points by hartror 13 hours ago  | 22 comments
	21.  Going long long on time_t (openbsd.org)  110 points by hebz0rl 15 hours ago  | 63 comments
	22.  Judge tosses Apple motion, allows patent troll Lodsys to continue rampage (arstechnica.com)  154 points by protomyth 18 hours ago  | 100 comments
	23.  SpaceX Launch - Official Webcast (spacex.com)  224 points by nkoren 22 hours ago  | 143 comments
	24.  How to write a crawler (emanueleminotto.it)  104 points by EmanueleMinotto 16 hours ago  | 23 comments
	25.  Data-Processing Frameworks Benchmark: Redshift, Hive, Shark, Impala (berkeley.edu)  83 points by ceyhunkazel 16 hours ago  | 14 comments
	26.  Bitcoin is Worse is Better (gwern.net)  134 points by gwern 20 hours ago  | 38 comments
	27.  Day 180: Finished (jenniferdewalt.com)  337 points by wallflower 1 day ago  | 84 comments
	28.  Create diagrams in the browser (draw.io)  211 points by gpsarakis 1 day ago  | 41 comments
	29.  Why Free Software Is More Important Now Than Ever Before (wired.com)  360 points by hexis 1 day ago  | 264 comments
	30.  What is the theoretical limit of information density? (stackexchange.com)  55 points by lpage 15 hours ago  | 30 comments


In this context cluster represents a group of repeated entities / units. 
Each unit in a cluster contains the same set of HTML tags and has the following attributes:

* level information (how deep in the HTML structure it is)
* type (type 0 - all tags are of the same depth, type 1 - tags are of the two different levels - parents and their children one level below)
* pattern (for example *tr td td* - the sequence of HTML tags that was found to be repeated)
* parent_tag_indices (indices of the tags which are parents)
* irregular (if True, the unit's pattern is slightly different from the others in cluster, but it appears to be of the very similar structure - for example a cluster of articles might contain one article which doesn't have an image, while the others have it (it lacks the *img* tag) - however, the algorithm doesn't work well if the sequence contains more irregularities)

The code above finds two clusters - the second one is the one that contains actual news, 
the first one is to be ignored (just two occurrences of *tr td tr* pattern which do not represent any meaningful 
entities on the web page).
Usually, some such meaningless clusters appear - 
but it is up to the programmer to filter out the unneeded clusters.
Frequently, some clusters related to web page menus appear too.

Another example might be extracting news from DZone:
::

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


Here we receive even more clusters, however, among them there is one with actual news:
::

	------------------------------------------------------------------
	6 a div div div div div : 25
	4  0   What’s new for ALM in Visual Studio 2013 and Team Foundation Server 2013        martinig vi
	5  0   Applying machine learning to improve your algos        ivom2gi via plumbr.eu    Promoted: Oct
	5  0   Extreme Reality SDK open to all Developers        mannt8 via iapplehow.com    Promoted: Oct 0
	10  0   JavaOne 2013 - Mark Reinhold explains Lambda in Java Technical keynote        markee174 via 
	10  1   10 Web Development Tools for Developers        gavin_dm via codegeekz.com    Promoted: Oct 0
	9  0   Apple Releases iOS 7.0.2 To Fix a pair of Screen Security Bugs        Kaostricks12 via iapple
	11  0   59 Hilarious but True Programming Quotes for Software Developers         garibbu via theprof
	6  1   Programming languages for web development        sbp_romania via sbp-romania.com    Promoted:
	5  0   5 ways devops can benefit IT        vcmilazzo via networkworld.com    Promoted: Oct 01 / 03:1
	6  0   How Google Converted Language Translation Into a Problem of Vector Space Mathematics        d
	6  0   Codenvy’s Architecture, Part 1        piccoloprincipe via infoq.com    Promoted: Oct 01 / 0
	8  0   How to extend enum in Java        Yifan Peng via blog.pengyifan.com    Promoted: Oct 01 / 03:
	7  0   draw.io        dotCore via draw.io    Promoted: Oct 01 / 02:48.
	9  0   How to Improve your WordPress Website for SEO        rajyog via thedesignblitz.com    Promote
	5  0   Add Recommendation Engine in your Ecommerce website with Ruby Backend APIs         vickytambu
	6  0   Intuitiveness Has a New Meaning in Terms of App Design        amicrux via bloggerspath.com   
	9  0   10 Useful WordPress Plugins for Customer Engagement        gavin_dm via webtoolsdepot.com    
	17  0   10 Best CSS Frameworks Which Developers Must Use For Faster Development        smith.steve13
	16  0   10+ Great Web Design Tools Which Designers Should Have In Their Toolbox        smith.steve13
	16  0   8 Must Have Tools For Web Developers to Test and Compare Website Loading Time        crazydz
	7  0   Simplified Releases to the Central Repository with Nexus        mosabua via blog.sonatype.com
	11  0   WordPress 3.6 – Six Useful Hacks that You Still Need        ialisavitti via designfloat.co
	8  0   Idiot's guide to Entity Framework by an idiot        meese200 via blogs.windward.net    Promo
	7  0   AutoCAD DXF Files Reading &amp; Conversion to PDF, Read/Edit Image EXIF Data        sheraz786
	4  0   JavaRoots: How to Set Default Schema In Oracle Using Commons DBCP        somaniab via javaroo
  

Algorithm
======

Repeated entities are discovered using slightly extended REPS algorithm:

Jinbeom Kang, Jaeyoung Yang, Joongmin Choi, “Repetition-based Web Page Segmentation by 
Detecting Tag Patterns for Small-Screen Devices”, IEEE Transactions on Consumer Electronics, 
IEEE, vol. 56, no. 2, pp.980-986, 2010. 

Install
======

::

	pip install -e git+https://miha-stopar@github.com/miha-stopar/extract-repetitions#egg=entextractor



