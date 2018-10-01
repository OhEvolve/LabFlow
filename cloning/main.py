
import plasmids 
import reactions

seqs = plasmids.get_all()

pHIV_record = seqs['pHIV-EGFP']
pHIV = pHIV_record.seq.tomutable()

reactions.digest(pHIV,'BamHI')
#print seqs




