from file_import import import_pdf
import glob
from tfidf import *

corpus=[]
publishing_dates = []
for file in list(glob.glob('speeches/*.pdf')):
    pdf, d = import_pdf(file)
    corpus.append(pdf)
    publishing_dates.append(d)


#based on initial analysis, add stop works 
#bank, england, 
#ha, wa - lemma issue

TFIDFvectorizer, feature_names = TFIDF(corpus)
results = corpus_resuts(corpus, TFIDFvectorizer, feature_names, 20)

d = dict()
for i in range(len(corpus)):
    
    text=corpus[i].split()
    
    for j in range(len(results[i])):
        tfidf_word = results[i][j]
        count = text.count(tfidf_word)
        
        if tfidf_word in d:
            d[tfidf_word] += count
            
        else:
            d[tfidf_word] = count
