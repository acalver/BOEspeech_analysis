def build_vocabulary(text):
    '''
    Builds vocabulary with all the words
    present in the list page.
    '''
    text=text.split()
    vocab = list(set(text))
    vocab.sort()
    
    vocab_dict = {}
    for index, word in enumerate(vocab):
        vocab_dict[word] = index
    return vocab_dict

vocab_dict = build_vocabulary(corpus[0])

co_ocurrence_vectors = pd.DataFrame(
    np.zeros([len(vocab_dict), len(vocab_dict)]),
    index = vocab_dict.keys(),
    columns = vocab_dict.keys()
)

def build_context(
    text:str, 
    window,
    co_ocurrence_vectors: pd.DataFrame
) -> pd.DataFrame:
    '''
    Updates co-ocurrence vectors based on
    text read from the page.
    '''
    text = text.split()
    for index, element in enumerate(text):
        # Build start and finish of context
        start = 0 if index-window < 0 else index-window
        finish = len(text) if index+window > len(text) else index+window+1
        # Retrieve Context for word
        if index -2 < 0:
            context = text[:1] + text[index+1:finish]
        else:
            context = text[start:index]+text[index+1:finish]
        for word in context:
            # Update Co-Occurrence Matrix 
            co_ocurrence_vectors.loc[element, word] = (
                co_ocurrence_vectors.loc[element, word]+1
            )
            
    return co_ocurrence_vectors

co_ocurrence_vectors_2 = build_context(corpus[0], 5, co_ocurrence_vectors)

co_ocurrence_vectors.loc['inflation'].sort_values(ascending=False).head(10)
