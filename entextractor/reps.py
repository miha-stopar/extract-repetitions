from collections import defaultdict

class Reps():
    """
    Repetition-based page segmentation algorithm.
    """
    
    def coverage(self, pattern, full_len):
        # pattern = ('f,a,b', [4, 8]) or pattern = ('div,div,p', [2,5]) or pattern = (["div", "div", "p", [2,5])
        if type(pattern[0]) == list:
            patt = pattern[0]
        else:
            patt = pattern[0].split(",")
        length = len(patt)
        positions = pattern[1]
        c = 0
        for i, pos in enumerate(positions):
            if i+1 < len(positions):
                next_pos = positions[i+1]
            else:
                next_pos = full_len
            diff = next_pos - pos
            if diff < length:
                #print "overlap not allowed"
                c = 0
                break
            c += min(diff, length)
        return c
    
    def _td_not_after_tr(self, x):
        els = x.split(",")
        if "tr" in els and "td" in els:
            if els.index("tr") > els.index("td"):
                return False
        return True
    
    def find_pattern(self, seq, consider_html_structure=False, max_pattern_length=None, allow_start_indices=[]):
        if len(seq) < 4:
            return None, None
        max_patt_size = len(seq) / 2
        seqs = defaultdict(int)
        seqs_start = defaultdict(list)
        patt_parent_tags = {}
        for patt_size in xrange(2, max_patt_size + 1):
            for j in xrange(len(seq) - patt_size + 1):
                patt_cand = seq[j:j+patt_size]
                key = ",".join(patt_cand)
                prev_part = patt_cand[0]
                contains_all_same = True
                for part in patt_cand[1:]:
                    if part != prev_part:
                        contains_all_same = False
                        break
                    prev_part = part
                if not contains_all_same:
                    if allow_start_indices:
                        if j not in allow_start_indices:
                            continue
                    seqs[key] += 1
                    seqs_start[key].append(j)
                    patt_parent_tags[key] = []
                    for l in range(patt_size):
                        if j + l in allow_start_indices:
                            patt_parent_tags[key].append(l)
        candidates = filter(lambda x : len(x[1]) > 1, seqs_start.iteritems())
        max_cov = 0
        winner = None
        cands = []
        if consider_html_structure: 
            cands = filter(lambda x : self._td_not_after_tr(x[0]), candidates)
        if cands == []:
            cands = candidates
        if max_pattern_length:
            cands = filter(lambda x : len(x[0].split(",")) <= max_pattern_length, cands) 
        for i in cands:
            cov = self.coverage(i, len(seq))
            if cov > max_cov:
                winner = i
                max_cov = cov
        wwinner = None
        parent_tags = None
        if winner != None:
            cov = self.coverage(winner, len(seq))
            if cov < len(seq) / 2:
                return None, None
            wwinner = (winner[0].split(","), winner[1])
            parent_tags = patt_parent_tags[winner[0]] 
        return wwinner, parent_tags
        
            
    