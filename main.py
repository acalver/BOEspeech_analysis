from file_import import import_pdf
import glob

corpus=[]
publishing_dates = []
for file in list(glob.glob('speeches/*.pdf')):
    pdf, d = import_pdf(file)
    corpus.append(pdf)
    publishing_dates.append(d)


#based on initial analysis, add stop works 
#bank, england, 
#ha, wa - lemma issue