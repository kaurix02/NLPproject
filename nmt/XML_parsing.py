
# coding: utf-8
# In[18]:


import gzip
import xml.etree.ElementTree as ET
import re
import os
import sys

fromDoc = []
toDoc = []
target_list = list()

directory_to = ''
diectory_from = ''
langto = sys.argv[1]	#"ka" for Georgian etc. READ FROM COMMAND LINE

#Change for your setup:
alignfiledir = "data/"
alignfile = alignfiledir+"en-"+langto+".xml.gz"	#alignment file
from_f = "data/en"+langto+".en"	#Saves from-language lines
to_f = "data/en"+langto+"."+langto	#Saves to-language lines


with gzip.open(alignfile, 'rb') as f:
    tree = ET.parse(f)
    root = tree.getroot()
    #file_content = f.read()



#root.findall()

for child in root:
    fromDoc.append(child.attrib['fromDoc'])
    toDoc.append(child.attrib['toDoc'])
    target = list()
    for i in child:
        t = i.attrib['xtargets']
        if len(t.split(';')[0])>0 and len(t.split(';')[1])>0:
            target.append(tuple(t.split(';')))
    target_list.append(target)

#print target_list[0]   

from_file = open(from_f, 'w')
to_file = open(to_f, 'w')

for i  in range (len(fromDoc)):
    #Directories of input
    from_path = 'data/' + fromDoc[i]
    to_path = 'data/' + toDoc[i]
    #print 324
    
    #Directories of output
    

    with gzip.open(from_path, 'rb') as f:
        tree_from = ET.parse(f, ET.XMLParser(encoding='utf-8'))
        root_from = tree_from.getroot()
    with gzip.open(to_path, 'rb') as f:
        tree_to = ET.parse(f, ET.XMLParser(encoding='utf-8'))
        root_to = tree_to.getroot()
    #print 9234
    for j in target_list[i]:
        #print 45
        #print j[1]
        #root_from.find("[@id = '{0}']".format(j[0]))
        for i in j[1].split():
            to_sent = root_to.findall(".//s[@id='{0}']/w".format(i))
            s = ''
            for sent in to_sent:
                s+=sent.text + ' '
            s = re.sub(r'\s+([?.!",\'])', r'\1', s)
                #to_file.write(sent.text.encode('utf-8') + ' ')
            to_file.write(s.encode('utf-8'))
        to_file.write("\n")
        
        for i in j[0].split():
            #print i
            from_sent = root_from.findall(".//s[@id='{0}']/w".format(i))
            s = ''
            for sent in from_sent:
                s+=sent.text + ' '
            s = re.sub(r'\s+([?.!",\'])', r'\1', s)
            from_file.write(s.encode('utf-8'))
        from_file.write("\n")
from_file.close()
to_file.close()
        

