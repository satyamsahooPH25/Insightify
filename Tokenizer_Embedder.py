import nltk
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import nltk
import numpy as np
from nltk.corpus import stopwords
import gensim
from gensim.utils import simple_preprocess
import nltk
from tensorflow import keras
import gensim
from gensim.models import Word2Vec
import numpy as np
import tensorflow as tf
class Vectorizer:
    def __init__(self):
        self.model=gensim.models.KeyedVectors.load(r"C:\Users\satya\Desktop\Insightify\Code_base\Version_0.1\glove_model.gensim")
    def transform_text(self,text, use_lemmatization=True):
        text = text.lower()
        tokens = nltk.word_tokenize(text)
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stopwords.words('english') and word!='columns' and word!='column'and word!='data' and word!='dataset']
        filtered_tokens = [word for word in filtered_tokens if word not in string.punctuation]
        if use_lemmatization:
            wnl = nltk.WordNetLemmatizer()
            tokens = [wnl.lemmatize(word) for word in filtered_tokens]
        else:
            ps = PorterStemmer()
            tokens = [ps.stem(word) for word in filtered_tokens]
        embsum=np.zeros(300)
        embeddings=[]
        for count,token in enumerate(tokens):
            try:
                embeddings.append(self.model[token])
                embsum+=self.model[token]
            except:
                embeddings.append(embsum/(count+1))
        max_len=15
        while(len(embeddings)<max_len):
            padding_array = np.zeros(300,)
            embeddings.append(padding_array)
        vector=np.array(embeddings)
        vector = np.expand_dims(vector, axis=0)
        vector = tf.convert_to_tensor(vector, dtype=tf.float32)
        return vector
