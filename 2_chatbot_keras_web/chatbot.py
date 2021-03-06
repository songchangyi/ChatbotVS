# *******************************************************************
# Deep learning part :
# *******************************************************************
# Necessary packages
from keras.layers import Input, Embedding, LSTM, Dense, RepeatVector, Dropout, merge
from keras.optimizers import Adam 
from keras.models import Model
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.preprocessing import sequence

import keras.backend as K
import numpy as np
np.random.seed(1234)  # for reproducibility
import pickle
import theano
import os.path
import sys
import nltk
import re
import time

# initialization of parameters
word_embedding_size = 100
sentence_embedding_size = 300
dictionary_size = 7000
maxlen_input = 50

vocabulary_file = 'vocabulary_movie'
weights_file = 'my_model_weights.h5' # my pretrained model
unknown_token = 'something'
file_saved_context = 'saved_context'
file_saved_answer = 'saved_answer'
name_of_computer = 'ChatbotVS'

# Greedy decoder algorithm
def greedy_decoder(input): # input is a tokenized

    flag = 0
    prob = 1
    ans_partial = np.zeros((1,maxlen_input))
    ans_partial[0, -1] = 2  #  the index of the symbol BOS (begin of sentence)
    for k in range(maxlen_input - 1):
        ye = model.predict([input, ans_partial]) # use the model to predict the partial answer
        yel = ye[0,:]
        p = np.max(yel)
        mp = np.argmax(ye)
        ans_partial[0, 0:-1] = ans_partial[0, 1:]
        ans_partial[0, -1] = mp
        if mp == 3:  #  the index of the symbol EOS (end of sentence)
            flag = 1
        if flag == 0:    
            prob = prob * p
    text = ''
    for k in ans_partial[0]:
        k = k.astype(int)
        if k < (dictionary_size-2):
            w = vocabulary[k]
            text = text + w[0] + ' '
    return(text, prob) # return the reply text and its probability

# preprocessing the raw sentence
def preprocess(raw_word, name):
    
    l1 = ['won’t','won\'t','wouldn’t','wouldn\'t','’m', '’re', '’ve', '’ll', '’s','’d', 'n’t', '\'m', '\'re', '\'ve', '\'ll', '\'s', '\'d', 'can\'t', 'n\'t', 'B: ', 'A: ', ',', ';', '.', '?', '!', ':', '. ?', ',   .', '. ,', 'EOS', 'BOS', 'eos', 'bos']
    l2 = ['will not','will not','would not','would not',' am', ' are', ' have', ' will', ' is', ' had', ' not', ' am', ' are', ' have', ' will', ' is', ' had', 'can not', ' not', '', '', ' ,', ' ;', ' .', ' ?', ' !', ' :', '? ', '.', ',', '', '', '', '']
    l3 = ['-', '_', ' *', ' /', '* ', '/ ', '\"', ' \\"', '\\ ', '--', '...', '. . .']
    l4 = ['jeffrey','fred','benjamin','paula','walter','rachel','andy','helen','harrington','kathy','ronnie','carl','annie','cole','ike','milo','cole','rick','johnny','loretta','cornelius','claire','romeo','casey','johnson','rudy','stanzi','cosgrove','wolfi','kevin','paulie','cindy','paulie','enzo','mikey','i\97','davis','jeffrey','norman','johnson','dolores','tom','brian','bruce','john','laurie','stella','dignan','elaine','jack','christ','george','frank','mary','amon','david','tom','joe','paul','sam','charlie','bob','marry','walter','james','jimmy','michael','rose','jim','peter','nick','eddie','johnny','jake','ted','mike','billy','louis','ed','jerry','alex','charles','tommy','bobby','betty','sid','dave','jeffrey','jeff','marty','richard','otis','gale','fred','bill','jones','smith','mickey']    

    raw_word = raw_word.lower()
    raw_word = raw_word.replace(', ' + name_of_computer, '') # replace the computer name within the raw word
    raw_word = raw_word.replace(name_of_computer + ' ,', '')

    for j, term in enumerate(l1):
        raw_word = raw_word.replace(term,l2[j]) # clean the symbols
        
    for term in l3:
        raw_word = raw_word.replace(term,' ')
    
    for term in l4:
        raw_word = raw_word.replace(', ' + term, ', ' + name) # replace the actor/actress's name with user name
        raw_word = raw_word.replace(' ' + term + ' ,' ,' ' + name + ' ,')
        raw_word = raw_word.replace('i am ' + term, 'i am ' + name_of_computer)
        raw_word = raw_word.replace('my name is' + term, 'my name is ' + name_of_computer)
    
    for j in range(30):
        raw_word = raw_word.replace('. .', '')
        raw_word = raw_word.replace('.  .', '')
        raw_word = raw_word.replace('..', '')
       
    for j in range(5):
        raw_word = raw_word.replace('  ', ' ')
        
    if raw_word[-1] !=  '!' and raw_word[-1] != '?' and raw_word[-1] != '.' and raw_word[-2:] !=  '! ' and raw_word[-2:] != '? ' and raw_word[-2:] != '. ':
        raw_word = raw_word + ' .'
    
    if raw_word == ' !' or raw_word == ' ?' or raw_word == ' .' or raw_word == ' ! ' or raw_word == ' ? ' or raw_word == ' . ':
        raw_word = 'what ?'
    
    if raw_word == '  .' or raw_word == ' .' or raw_word == '  . ':
        raw_word = 'i do not want to talk about it .'
      
    return raw_word

# Tokenization
def tokenize(sentences):
    
    # Tokenizing the sentences into words:
    tokenized_sentences = nltk.word_tokenize(sentences)
    index_to_word = [x[0] for x in vocabulary]
    word_to_index = dict([(w,i) for i,w in enumerate(index_to_word)])
    tokenized_sentences = [w if w in word_to_index else unknown_token for w in tokenized_sentences]
    X = np.asarray([word_to_index[w] for w in tokenized_sentences])
    s = X.size
    Q = np.zeros((1,maxlen_input))
    if s < (maxlen_input + 1): # if the input size do not pass the max length limit
        Q[0,- s:] = X
    else:
        Q[0,:] = X[- maxlen_input:]
    
    return Q

# Open files to save the conversation for further training:

qf = open(file_saved_context, 'w')
af = open(file_saved_answer, 'w')

print('Starting the model...')
# *******************************************************************
# Keras model of the chatbot: 
# *******************************************************************

ad = Adam(lr=0.00005) # Adam optimizer, lr is the learning rate

input_context = Input(shape=(maxlen_input,), dtype='int32', name='the_context_text')
input_answer = Input(shape=(maxlen_input,), dtype='int32', name='the_answer_text_up_to_the_current_token')
# The LSTM encoder and decoder
LSTM_encoder = LSTM(sentence_embedding_size, init= 'lecun_uniform', name='Encode_context')
LSTM_decoder = LSTM(sentence_embedding_size, init= 'lecun_uniform', name='Encode_answer_up_to_the_current_token')
# The shared embedding layer
if os.path.isfile(weights_file):
    Shared_Embedding = Embedding(output_dim=word_embedding_size, input_dim=dictionary_size, input_length=maxlen_input, name='Shared')
else:
    Shared_Embedding = Embedding(output_dim=word_embedding_size, input_dim=dictionary_size, weights=[embedding_matrix], input_length=maxlen_input, name='Shared')
# Apply LSTM with embedding layer
word_embedding_context = Shared_Embedding(input_context)
context_embedding = LSTM_encoder(word_embedding_context)

word_embedding_answer = Shared_Embedding(input_answer)
answer_embedding = LSTM_decoder(word_embedding_answer)
# Merge layer
merge_layer = merge([context_embedding, answer_embedding], mode='concat', concat_axis=1, name='concatenate_the_embeddings_of_the_context_and_the_answer_up_to_current_token')
out = Dense(int(dictionary_size/2), activation="relu", name='relu_activation')(merge_layer)
out = Dense(dictionary_size, activation="softmax", name='likelihood_of_the_current_token_using_softmax_activation')(out)
# Create the model and compile
model = Model(input=[input_context, input_answer], output = [out])

model.compile(loss='categorical_crossentropy', optimizer=ad)

if os.path.isfile(weights_file):
    model.load_weights(weights_file)
	
# Loading data
vocabulary = pickle.load(open(vocabulary_file, 'rb'))

# *******************************************************************
# Chatting online using Flask :
# *******************************************************************
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # user inputs
        first = request.form.get('first')
        # get response
        prob = 0
        que = str(first)
        last_query  = ' '
        last_last_query = ''
        text = ' '
        last_text = ''
        name = 'User'

        que = preprocess(que, name_of_computer)
        # Collecting data for training:
        q = last_query + ' ' + text
        a = que
        qf.write(q + '\n')
        af.write(a + '\n')
        # Composing the context:
        if prob > 0.2:
            query = text + ' ' + que
        else:    
            query = que

        last_text = text

        Q = tokenize(query)
        # Using the trained model to predict the answer:
        predout, prob = greedy_decoder(Q[0:1]) # Get the first row as predict output and the second row as their probs
        start_index = predout.find('EOS') # Get the end of the output
        text = preprocess(predout[0:start_index], name) # Extract the output and clean
        #print ('computer: ' + text + '    (with probability of %f)'%prob)
        res_reply = str(text)
        
        last_last_query = last_query    
        last_query = que

        return jsonify(res_reply)
    return render_template('index.html')

app.run()