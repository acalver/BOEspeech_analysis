import fitz  # from pymupdf package
import string
import re
import gensim
from gensim import utils
from datetime import datetime
from nltk.stem import WordNetLemmatizer
from  nltk import word_tokenize
from gensim.parsing.preprocessing import remove_stopwords


def import_pdf(file):
    '''
    import speech PDFs and clean the text
    '''
    
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
    
    
    punc = string.punctuation + '’“”‘–' #curly quotes and long dash not included in default
    
    #remove punctuation, digits and standardise case
    cleaned_text = cleaned_text.translate(str.maketrans('', '', punc))
    cleaned_text = cleaned_text.translate(str.maketrans('', '', string.digits))
    cleaned_text = cleaned_text.lower()
    
    cleaned_text = remove_stopwords(cleaned_text)
    
    lemmatizer = WordNetLemmatizer()
    tokenised = word_tokenize(cleaned_text)
    cleaned_text = ' '.join([lemmatizer.lemmatize(words) for words in tokenised])
 
    #manually remove common words specific to the speeches
    cleaned_text = remove_stopwords_manual(cleaned_text)
    
    return cleaned_text, pub_date


#taken from source code
#https://github.com/RaRe-Technologies/gensim/blob/d5556ea2700333e07c8605385def94dd96fb2c94/gensim/parsing/preprocessing.py#L71
def remove_stopwords_manual(s):
    '''
    add words to default stopword list
    '''
    
    new_stops = {'central', 'bank', 'et', 'al', 'et al',
                 'uk', 'chart', 's'}
    stops = gensim.parsing.preprocessing.STOPWORDS.union(new_stops)
    s = utils.to_unicode(s)
    return " ".join(w for w in s.split() if w not in stops)

