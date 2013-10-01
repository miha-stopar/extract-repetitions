import logging
from BeautifulSoup import BeautifulSoup, Tag
from reps import Reps
from unit import Unit
from repspattern import RepsPattern
import util
from time import time

class Extractor(object):
	def __init__(self, max_pattern_length=8):
		self.max_pattern_length = max_pattern_length
		self.sentences = []
		self._logger = logging.getLogger("extractor")
		self._logger.setLevel(logging.DEBUG)
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		formatter = logging.Formatter('%(message)s')
		ch.setFormatter(formatter)
		self._logger.addHandler(ch)
		self._logger.info("extractor initialized")
		self.candidates = [] # unit candidates found across HTML tags
		self.candidates_by_class = [] # unit candidates found across CSS classes
		self.child_candidates = [] # unit candidates found across HTML tags in the second level (found in grandchildren tags)
		self.child_candidates_by_class = [] # unit candidates found across CSS classes in the second level (found in grandchildren tags)
		self.levels = []
		self.cluster_labels = []
	
	def extract(self, url):
		source = util.get_page_source(url)
		soup = BeautifulSoup(source)
		self.ignore_tags = ["script", "form", "img", "br", "nav"]
		# don't put "sidebar" there as it appears in Twitter as "no-sidebar"
		self.ignore_css = ["menu", "title-nav", "footer", "crumbs", "doc-nav", "navigation", "side-bar", "metadata"] 
		self._traverse(soup.body)
		self._find_levels()
		self.html_body = soup.body
		self.units = []
		self._extract_units()
		self._extract_units_from_children()
		msg = "number of units found by REPS: %s" % len(self.units)
		self._logger.info(msg)
		self._label_units()
		self._extract_irregular_units()
		msg = "number of units found by REPS + irregular units: %s" % len(self.units)
		self._logger.info(msg)
		self._find_hierarchy()
		clusters = self._get_clusters()
		return clusters
	
	def _find_levels(self):
		for c in self.candidates:
			if c.level not in self.levels:
				self.levels.append(c.level)
		for c in self.candidates_by_class:
			if c.level not in self.levels:
				self.levels.append(c.level)
		for c in self.child_candidates:
			if c.level not in self.levels:
				self.levels.append(c.level)
		for c in self.child_candidates_by_class:
			if c.level not in self.levels:
				self.levels.append(c.level)
			
	def _extract_irregular_units(self):
		"""
		Check if some units were overlooked, for example "GET search/tweets" inside "Search" on Twitter API
		"""
		for cluster_label in self.cluster_labels:
			parents = []
			gparents = []
			ggparents = []
			gggparents = []
			cluster_units = filter(lambda x : x.label == cluster_label, self.units)
			us = cluster_units #for debugging
			for unit in cluster_units:
				parents.append(unit.parent)
				gparents.append(unit.parent.parent)
				ggparents.append(unit.parent.parent.parent)
				gggparents.append(unit.parent.parent.parent.parent)
			# what is in common - parent, grand parent, grand grand parent?
			self._logger.info("number of parents: %s" % len(set(parents)))
			self._logger.info("number of grand parents: %s" % len(set(gparents)))
			self._logger.info("number of grand grand parents: %s" % len(set(ggparents)))
			self._logger.info("number of grand grand grand parents: %s" % len(set(gggparents)))
			if len(set(parents)) == 1:
				common_parent = unit.parent
				potential_parents = [unit.parent]
				self._find_irregular(common_parent, potential_parents, cluster_units)
			elif len(set(gparents)) == 1:
				common_parent = unit.parent.parent
				potential_parents = filter(lambda x : isinstance(x, Tag), common_parent.contents)
				name = cluster_units[0].parent.name
				potential_parents = filter(lambda x : x.name == name, potential_parents)
				self._find_irregular(common_parent, potential_parents, cluster_units)
			elif len(set(ggparents)) == 1:
				common_parent = unit.parent.parent.parent
				potential_parents = []
				parent_name = cluster_units[0].parent.name
				gparent_name = cluster_units[0].parent.parent.name
				potential_grand_parents = filter(lambda x : isinstance(x, Tag) and x.name == gparent_name, common_parent.contents)
				for p in potential_grand_parents:
					potential_parents.extend(filter(lambda x : isinstance(x, Tag) and x.name == parent_name, p.contents))
				self._find_irregular(common_parent, potential_parents, cluster_units)
			elif len(set(gggparents)) == 1:
				common_parent = unit.parent.parent.parent.parent
				potential_parents = []
				parent_name = cluster_units[0].parent.name
				gparent_name = cluster_units[0].parent.parent.name
				ggparent_name = cluster_units[0].parent.parent.parent.name
				potential_grand_grand_parents = filter(lambda x : isinstance(x, Tag) and x.name == ggparent_name, common_parent.contents)
				for p in potential_grand_grand_parents:
					ps = filter(lambda x : isinstance(x, Tag) and x.name == gparent_name, p.contents)
					for s in ps:
						potential_parents.extend(filter(lambda x : isinstance(x, Tag) and x.name == parent_name, s.contents))
				self._find_irregular(common_parent, potential_parents, cluster_units)
	
	def _find_irregular(self, common_parent, potential_parents, cluster_units):
		unit = cluster_units[0]
		unit_tags_names = map(lambda x : x.name, unit.tags)
		typ = unit.typ
		unit_length = len(unit.tags) # units in the same cluster are expected to have the same number of tags
		for p in potential_parents:
			units_in_p = filter(lambda x : x.parent == p, cluster_units)
			tags = filter(lambda x : isinstance(x, Tag), p.contents)
			occupied_indices = []
			for un in units_in_p:
				start, stop = un.get_tags_interval()
				occupied_indices.extend(range(start, stop+1))
				if typ == 1:
					count = unit.get_level_one_tags_count()
					occupied_indices.extend(range(start+1, start+count))
			already_checked_instances = []
			for i in range(0, len(tags)):
				if i not in occupied_indices and i not in already_checked_instances:
					new_unit_tags = []
					for j in range(i, i+unit_length):
						if j in occupied_indices or j >= len(tags):
							break
						if tags[j].name in unit_tags_names:
							new_unit_tags.append(tags[j])
							if typ == 1:
								ts = filter(lambda x : isinstance(x, Tag), tags[j].contents)
								new_unit_tags.extend(ts)
						already_checked_instances.append(j)
					new_unit_tags_names = map(lambda x : x.name, new_unit_tags)
					lev = self._levenshtein(unit_tags_names, new_unit_tags_names)
					if abs(len(unit_tags_names) - len(new_unit_tags)) <= 1 and lev <= 1:
						new_unit = Unit(self, p, new_unit_tags, unit.level, typ, unit.pattern, unit.parent_tag_indices)
						new_unit.label = unit.label
						new_unit.irregular = True
						self._logger.info("irregular unit found ---------------------------------")
						self._logger.info("new irregular unit: %s" % new_unit)
						self.units.append(new_unit)
	
	def _levenshtein(self, seq1, seq2):
		oneago = None
		thisrow = range(1, len(seq2) + 1) + [0]
		for x in xrange(len(seq1)):
			twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
			for y in xrange(len(seq2)):
				delcost = oneago[y] + 1
				addcost = thisrow[y - 1] + 1
				subcost = oneago[y - 1] + (seq1[x] != seq2[y])
				thisrow[y] = min(delcost, addcost, subcost)
		return thisrow[len(seq2) - 1]
						
	def _get_detailed_label(self, unit):
		label = "%s" % unit.level
		for t in unit.tags:
			label += " " + t.name + " >"
			children = filter(lambda x : isinstance(x, Tag), t.contents)
			children = map(lambda x : x.name, children)
			if set(children) == set(["li"]):
				label += " " + "m*li"
			elif set(children) == set(["tr"]):
				label += " " + "m*tr"
			else:
				for child in children:
					label += " " + child
		label = label.strip()	
		return label
	
	def _get_label(self, unit):
		label = "%s" % unit.level
		for t in unit.tags:
			label += " " + t.name
			label = label.strip()	
		return label
						
	def _label_units(self):
		for unit in self.units:
			label = self._get_label(unit)
			unit.label = label
			if label not in self.cluster_labels:
				self.cluster_labels.append(label)
		self._logger.info("%s groups of units found" % len(self.cluster_labels))
	
	def _get_clusters(self):
		clusters = {}
		for unit in self.units: 
			if str(unit.label) not in clusters:
				clusters[str(unit.label)] = []
			clusters[str(unit.label)].append(unit)
		return clusters
			
	def _find_hierarchy(self):
		levels = sorted(self.levels, reverse=True)
		for ind, level in enumerate(levels):
			for unit in filter(lambda x : x.level == level, self.units):
				if ind+1 == len(levels):
					break
				levs = levels[ind+1:]
				for lev in levs:
					for parent_unit_candidate in filter(lambda x : x.level == lev, self.units):
						if self._is_unit_in_unit(unit, parent_unit_candidate):
							break
		
	def _is_unit_in_unit(self, unit, parent_candidate):	
		for tag in parent_candidate.tags:
			parents = unit.tags[0].findParents() # only the first tag is checked if in parent_candidate, maybe others should be too
			if tag in parents: 
				parent_candidate.children_units.append(unit)
				return True
		return False
		
	def _extract_units(self):
		"""
		Prepare a dictionary of units - sorted by unit_ids. Units with same unit_id are considered
		to be of the same semantic class (for example "GET statuses/user_timeline" could be part
		of one unit, "GET statuses/retweets/:id" could be another. These two sample Units from 
		Twitter REST API are of the same HTML structure, but are found in different groups - the 
		first one inside "Timelines", the second one inside "Tweets").	
		"""
		for c in self.candidates:
			l = [] # list of units corresponding to this pattern candidate
			element = c.element
			patt = c.pattern[0]
			level = c.level
			starts = c.pattern[1] # index where pattern starts
			tags = filter(lambda x : isinstance(x, Tag), element.contents)
			for s in starts:
				unit = Unit(self, element, tags[s:s+len(patt)], level, 0, patt)
				self._logger.info("Extracted unit: %s" % unit.tags)
				ignore = False
				for el in unit.tags:
					if self._is_to_be_ignored(el):
						ignore = True
						break
				if not ignore:
					l.append(unit)
			self._logger.info("extract_units: %s" % len(l))
			self.units.extend(l)
	
	def _extract_units_from_children(self):
		for c in self.child_candidates:
			l = []
			element = c.element
			patt = c.pattern[0]
			parent_tags_indices = c.parent_tags_indices
			starts = c.pattern[1] # index where pattern starts
			level = c.level
			tags = []
			children = filter(lambda x : isinstance(x, Tag), element.contents)
			for child in children:
				tags.append(child)
				cs = filter(lambda x : isinstance(x, Tag), child.contents)
				tags.extend(cs)
			for s in starts:
				unit = Unit(self, tags[s].parent, tags[s:s+len(patt)], level, 1, patt, parent_tags_indices)
				#self._logger.info("Extracted unit from children: %s" % unit.tags)
				ignore = False
				for el in unit.tags:
					if self._is_to_be_ignored(el):
						ignore = True
						break
				if not ignore:
					l.append(unit)
			self._logger.info("extract_units_from_children: %s" % len(l))
			self.units.extend(l)
			
	def _is_to_be_ignored(self, element):
		attrs_names = map(lambda x : x[1], element.attrs) 
		for n in attrs_names:
			for i in self.ignore_css: 
				if i in n.lower():
					return True
		return False
	
	def _traverse(self, element):
		if self._is_to_be_ignored(element):
			return None
		seq = []
		seq_with_children = []
		children = filter(lambda x : isinstance(x, Tag) and x.name not in self.ignore_tags, element.contents)
		ptrns = []
		allow_start_indices = []
		# doloci kateri indexi v patternu so parenti, rabis recimo v str() od unita
		for child in children:
			self._traverse(child)
			seq.append(str(child.name))
			# check if pattern is hidden inside grandchildren when all children are of the same name:
			grandchildren = filter(lambda x : isinstance(x, Tag) and x.name not in self.ignore_tags, child.contents)
			ptrn = [str(child.name)]
			if len(grandchildren) > 0:
				for gchild in grandchildren:
					ptrn.append(str(gchild.name))
			flat = [y for x in ptrns for y in x]
			allow_start_indices.append(len(flat))
			ptrns.append(ptrn)
			if len(children) > 1:
				seq_with_children.extend(ptrn)
		if allow_start_indices != []:
			allow_start_indices = allow_start_indices[:-1]
		if seq == seq_with_children:
			seq_with_children = []
		reps = Reps()
		patt, _ = reps.find_pattern(seq, consider_html_structure=True, max_pattern_length=8)
		if patt != None:
			self._logger.info("pattern across tags found: %s" % patt[0])
			level = len(element.findParents()) + 1 # level of element children
			reps_pattern = RepsPattern(patt, element, level)
		cpatt, patt_parent_tags_indices = reps.find_pattern(seq_with_children, consider_html_structure=True, 
								max_pattern_length=self.max_pattern_length, allow_start_indices=allow_start_indices)
		if cpatt != None and len(cpatt[0]) == 2:
			cpatt = None
		if cpatt != None:
			self._logger.info("pattern across tags and their children found: %s" % cpatt[0])
			level = len(element.findParents()) + 2 # level of element grand-children
			creps_pattern = RepsPattern(cpatt, element, level, patt_parent_tags_indices)
		if patt != None:
			if cpatt != None:
				if patt[0] == cpatt[0]:
					return
				pcov = reps.coverage(patt, len(seq))
				cpcov = reps.coverage(cpatt, len(seq_with_children))
				pcoverage = float(pcov) / len(seq)
				cpcoverage = float(cpcov) / len(seq_with_children)
				self._logger.info("both - pattern across elements and pattern across elements with their children found")
				self._logger.info("coverage for %s: %s" % (patt[0], pcoverage))
				self._logger.info("coverage for %s: %s" % (cpatt[0], cpcoverage))
				if pcoverage > cpcoverage:
					self._logger.info("pattern %s added" % patt[0])
					self.candidates.append(reps_pattern)
				else:
					self._logger.info("pattern %s added" % cpatt[0])
					self.child_candidates.append(creps_pattern)
				return
			else:
				self._logger.info("pattern %s added" % patt[0])
				self.candidates.append(reps_pattern)
				return
		if cpatt != None:
			self._logger.info("pattern %s added" % cpatt[0])
			self.child_candidates.append(creps_pattern)
				
if __name__ == "__main__":
	url = "https://news.ycombinator.com/"
	t0 = time()
	extractor = Extractor()
	extractor.extract(url)
	duration = time() - t0
	print "duration: %s" % duration





