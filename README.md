# Chatbot Using Movie Subtitles

Author: Changyi SONG

Date: 2017/11/19

## 0. Flow Diagram

<div align=center><img width="450" src="/img/Flowgram.PNG"/></div>

## 1. Introduction
Chat bots using AI technique have driven many attentions not only in academic fields but also in business areas. A Chat bot can work as a virtual assistant in customer service, consulting services and smart conversations, etc. Here we are going to develop a chat bot using movie subtitles downloaded from the internet. Since the project is an open-end task, we can analyze it in different aspects or different scopes and multiple solutions are available.

First, intuitively we think a chat bot using movie subtitles means it can return the exact following subtitle of a movie from which we give choose a sentence for test. For this type of chat bots, the most common technique is by using string-matching algorithm. Among a corpus of movie subtitles download from the internet, we find the sentence best matching the given sentence and return directly the following sentence to the system. Even though it is not so intelligent, it is the basic and simplest way to create a chat bot. There I will briefly introduce it in the following chapter.

However, when we talk about using movie subtitles, we can also think about using in NLP (Nature Language Process). Movie subtitles are actually a custom or a style of talking. As everyone has its own preference to speak, movie dialogues also have its inner features. Therefore, we can use NLP as well as deep learning algorithm to build a chat bot that use movie subtitles’ “style” to communicate with its user. Since this type of chat bots are more human like or in other words more artificial intelligent, it is more interesting to most companies and related researches. Thus, this report will mainly concerned the realization of this chat bot. 

Finally, by integrating exiting APIs, we can create some robots with diverse functions. In addition, please excuse for my carelessness that I have not read the FAQ parts at the very beginning since it is separated in the last page. Still I would like to present it in this report because it could be a part of supplement to the project.

In the following chapter, all three chat bots will be introduced. You can find the relative code on https://github.com/songchangyi/ChatbotVS .

## 2. Chat bot I (seq2seq using keras)
The first Chat bot uses seq2seq model.
Primarily, the words of questions and answers are not exactly the same in most circumstances. Besides, the answer given by a chat bot results from the last two related conversations. Consequently, to generate a needed response, we use LSTM (Long Short-Term Memory), which is a variant of the RNN (Recurrent Neural Networks).
While the keras library provides the necessary functions for implementation, some basic libraries such as NLTK, Numpy are also needed.

### 2.1 Data source
The chat bot should learn from a big database of movie subtitles and the best well-known English movie corpus is Cornell University movie dialog corpus, which contains about 300K lines of movie dialogs. 
It is available on the Kaggle website :
https://www.kaggle.com/Cornell-University/movie-dialog-corpus 

### 2.2 Algorithm 
The architecture presented here assumes the same prior distributions for input and output words. Therefore, it shares the embedding layer (Glove pre-trained word embedding) between the encoding and decoding processes through the adoption of a new model. 
To improve the context sensitivity, the thought vector (i.e. the encoder output) encodes the last two utterances of the conversation up to the current point. To avoid forgetting the context during the answer generation, the thought vector is concatenated to a dense vector that encodes the incomplete answer generated up to the current point. The resulting vector is provided to dense layers that predict the current token of the answer. 
The algorithm iterates by feeding back the predicted token to the right-hand side input layer of the model shown below.
---
The following pseudo code explains the algorithm.
---

### 2.3 Training model
30,000 lines of movie conversations were used to train the designed model while it required 100 epochs to reach categorical cross-entropy loss of 0.0394, at the cost of 600 s/epoch running on the FloydHub platform (a public platform for data scientist, https://www.floydhub.com/ ).

Here shows the result of the training logs :
---
It is also suggested to use Glove pre-trained model, which is available on line (https://nlp.stanford.edu/projects/glove/). This algorithm applies transfer learning which is fine-tuned during the training by using a pre-trained word embedding. This transfer-learning model will help us to obtain a better performance.[2]

Find the final model here:
https://www.dropbox.com/s/e13y0zarsfv76vt/my_model_weights.h5?dl=0
Please use it when test the seq2seq Chat bots.

### 2.4 Test 1 : Chat in python console
So far, our first chat bot is ready to use. 
Download all the resource from: https://github.com/songchangyi/ChatbotVS/tree/master/1_chatbot_keras_py.

The file saved_context is used to save questions and the saved_answer for answers of historical conversation for future learning. The vocabulary_movie file contains the vocabularies it will use. 

Download our pre-training model in the same folder.

Open the terminal and switch to the folder path, enter :
	python chatbot.py

If some libraries are missing in the environment, use :
	pip install xxx # xxx for package name

Then we can start chatting with the first chat bot.
---

### 2.5 Local website
As suggested in the task statement, a simple web page can make the application more interactive and a python based website is created dedicate to the chat bot.
The backend reply part is based on python, to make life easier, we use another python library Flask for web application.

Here you find the relative resources (integrated with chatbot) : 
https://github.com/songchangyi/ChatbotVS/blob/master/2_chatbot_keras_web/chatbot.py 

And the website template:
https://github.com/songchangyi/ChatbotVS/tree/master/2_chatbot_keras_web/templates 
### 2.6 Test 2: Chat through web page
Download the code from: 
https://github.com/songchangyi/ChatbotVS/tree/master/2_chatbot_keras_web

As talked in 2.4, we should ensure my_model_weights.h5 file exists in the same folder.

Repeat the steps in 2.4 to execute the python file (chatbot.py). 

In the console, we can see that our local web application started and the port have already connected:
---
Open the browser and search :
http://127.0.0.1:5000/

The application web page should be opened. Then enter a sentence in text box and click the button “Get response!” to start chatting. The reply will be shown below.
---

## 3. Chat bot II (using python library)
As we know, the Chat bot I (seq2seq using keras) is a possible realization of a Chat bot. However, the responds are sometimes ambiguous that are not much like a human sentence. It is kind of making up sentences following statistical rules and need more linguistic improvement. 

The following chat bot is created from another different method, which makes it more like a human talking but with less intelligence.
### 3.1 Chatterbot
Chatterbot is a dedicated python library for creating chatbots. By using this package, we can realize the chatbot function in very few code. Its mechanism is simply finding the most similar word/sentence in the corpus.
### 3.2 Test
Find the resources here: https://github.com/songchangyi/ChatbotVS/tree/master/3_chatbot_pythonAPI

Here the pre-trained model is unnecessary.

As shown below, it is possible to make chat bot in very short lines of code.
---
The way to integrate web part and chat part is the same as 2.6.
## 4. Chat bot III (integrated with Google API)
By using different algorithm, it is not so difficult to create a text based chat bot, but more API functions can make the robot much interesting. Here we can see how a Chat bot integrated Google API attract many fans on Wechat.

By integrating APIs, the chat bot is able to do image recognition, translation and communication.

The python library itchat helps to connect chat bot to WeChat backstage. 

For more details:
https://itchat.readthedocs.io/zh/latest/intro/start/ 
### 4.1 Google API
Based on Google's image recognition API, text analysis API and translation API, we can make our chatbot more powerful. 

Use Jupyter Notebook to run:
https://github.com/songchangyi/ChatbotVS/tree/master/4_chatbot_googleAPI
### 4.2 Test
Test results from Wechat :
---
---
---
---
Try to talk with it by scanning the QR-Code.

## 5. Bibliographies
1. Data source : Cornell Movie Corpus:
https://www.kaggle.com/Cornell-University/movie-dialog-corpus

2. Seq2seq Chatbot
https://github.com/oswaldoludwig/Seq2seq-Chatbot-for-Keras

3. Chatterbot Library
https://github.com/gunthercox/ChatterBot/tree/master/examples
http://chatterbot.readthedocs.io/en/stable/training.html#training-with-corpus-data

4. ItChat Library
https://github.com/littlecodersh/ItChat

5. Google APIs
https://github.com/telescopeuser/workshop_blog 
