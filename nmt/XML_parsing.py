
# coding: utf-8
# In[18]:


import gzip
import xml.etree.ElementTree as ET
import re
import os
import sys
import codecs

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

from_file = codecs.open(from_f, 'w', encoding="UTF-8", errors='ignore')
to_file = codecs.open(to_f, 'w', encoding="UTF-8", errors='ignore')

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
    #FROM-FILE
    sent = ""
    ind1=0
    ind2=0
    jj=target_list[i][ind1][0].split(" ")
    for ind_s in range(len(root_from)):
        s=root_from[ind_s]
        if s.tag!="s":  #wrong tag
            continue
        if int(s.attrib["id"])>int(jj[ind2]):
            ind_s-=int(s.attrib["id"])-int(jj[ind2])+1
            continue
        if s.attrib["id"]==jj[ind2]:
            for w in s:
                if w.tag!="w":
                    continue
                sent+=w.text+" "
            sent = re.sub(r'\s+([?.!",\'])', r'\1', sent)
            if ind2==len(jj)-1: #this alignment has been completed
                if ind1 == len(target_list[i])-1:   #this file has been completed
                    break
                ind1+=1
                ind2=0
                from_file.write(sent)
                sent=""
                jj=target_list[i][ind1][0].split(" ")
            else:
                ind2+=1 #get more sentences of this alignment
    #TO-FILE
    sent = ""
    ind1=0
    ind2=0
    jj=target_list[i][ind1][1].split(" ")
    for ind_s in range(len(root_to)):
        s=root_to[ind_s]
        if s.tag!="s":  #wrong tag
            continue
        if int(s.attrib["id"])>int(jj[ind2]):
            ind_s-=int(s.attrib["id"])-int(jj[ind2])+1
            continue
        if s.attrib["id"]==jj[ind2]:
            for w in s:
                if w.tag!="w":
                    continue
                sent+=w.text+" "
            sent = re.sub(r'\s+([?.!",\'])', r'\1', sent)
            if ind2==len(jj)-1: #this alignment has been completed
                if ind1 == len(target_list[i])-1:   #this file has been completed
                    break
                ind1+=1
                ind2=0
                to_file.write(sent)
                sent=""
                jj=target_list[i][ind1][1].split(" ")
            else:
                ind2+=1 #get more sentences of this alignment
from_file.close()
to_file.close()
        
"""
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
"""
from_file.close()
to_file.close()
        

