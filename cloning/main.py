
import plasmids 
import reactions

from pydna.dseq import Dseq
from pydna.dseqrecord import Dseqrecord

seqs = plasmids.get_all()

pHIV_record = seqs['pHIV-EGFP']
pHIV = Dseqrecord(pHIV_record)

reactions.digest(pHIV,'BamHI')




