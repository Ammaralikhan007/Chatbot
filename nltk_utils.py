import nltk
import numpy as np
#nltk.download('punkt') #Download the Punkt tokenizer model, which is a pre-trained model used by NLTK for sentence and word tokenization.
from nltk.stem.porter import PorterStemmer #Import the PorterStemmer, a rule-based algorithm for stemming words (reducing words to their root form).
stemmer = PorterStemmer()

def tokenize(sentence): #this is tokenizing the sentences into words
    return nltk.word_tokenize(sentence) #nltk.word_tokenize(sentence) returns a list of word tokens (and punctuation) from the input sentence.


def stem(word):
    return stemmer.stem(word.lower()) # .stem Applies Porter stemming to reduce the word to its root or base form.


def bag_of_words(tokenized_sentence,all_words):

    tokenized_sentence = [stem(w) for w in tokenized_sentence ]
    bag = np.zeros((len(all_words)), dtype=np.float32)

    for idx , w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0


    return bag











    

