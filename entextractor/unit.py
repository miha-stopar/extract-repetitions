import util
from BeautifulSoup import Tag

class Unit(object):
    """
    Unit is a set of elements (for example [p, p, div]) which is found to be repeated.
    """
    def __init__(self, crawler, parent, tags, level, typ, pattern, parent_tag_indices=None):
        self.crawler = crawler
        self.parent = parent
        self.tags = tags
        self.level = level
        self.typ = typ # 0 - all tags of the same level (depth), 1 - tags and their children
        self.pattern = pattern
        self.parent_tag_indices = parent_tag_indices # tags which are of the higher level if typ = 1
        self.children_units = []
        self.irregular = False
        self.label = None
        
    def __unicode__(self):
        text = ""
        if self.typ == 0:
            for tag in self.tags:
                text += " " + util.text_from_el(tag)
        else:
            for ind, tag in enumerate(self.tags):
                if ind not in self.parent_tag_indices:
                    text += " " + util.text_from_el(tag)
        return text.strip()

    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def get_tags_interval(self):
        """
        Get the position of this unit's tags inside parent element.
        """
        tags_in_parent = filter(lambda x : isinstance(x, Tag), self.parent.contents)
        start = 0
        stop = 0
        ind = 0
        if len(self.tags) == 1:
            index = tags_in_parent.index(self.tags[0])
            return (index, index)
        for t in tags_in_parent:
            if t == self.tags[0]:
                start = ind
            if t == self.tags[-1]:
                stop = ind
                break
            ind += 1
        if stop < start: # needed for units which have one element and some of its children
            stop = start
        return (start, stop)
    
    def get_level_one_tags_count(self):
        tags_in_parent = filter(lambda x : isinstance(x, Tag), self.parent.contents)
        count = 0
        for t in self.tags:
            if t in tags_in_parent:
                count += 1
        return count
        

        
        
