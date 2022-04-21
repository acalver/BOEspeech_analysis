#handle nltk downloads?

import fitz  # from pymupdf package
import string
import re

def import_pdf(file):
    
    with fitz.open(file) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
            
    #remove references at end of document and page numbers
    cleaned_text=''
    for line in text.split('\n'):
        if not re.search('^[0-9]+\\.', line) and not re.search('^Page [0-9]+', line):
            cleaned_text += line + '\n'
            
    #repeated in some pdfs
    cleaned_text = re.sub(r"All speeches are available online at www.bankofengland.co.uk.*", "", cleaned_text)
    
    import nltk
    #from nltk.tokenize import word_tokenize
    #remove punctuation and numbers
    #stopwords = nltk.corpus.stopwords.words('english')
    
    #punc = string.punctuation.replace('.', '')
    punc = string.punctuation + '’“”‘' #curly quotes not included in default
    
    cleaned_text = cleaned_text.translate(str.maketrans('', '', punc))
    cleaned_text = cleaned_text.translate(str.maketrans('', '', string.digits))
    
    #remove stopwords
    from gensim.parsing.preprocessing import remove_stopwords
    cleaned_text = cleaned_text.lower()
    cleaned_text = remove_stopwords(cleaned_text)
    
    
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    tokenised = nltk.word_tokenize(cleaned_text)
    cleaned_text = ' '.join([lemmatizer.lemmatize(words) for words in tokenised])
 
    return cleaned_text


#%%
'''
from rake_nltk import Rake
nltk.download('stopwords')
nltk.download('punkt')

# Uses stopwords for english from NLTK, and all puntuation characters by
# default
r = Rake(max_length=2)

# Extraction given the text.
r.extract_keywords_from_text(cleaned_text)

len(r.get_ranked_phrases())


r.get_ranked_phrases_with_scores()[0:100]


r.get_word_frequency_distribution()['covid']
r.get_word_degrees()['brexit']
'''