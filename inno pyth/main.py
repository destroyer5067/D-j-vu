import docx2txt
import difflib
import nltk
t1 = docx2txt.process("merge.docx")
t2=docx2txt.process("merge2.docx")
sent_text1=t1.split(';')
sent_text2=t2.split(';')
final_list=[]
count=0
for z in sent_text1:
    for y in sent_text2:
        if z==y:
            final_list.append(z)
            count+=1
seq=difflib.SequenceMatcher(None,t1,t2)
d=seq.ratio()*100
print(d)