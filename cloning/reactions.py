
"""
Utility for all reactions
"""

from Bio import Restriction

def digest(seq,*enzyme_names):

    print seq
    print type(seq)

    for enzyme in enzyme_names:
        enz = getattr(Restriction,enzyme)
        frags = enz.catalyse(seq,linear=False)
        #print seq
        for frag in frags:
            print 'Frag:'
            #print frag
            #print frag.toseq()
            print type(frag)
        #print frags


