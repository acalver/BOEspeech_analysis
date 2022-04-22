#handle nltk downloads?

import fitz  # from pymupdf package
import string
import re
import gensim
from gensim import utils
from datetime import datetime

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
            
    #find date of publishing
    pub_date=re.search('[0-9]{1,2} [a-zA-Z]+ [0-9]{4}',cleaned_text)
    pub_date=pub_date.group()
    pub_date = datetime.strptime(pub_date, '%d %B %Y').date()
    pub_date = datetime.strftime(pub_date,'%Y-%m-%d')
            
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
    #rom gensim.parsing.preprocessing import remove_stopwords
    cleaned_text = cleaned_text.lower()
    
    
    
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    tokenised = nltk.word_tokenize(cleaned_text)
    cleaned_text = ' '.join([lemmatizer.lemmatize(words) for words in tokenised])
 
    cleaned_text = remove_stopwords(cleaned_text)
    
    return cleaned_text, pub_date

#taken from source code
#https://github.com/RaRe-Technologies/gensim/blob/d5556ea2700333e07c8605385def94dd96fb2c94/gensim/parsing/preprocessing.py#L71
#function to add words to default stopword list
def remove_stopwords(s):
    new_stops = {'bank', 'england', 'ha', 'wa', 'et', 'al', 'et al',
                 'central', 'uk', 'chart'}
    stops = gensim.parsing.preprocessing.STOPWORDS.union(new_stops)
    s = utils.to_unicode(s)
    return " ".join(w for w in s.split() if w not in stops)

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