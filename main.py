from file_import import import_pdf
import glob

corpus=[]
for file in list(glob.glob('*.pdf')):
    corpus.append(import_pdf(file))
