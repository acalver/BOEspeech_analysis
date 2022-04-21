from file_import import import_pdf
import glob

corpus=[]
for file in list(glob.glob('speeches/*.pdf')):
    corpus.append(import_pdf(file))


#based on initial analysis, add stop works 
#bank, england, 
#ha, wa - lemma issue