
# coding: utf-8
# In[18]:


import gzip
import xml.etree.ElementTree as ET
import re
import os
import sys
import codecs



directory_to = ''
diectory_from = ''
langto = sys.argv[1]    #"ka" for Georgian etc. READ FROM COMMAND LINE

#Change for your setup:
alignfiledir = "data/"
alignfile = alignfiledir+"en-"+langto+".xml.gz"    #alignment file
from_f = "data/en"+langto+".en"    #Saves from-language lines
to_f = "data/en"+langto+"."+langto    #Saves to-language lines
from_file = codecs.open(from_f, 'w', encoding="UTF-8", errors='ignore')    #where to write language1
to_file = codecs.open(to_f, 'w', encoding="UTF-8", errors='ignore')    #where to write language2

def inloop(root):
    target_list = list()
    fromDoc=root.attrib['fromDoc']
    toDoc=root.attrib['toDoc']
    target = list()
    for i in root:
        t = i.attrib['xtargets']
        if len(t.split(';')[0])>0 and len(t.split(';')[1])>0:
            target.append(tuple(t.split(';')))
        target_list.append(target)

    #Directories of input
    from_path = 'data/' + fromDoc
    to_path = 'data/' + toDoc

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
    jj=target_list[0][ind1][0].split(" ")
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
            if ind1 == len(target_list[0])-1:   #this file has been completed
                break
            ind1+=1
            ind2=0
            from_file.write(sent+"\n")
            sent=""
            jj=target_list[0][ind1][0].split(" ")
        else:
            ind2+=1 #get more sentences of this alignment
    #TO-FILE
    sent = ""
    ind1=0
    ind2=0
    jj=target_list[0][ind1][1].split(" ")
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
            if ind1 == len(target_list[0])-1:   #this file has been completed
                break
            ind1+=1
            ind2=0
            to_file.write(sent+"\n")
            sent=""
            jj=target_list[0][ind1][1].split(" ")
        else:
            ind2+=1 #get more sentences of this alignment

with gzip.open(alignfile, 'rb') as f:
    part=""
    f.readline()    #xml version
    f.readline()    #doctype cesalign
    f.readline()    #cesalign version
    row = f.readline()
    while row != None and row != "":
        part+=row
        if "</linkGrp>" in row:
            root = ET.fromstring(part)
            inloop(root)
            part=""
        row = f.readline()

from_file.close()
to_file.close()
        


