
import plasmids 
import primers 
import reactions

from pydna.dseq import Dseq
from pydna.dseqrecord import Dseqrecord
#from pydna.amplify import pcr

seqs = plasmids.get_all()
primers = primers.get_all()

pHIV = seqs['pHIV-mCherry-xI']

p1_5 = primers['Add-GG-Frag1-F']
p1_3 = primers['Add-GG-Frag1-R']

p2_5 = primers ['Add-GG-Frag2-F']
p2_3 = primers ['Add-GG-Frag2-R']

pHIV_fragments = reactions.digest(pHIV,'XhoI','BspQI')
linear_pHIV = max(pHIV_fragments, key=len)

frag1 = reactions.pcr(pHIV,p1_5,p1_3)
frag2 = reactions.pcr(pHIV,p2_5,p2_3)

reactions.gibson(linear_pHIV,frag1,frag2,limit = 18)



print('Amplicon:')









