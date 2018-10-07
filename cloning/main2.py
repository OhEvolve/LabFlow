
# homegrown libraries
import plasmids 
import primers 
import restriction_enzymes 

import reactions
import tools

# nonstandard libraries
from pydna.dseq import Dseq
from pydna.dseqrecord import Dseqrecord

from Bio import pairwise2

"""
Available functions:
    >>> reactions.digest(sequence,*cutsites)
    >>> reactions.pcr(seq_template,primer1,primer2)
    >>> reactions.gibson(seq_template,primer1,primer2,limit = homology_int)
    >>> tools.get_largest(sequence_list)
"""

seqs = plasmids.get_all()
primers = primers.get_all()
renzymes = restriction_enzymes.get_all()

gRNA = seqs['HEK-gRNA_2site_Cloning_Vector']
pHIV = seqs['pHIV-mCherry-xI-GG']

psets = [
    (primers['pgRNA-GG-0-F'],primers['pgRNA-GG-1-R']),
    (primers['pgRNA-GG-1-F'],primers['pgRNA-GG-2-R']),
    (primers['pgRNA-GG-2-F'],primers['pgRNA-GG-0-R'])
]

pcr_products = []

for pset in psets:
    product = reactions.pcr(gRNA,*pset)
    pcr_products += [product]

possible_plasmids = reactions.golden_gate(pHIV,*pcr_products,enzyme = 'Esp3I')

final_plasmid = tools.get_largest(possible_plasmids)

final_plasmid.write('Complete.dna')


