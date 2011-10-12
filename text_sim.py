
import os
import csv
from StringIO import StringIO
import subprocess as sp
from nltk.draw.tree import Tree, TreeWidget
from nltk.draw.util import CanvasFrame
import Pyro4
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic

semcor_ic = wordnet_ic.ic('ic-semcor.dat')
brown_ic = wordnet_ic.ic('ic-brown.dat')

sentence1 = 'My brother has a dog with four legs'
sentence2 = 'My brother has four legs'

def extract_last_column(table):
    """extract last column of the table"""
    tree_string = ''
    for line in table:
        if line:
            tree_string += line[-1]
    return tree_string

def get_parsetree(senna_out, sentence):
    """get the nltk parsetree for a senna output"""
    table = csv.reader(StringIO(senna_out), dialect='excel-tab')
    # replace stars by corresponding word
    tree_string = extract_last_column(table)
    tree_string = tree_string.replace('*', ' %s ')
    tree_string = tree_string % tuple(sentence.split())
    return Tree.parse(tree_string)

def mean_lin_sim(word1, word2, ic, pos):
    """compute the mean similarity (LIN measure) of two words

        because one word can has many meanings,
        the mean sense similarity is computed
    """
    sets1 = wn.synsets(word1, pos=pos)
    sets2 = wn.synsets('leg', pos=pos)

    res = []
    for s1 in sets1:
        for s2 in sets2:
            res.append(s1.lin_similarity(s2, brown_ic))
    return np.mean(np.array(res))




senna_server = Pyro4.Proxy("PYRONAME:servers.senna")

treetok1 = get_parsetree(senna_server.tag(sentence1), sentence1)
treetok2 = get_parsetree(senna_server.tag(sentence2), sentence2)

# show parsetree
cf = CanvasFrame(width=550, height=450, closeenough=2)
tc1 = TreeWidget(cf.canvas(), treetok1, draggable=1,
                node_font=('helvetica', -14, 'bold'),
                leaf_font=('helvetica', -12, 'italic'),
                roof_fill='white', roof_color='black',
                leaf_color='green4', node_color='blue2')
tc2 = TreeWidget(cf.canvas(), treetok2, draggable=1,
                node_font=('helvetica', -14, 'bold'),
                leaf_font=('helvetica', -12, 'italic'),
                roof_fill='white', roof_color='black',
                leaf_color='green4', node_color='blue2')

cf.add_widget(tc1,10,10)
cf.add_widget(tc2,290,10)
cf.mainloop()




