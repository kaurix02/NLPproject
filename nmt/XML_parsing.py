
# coding: utf-8

# In[18]:


import gzip
import xml.etree.ElementTree as ET
import re
import os


fromDoc = []
toDoc = []
target_list = list()

directory_to = ''
diectory_from = ''


with gzip.open('en-ka.xml.gz', 'rb') as f:
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


for i  in range (len(fromDoc)):
    #Directories of input
    from_path = '/home/aghabayli/Documents/NLP/Project/en/OpenSubtitles2018/xml/' + fromDoc[i]
    to_path = '/home/aghabayli/Documents/NLP/Project/OpenSubtitles2018/xml/' + toDoc[i]
    #print 324
    
    #Directories of output
    from_file = open('From_dir' + "_".join(fromDoc[i].split('/'))+'.txt', 'w')
    to_file = open('To_dir' + "_".join(toDoc[i].split('/')) + '.txt', 'w')
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
        

