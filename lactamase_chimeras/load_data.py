

def chimera2sequence(block_alignment,chimera_seq):
    blocks = sorted(set([p[0] for p in block_alignment]))
    parents = range(len(block_alignment[0][1:]))
    chimera_seq = [int(i)-1 for i in chimera_seq]
    if len(blocks)!=len(chimera_seq):
        print('chimera sequence needs contain the same number of blocks as the block alignment')
        return
    if max(chimera_seq)>max(parents):
        print('too many parents - chimera blocks are not in block alignment')
        return
    sequence = ''.join([pos[chimera_seq[blocks.index(pos[0])]+1] for pos in block_alignment])
    return sequence


def read_alignment(filename):
    file = open(filename).read()
    data = [line for line in file.split('\n') if len(line) > 0 and line[0]!='#'] # remove spaces and comments
    if '>seq_names' in file:
        seq_names = data[data.index('>seq_names')+1:data.index('>alignment')]
    else:
        seq_names = []
    ali_data = data[data.index('>alignment')+1:]
    alignment =  [pos.split()[1:] for pos in ali_data]
    return alignment,seq_names


def read_data(datafile):
    '''reads the standard data file format I have been using'''
    data = open(datafile,'r').read().strip().replace('\t','').split('\n')

    # remove all comments in data file 
    nocomments = [line.split('#')[0].strip() for line in data if len(line.strip())>0 and line.strip()[0]!='#']


    ## get the header
    header_ind = [i for i,row in enumerate(nocomments) if '>header' in row][0] + 1
    header = [h.strip() for h in nocomments[header_ind].split(',')]

    # get the data
    data_ind = [i for i,row in enumerate(nocomments) if '>data' in row][0] + 1
    data = []
    for line in nocomments[data_ind:]:
        d = [e.strip() for e in line.split(',')]
        data.append(d)
    return header,data

notes = """

Data Sources: 

Structure-Guided SCHEMA Recombination of Distantly Related beta-Lactamases
 - 8 block library


Library Analysis of SCHEMA-Guided Protein Recombination
 - 14 block library (not so much data)"""


import pickle

# load block alignment for eight block library
block_alignment, column_names = read_alignment('lactamase_block_alignment.aln')

# load block alignment for 14 block library
block_alignment14, column_names = read_alignment('lactamase14_block_alignment.aln')

# load contacts 
contacts = pickle.load(open('lactamase_contacts.pkl','rb'))

# load binary function data 
names,function_data = read_data('lactamase_function.data')
AAseqs = [chimera2sequence(block_alignment,f[0]) for f in function_data]

# load binary function data for 14 block library
names,function14_data = read_data('lactamase14_function.data')
AAseqs14 = [chimera2sequence(block_alignment14,f[0]) for f in function14_data]
