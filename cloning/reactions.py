
"""
Utility for all reactions
"""

from Bio import Restriction
from Bio import SeqRecord

def digest(seq,*enzyme_names):

    enzymes = [getattr(Restriction,enz) for enz in enzyme_names]
    frags = seq.cut(*enzymes)

    

