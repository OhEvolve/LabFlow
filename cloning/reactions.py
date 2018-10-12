
"""
Utility for all reactions
"""

import tools

from Bio import Restriction
#from Bio import SeqRecord

from pydna.dseqrecord import Dseqrecord
from pydna import amplify
from pydna import assembly 
#from pydna.design import assembly_fragments
from pydna.assembly import Assembly
from pydna.amplicon import Amplicon 


def digest(seq,*enzyme_names):
    """ Forward digest reaction """
    if not isinstance(seq,Dseqrecord):
        raise TypeError('Sequence is not Dseqrecord')
    enzymes = [getattr(Restriction,enz) for enz in enzyme_names]
    products = seq.cut(*enzymes)
    if products == []:
        print('WARNING: No cut performed w/ {}'.format(enzymes))
        return seq
    return products

def anneal(f_primer,r_primer):
    """ Forward PCR reaction w/ primers and template """
    # TODO: create checks for actual seq
    return Amplicon(f_primer)

def pcr(template,*primers):
    """ Forward PCR reaction w/ primers and template """
    return amplify.pcr(primers,template)

def gibson(*fragments,limit = 18):
    """ Forward Gibson reaction for fragments with overlaps """
    products = Assembly(fragments,limit = 18)
    print(products)
    return products.circular_products

def golden_gate(*elements,enzyme = 'BspQI'):
    """ Forward Gibson reaction for fragments with overlaps """
    fragments = []
    for element in elements:
        product = digest(element,enzyme)
        fragments += [tools.get_largest(product)]
    products = Assembly(fragments,limit = 4,only_terminal_overlaps = True)
    circ = products.circular_products
    if len(circ) > 1:
        print('WARNING: {} circular plasmids detected, returning largest.'.format(circ))
    if len(circ) == 0:
        print('WARNING: no circular plasmids detected.')
        return None
    return tools.get_largest(circ) 
    

