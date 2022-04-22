from file_import import import_pdf
import glob
from tfidf import *
from co_occurance import *
import numpy as np

corpus=[]
publishing_dates = []
for file in list(glob.glob('speeches/*.pdf')):
    pdf, d = import_pdf(file)
    corpus.append(pdf)
    publishing_dates.append(d)


#based on initial analysis, add stop works 
#bank, england, 
#ha, wa - lemma issue

#%% TF-IDF

TFIDFvectorizer, feature_names = TFIDF(corpus)
results = corpus_resuts(corpus, TFIDFvectorizer, feature_names, 10)

def corpus_totals(corp, tfidf_results, top_n):
    totals = dict()
    for i in range(len(corp)):
        
        text=corpus[i].split()
        
        for j in range(len(tfidf_results[i])):
            tfidf_word = tfidf_results[i][j]
            count = text.count(tfidf_word)
            
            if tfidf_word in totals:
                totals[tfidf_word] += count
                
            else:
                totals[tfidf_word] = count
                
    totals = dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))
    totals  = {k: totals[k] for k in list(totals)[:top_n]}
    
    return totals

top_words = corpus_totals(corpus, results, 25)
top_words = pd.DataFrame(top_words.items(), columns=['word','freq'])

import seaborn as sns
from matplotlib import pyplot as plt
sns.set(rc={'figure.figsize':(10.7,5.27)})
sns.barplot(x='word', y='freq', data=top_words)
plt.xticks(rotation=40)
plt.tight_layout()

risks = ['inflation',
         'productivity',
         'risk',
         'growth',
         'pay',
         'capital',
         'wage', 
         'crisis',
         'gap',
         'income',
         'trust',
         'distribution']
#brexit and covid?!

#%% Co Occurance

vocab_dict = build_vocabulary(corpus[1])

co_ocurrence_vectors = pd.DataFrame(
    np.zeros([len(vocab_dict), len(vocab_dict)]),
    index = vocab_dict.keys(),
    columns = vocab_dict.keys()
)


co_ocurrence_vectors = build_context(corpus[1], 5, co_ocurrence_vectors)
co_ocurrence_vectors.loc['crisis'].sort_values(ascending=False).head(10)
