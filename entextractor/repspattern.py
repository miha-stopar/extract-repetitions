class RepsPattern(object):
    def __init__(self, pattern, element, level, parent_tags_indices=None):
        self.pattern = pattern # format is (['div,div,p'], [2,5]) - TODO: fix this
        self.element = element
        self.level = level
        self.parent_tags_indices = parent_tags_indices
        
    def __str__(self):
        text = "RepsPattern - pattern: %s, element name: %s, level: %s" % (self.pattern, self.element.name, self.level)
        return text
    
    def get_coverage(self):
        cov = len(self.pattern[0]) * len(self.pattern[1])
        return cov