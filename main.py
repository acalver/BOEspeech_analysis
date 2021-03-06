from file_import import import_pdf
import glob
from tfidf import *
from co_occurance import *
import numpy as np
import pandas as  pd

corpus=[]
publishing_dates = []
for file in list(glob.glob('speeches/*.pdf')):
    pdf, d = import_pdf(file)
    corpus.append(pdf)
    publishing_dates.append(d)


#%% TF-IDF

TFIDFvectorizer, feature_names = TFIDF(corpus)
results = corpus_resuts(corpus, TFIDFvectorizer, feature_names, 10)

def corpus_totals(corp, tfidf_results, top_n):
    '''
    Count the frequency of each TF-IDF result in the corresponding speech
    add these and select the top 25 words
    '''
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
plt.show()

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


#Time series plot
def risks_time_series(corp, risk, dates):
    '''
    Count the frequency of each risk term in each document
    join to the date of the speech to create a time series
    for each risk term
    '''
    time_series = pd.DataFrame(columns=['Date', 'Freq', 'Risk'])
    
    for r in risk:
        r_count = []
        
        for doc in corp:
            r_count.append(doc.count(r))
        
        r_ts = pd.DataFrame([dates, r_count]).transpose()
        r_ts.columns = ['Date', 'Freq']
        r_ts['Risk'] = r
        
        time_series = time_series.append(r_ts)
        
    return time_series

risk_ts = risks_time_series(corpus, risks)

#wide data for  plotting
risk_ts = risk_ts.pivot("Date", "Risk", "Freq")
sns.set(rc={'figure.figsize':(10.7,5.27)})
sns.lineplot(data=risk_ts, dashes=False)
plt.xticks('')
plt.show()

#%% Co Occurance

highest_coo = pd.DataFrame()

def top_coocurrance_words(doc, target):
    '''
    Generate a co-occurrance matrix of each speech
    select the top 10 co-occurance terms with the target risk word
    '''
    
    vocab_dict = build_vocabulary(doc)
    
    if target in vocab_dict.keys():
    
        #blank matrix of 0s
        co_ocurrence_vectors = pd.DataFrame(
            np.zeros([len(vocab_dict), len(vocab_dict)]),
            index = vocab_dict.keys(),
            columns = vocab_dict.keys()
        )
        
        co_ocurrence_vectors = build_context(doc, 5, co_ocurrence_vectors)
        
        #generate dataframe of top 10 co-occurance words
        top_words = co_ocurrence_vectors.loc[target].sort_values(ascending=False).head(10)
        top_words = top_words.rename('Freq')
        top_words = pd.DataFrame(top_words)
        top_words = top_words.rename_axis('Co-Oc').reset_index()
        top_words['Target'] = target
        
        return top_words

risk_terms = ['risk', 'crisis', 'uncertainty']

for target in risk_terms:
    for doc in corpus:
        
        top_values = top_coocurrance_words(doc, target)
        highest_coo = highest_coo.append(top_values)

#sum repeated terms
highest_coo = highest_coo.groupby(['Target', 'Co-Oc']).sum().sort_values('Freq', ascending=False)
highest_coo = highest_coo.reset_index('Co-Oc')

#select top 20 co-occurrancd words for each target risk term
coo_top20 = highest_coo.groupby('Target').head(20)

for rt in risk_terms:
    title = 'Top 20 terms within 5 words of: ' + rt
    sns.barplot(data=coo_top20.loc[rt], x='Co-Oc', y='Freq').set_title(title)    
    plt.xticks(rotation=40)
    plt.show()