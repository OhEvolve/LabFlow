
"""
Pulls primers from xlsx
"""

# nonstandard libraries
from openpyxl import load_workbook,Workbook
from pydna.dseq import Dseq


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


