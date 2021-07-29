import pandas as pd
import nltk
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class Preprocess():
    def __init__(self,data):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        self.data = data
        self.result = self.sastrawi(self.filtering(self.tokenizing(self.caseFolding())))
        

    def caseFolding(self):
        return self.data.translate(str.maketrans('','',string.punctuation)).lower()
    
    def tokenizing(self, data):
        token = nltk.tokenize.word_tokenize(data)
        return token

    def filtering(self, data):
        ta_stopwords_list=open('ta_stopwords_list.txt', 'r+')
        saya = ta_stopwords_list.read()
        saya=word_tokenize(saya)
        return [word for word in data if not word in saya]

    def sastrawi(self, data):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        return  [(stemmer.stem(token)) for token in data]  
        


# data = "Apa latar belakang Jepang membagi wilayah Indonesia menjadi tiga pemerintahan militer ?"
# p = Preprocess(data)
# print(p.res)        