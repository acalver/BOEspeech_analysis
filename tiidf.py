from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_df=1.0,min_df=0.33, ngram_range=(1,2))
vectors = vectorizer.fit_transform(corpus)

feature_names = vectorizer.get_feature_names_out()

def sort_coo(coo_matrix):
    """Sort a dict with highest score"""
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature, score
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results
def get_keywords(vectorizer, feature_names, doc, TOP_K_KEYWORDS):
    """Return top k keywords from a doc using TF-IDF method"""

    #generate tf-idf for the given document
    tf_idf_vector = vectorizer.transform([doc])
    
    #sort the tf-idf vectors by descending order of scores
    sorted_items=sort_coo(tf_idf_vector.tocoo())

    #extract only TOP_K_KEYWORDS
    keywords=extract_topn_from_vector(feature_names,sorted_items,TOP_K_KEYWORDS)
    
    return list(keywords.keys())

result = []
for doc in corpus:
    
    result.append(get_keywords(vectorizer, feature_names, doc, 20))






#%%
from sklearn.feature_extraction.text import CountVectorizer
from numpy import array, log
cv = CountVectorizer()
tf = cv.fit_transform(corpus)
tf = tf.toarray()
tf = log(tf + 1)

dict_of_tokens={i[1]:i[0] for i in vectorizer.vocabulary_.items()}

tfidf_vectors = []  # all deoc vectors by tfidf
for row in vectors:
  tfidf_vectors.append({dict_of_tokens[column]:value for (column,value) in zip(row.indices,row.data)})



doc_sorted_tfidfs =[]  # list of doc features each with tfidf weight
#sort each dict of a document
for dn in tfidf_vectors:
  newD = sorted(dn.items(), key=lambda x: x[1], reverse=True)
  newD = dict(newD)
  doc_sorted_tfidfs.append(newD)



tfidf_kw = [] # get the keyphrases as a list of names without tfidf values
for doc_tfidf in doc_sorted_tfidfs:
    ll = list(doc_tfidf.keys())
    tfidf_kw.append(ll)
    
tfidf_kw[2][:10]
