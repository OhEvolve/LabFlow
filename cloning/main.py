
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

pHIV = seqs['pHIV-mCherry-xI']

p1_5 = primers['Add-GG-Frag1-F']
p1_3 = primers['Add-GG-Frag1-R']

p2_5 = primers ['Add-GG-Frag2-F']
p2_3 = primers ['Add-GG-Frag2-R']

for renzyme in renzymes:
    print('{}:{}'.format(renzyme,tools.get_cuts(pHIV,renzyme)))

pHIV_fragments = reactions.digest(pHIV,'XhoI','BspQI')
linear_pHIV = tools.get_largest(pHIV_fragments)

frag1 = reactions.pcr(pHIV,p1_5,p1_3)
frag2 = reactions.pcr(pHIV,p2_5,p2_3)

possible_plasmids = reactions.gibson(linear_pHIV,frag1,frag2,limit = 18)

new_plasmid = tools.get_largest(possible_plasmids)

(pHIV,new_plasmid)

new_plasmid.write("pHIV-mCxI-GG.dna") 












