
# standard libraries
import os

# nonstandard libraries
from snapgene_reader import snapgene_file_to_dict, snapgene_file_to_seqrecord
from pydna.dseqrecord import Dseqrecord


def get(fname):
    """ Gather all sequences from a file """
    return snapgene_file_to_seqrecord(fname)

def get_all(folder = '/home/pandyr/Dropbox (MIT)/Research/Plasmids'):
    """ Gather all sequence files in fasta folder """
    all_data = {} # initialize storage 
    # Iterate through all files in fasta folder
    for file in os.listdir(folder):
        if file.endswith(".dna"):
            seq = get(folder + '/' + file)
            seqname = get_seqname(file)
            all_data[seqname] = Dseqrecord(seq,linear = False)
    return all_data

def get_seqname(fname):
    """ Grabs file name base """
    base = os.path.basename(fname)
    return os.path.splitext(base)[0]

if __name__ == "__main__":
    print(get_all())

