
# nonstandard libraries
from Bio import Restriction

def get_largest(frags):
    """ Select largest fragment from list of fragements """
    return max(frags, key=len)

def get_smallest(frags):
    """ Select largest fragment from list of fragements """
    return min(frags, key=len)


def get_cuts(seq,enzyme):
    # find enzyme if called by string
    if isinstance(enzyme,str): 
        enzyme = getattr(Restriction,enzyme)
    return seq.number_of_cuts(enzyme)


def plasmid_comparison():
    """ This is going to be hard """
    pass
