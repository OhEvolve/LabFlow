
# homegrown libraries
import plasmids 
import primers 
import inserts 
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
inserts = inserts.get_all()
renzymes = restriction_enzymes.get_all()

vector = seqs['ART-pgRNA-GG']

oligos = [
        inserts['ARTSE-TRAC-Template'],
        inserts['ARTSE-TRBC-Template'],
        inserts['ARTSE-MLRT-PBS-Bridge'],
        ]

possible_plasmids = reactions.golden_gate(vector,*oligos,enzyme = 'BsaI')

print(possible_plasmids)

possible_plasmids.write('ART-pgRNA-complete.dna')


"""
gRNA = seqs['HEK-gRNA_Cloning_Vector']
final = seqs['ART-pgRNA-GG']

psets = [
    (primers['ART-Vector-F'],primers['ART-Vector-R']),
    (primers['ART-Frag1-F'],primers['ART-Frag1-R']),
]

pcr_products = []

for pset in psets:
    product = reactions.pcr(gRNA,*pset)
    pcr_products += [product]

bridge = reactions.anneal(primers['ART-Span0-F'],primers['ART-Span0-R'])

for p in pcr_products:

    print(p.seq)

possible_plasmids = reactions.gibson(pcr_products[0],
                                     pcr_products[1],
                                     bridge,
                                     limit = 20,
                                     only_terminal_overlaps = True)
print(possible_plasmids)

final_plasmid = tools.get_smallest(possible_plasmids)

final_plasmid.write('ART-pgRNA-2.dna')
"""


