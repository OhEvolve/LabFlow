
"""
Utility for all reactions
"""

from Bio import Restriction
#from Bio import SeqRecord

from pydna.dseqrecord import Dseqrecord
from pydna import amplify
#from pydna.design import assembly_fragments
from pydna.assembly import Assembly

def digest(seq,*enzyme_names):
    """ Forward digest reaction """
    if not isinstance(seq,Dseqrecord):
        raise TypeError('Sequence is not Dseqrecord')
    enzymes = [getattr(Restriction,enz) for enz in enzyme_names]
    return seq.cut(*enzymes)

def pcr(template,*primers):
    """ Forward PCR reaction w/ primers and template """
    return amplify.pcr(primers,template)

def gibson(*fragments,limit = 18):
    """ Forward Gibson reaction for fragments with overlaps """
    products = Assembly(fragments,limit = 18)
    return products.circular_products
    

