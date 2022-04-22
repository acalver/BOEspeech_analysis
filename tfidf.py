from sklearn.feature_extraction.text import TfidfVectorizer

def TFIDF(corp):
    
    vectorizer = TfidfVectorizer(max_df=1.0,min_df=0.33, ngram_range=(1,2))
    vectorizer.fit_transform(corp)
    
    feature_names = vectorizer.get_feature_names_out()
    
    return vectorizer, feature_names

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


def corpus_resuts(corp, vectorizer, f_names, top_n):
    
    result = []
    for doc in corp:
        
        result.append(get_keywords(vectorizer, f_names, doc, top_n))

    return result
