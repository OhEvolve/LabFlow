
# standard libraries
import os
from openpyxl import load_workbook,Workbook

# nonstandard libraries
from pydna.dseq import Dseq
from pydna.dseqrecord import Dseqrecord


def get_all(fname = '/home/pandyr/Dropbox (MIT)/Research/Primers.xlsx'):
    """ Gather all sequence files in fasta folder """
    all_data = {} # initialize storage 
    # Iterate through all files in fasta folder
    wb = load_workbook(filename=fname,read_only=True)

    for ws in wb:
        for index,row in enumerate(ws.rows):
            if index == 0: continue # skip first row
            name = str(row[1].value)
            seq = str(row[2].value)
            all_data[name] = Dseq(seq) 

    return all_data

def get_seqname(fname):
    """ Grabs file name base """
    base = os.path.basename(fname)
    return os.path.splitext(base)[0]

if __name__ == "__main__":
    print(get_all())

