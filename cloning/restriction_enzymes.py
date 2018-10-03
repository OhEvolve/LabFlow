
"""
Pulls primers from xlsx
"""

# nonstandard libraries
from openpyxl import load_workbook,Workbook

def get_all(fname = '/home/pandyr/Dropbox (MIT)/Research/Enzymes.xlsx'):
    """ Gather all sequence files in fasta folder """
    all_data = {} # initialize storage 
    # Iterate through all files in fasta folder
    wb = load_workbook(filename=fname,read_only=True)

    ws = wb['Restriction Enzymes']

    for index,row in enumerate(ws.rows):
        if index == 0: continue # skip first row
        name = str(row[0].value)
        distributor = str(row[1].value)
        protocol = str(row[1].value)
        all_data[name] = {
                'distributor':distributor,
                'protocol':protocol,
                }

    return all_data


