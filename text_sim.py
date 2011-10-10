
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import csv
from StringIO import StringIO
import subprocess as sp
import os
from nltk.draw.tree import Tree, TreeWidget
from nltk.draw.util import CanvasFrame

senna_path = '/Users/dedan/Downloads/senna/'
sentence = 'My brother has a dog'

# read senna output
p = sp.Popen(['blabla', '-path',  senna_path],
             executable=os.path.join(senna_path, 'senna-osx'),
             stdin=sp.PIPE,
             stdout=sp.PIPE)
tagged = StringIO(p.communicate(sentence)[0])
table = csv.reader(tagged, dialect='excel-tab')

# extract last column
tree_string = ''
for line in table:
    if line:
        tree_string += line[-1]

# replace stars by corresponding word
tree_string = tree_string.replace('*', ' %s ')
tree_string = tree_string % tuple(sentence.split())
print tree_string

# use nltk to create parsetree
treetok = Tree.parse(tree_string)

# show parsetree
cf = CanvasFrame(width=550, height=450, closeenough=2)

tc = TreeWidget(cf.canvas(), treetok, draggable=1,
                node_font=('helvetica', -14, 'bold'),
                leaf_font=('helvetica', -12, 'italic'),
                roof_fill='white', roof_color='black',
                leaf_color='green4', node_color='blue2')
cf.add_widget(tc,10,10)
cf.mainloop()



# nltk.download('brown')

# brown_ic = wordnet_ic.ic('ic-brown.dat')
# semcor_ic = wordnet_ic.ic('ic-semcor.dat')
#
# print wn.synset('leg.n.01').lin_similarity(wn.synset('dog.n.01'), brown_ic)




# (S1(S(NP**)(VP*(NP**))))



