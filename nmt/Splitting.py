
# coding: utf-8

# In[23]:


from random import random
import codecs
import io

k1 = 0
k2 = 0
train_en = io.open("/media/aghabayli/Windows/Users/aghabayli/Documents/NLP/Project/train_enet_en.txt", 'w', encoding="UTF-8")
test_en = io.open("/media/aghabayli/Windows/Users/aghabayli/Documents/NLP/Project/test_enet_en.txt", 'w', encoding="UTF-8")
val_en = io.open("/media/aghabayli/Windows/Users/aghabayli/Documents/NLP/Project/val_enet_en.txt", 'w', encoding="UTF-8")
file1 = io.open("/media/aghabayli/Windows/Users/aghabayli/Documents/NLP/Project/enet_en.txt", 'r', encoding="UTF-8")
file2 = io.open("/media/aghabayli/Windows/Users/aghabayli/Documents/NLP/Project/enet_et.txt", 'r', encoding="UTF-8")
train_ot = io.open("/media/aghabayli/Windows/Users/aghabayli/Documents/NLP/Project/train_enet_et.txt", 'w', encoding="UTF-8")
test_ot = io.open("/media/aghabayli/Windows/Users/aghabayli/Documents/NLP/Project/test_enet_et.txt", 'w', encoding="UTF-8")
val_ot = io.open("/media/aghabayli/Windows/Users/aghabayli/Documents/NLP/Project/val_enet_et.txt", 'w', encoding="UTF-8")




r1 = file1.readline()
r2 = file2.readline()
while r1!="" and r1!=None:
    p = random()
    if(p<=0.3 and k1 < 20000):
        k1+=1
        val_en.write(r1)
        val_ot.write(r2)
    elif (p>0.3 and p<=0.6 and k2< 20000):
        k2+=1
        test_en.write(r1)
        test_ot.write(r2)
    else:
        train_en.write(r1)
        train_ot.write(r2)
    r1 = file1.readline()
    r2 = file2.readline()

file1.close()
file2.close()
val_en.close()
val_ot.close()
test_en.close()
test_ot.close()
train_en.close()
train_ot.close()

