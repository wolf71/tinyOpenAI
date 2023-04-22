# Tiny OpenAI ChatGPT and Whisper API Library
- 2023/4     V0.13       By Charles Lai

## Features
- OpenAI ChatGPT and Whisper API library written in pure Python, so it can run in Python environment on M1/M2 Mac, iPad/iPhone(e.g. Pythonista, Juno, CODE, Pyto, ...), Android.
- Supports methods that conform to the ChatGPT API JSON format for API calls. Provides an easy-to-use quick dialog method, support for contextual associations; and easy language translation method. 
- ChatGPT Supports streaming output.
- Support for Whisper API calls to recognize and parse uploaded audio files as text messages or translate them into English.
- Support Embedding API call, Embedding vectorization of the incoming text, support string or text array

## How to Use
### ChatGPT
- **__init__(self, API_Key='', Proxy='', Model='gpt-3.5-turbo', URL='https://api.openai.com/v1/chat/completions', Debug=False, stream=False)**
  - Initialize the ChatGPT object, with the following parameters
  - API_Key: your openAI API Key
  - Proxy: If needed, set your http proxy server, e.g.: http://192.168.3.1:3128
  - Model: If needed, you can set it according to the OpenAI API documentation, e.g. change the default gpt-3.5-turbo to gpt-3.5-turbo-0301
  - URL: If OpenAI has changed the API URL address, you can change it here
  - Debug: if there is a network error or call error, whether to print out the error message, default is False.
  - stream: using openAI stream mode (the content returned by openAI to be displayed as a stream)
- **call(self, data)**
  - Call ChatGPT interface, return data in JSON format (see OpenAI API documentation for JSON details)
  - data is a Python dictionary (same as JSON), see the OpenAI API documentation for details, for example:
``` python
  data = [ {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is the OpenAI mission?"} ]
```
  - Return data:
    - If non-stream mode, return as string
    - If stream mode, return a constructor, can be output: for t in ret, ret is constructor, and t is a string
- **query(data, flag=False, hcnt=0, system='You are a helpful assistant.')**
  - To simplify the operation, the query method implements the simplest and quickest dialog function, simply typing the question and returning the text of the ChatGPT answer.
  - data: your question text
  - flag: whether you need to ensure contextual coherence in the conversation. Because of the nature of ChatGPT, if you want the next question to be related to the previous one, you need to do something special and bring the previous content and answer with you. To do this, just set the flag to True
  - hcnt: The number of contextual history conversations, default is 0, which means that each conversation will pass all previous history questions and answers to ChatGPT. Set to 6, which means that only the last 6 conversations will be kept. (Note: Because of ChatGPT's limit, the maximum number of tokens per conversation is 4096, so keeping all the history will cause the limit to be exceeded)
  - system: This is used to set the system role description of ChatGPT, see the OpenAI documentation for details
  - Returns data:
    - The result text returned by openAI
    - If stream mode, the results will be print out (streamed on the terminal); when all content is completed, the result text is returned
- **translate(text, lang='simplified chinese')**
  - To simplify the operation, a quick language translation function is provided to translate the input text into the corresponding language.
  - text: the text to be translated
  - lang: the language you want to translate to, e.g. english, japan, simplified chinese, etc.
- **cHinfo()**
  - Delete Contextual Dialog History
- **Statistics**
  - Call_cnt: Total number of ChatGPT calls
  - Total_tokens: Total Tokens usage data (OpenAI uses this as a basis for billing, and it is derived from the data returned by the ChatGPT API) 
- **Conversation history data and clear**
  - Hinfo: When using the query method and setting flag=True, this list holds all the conversation history.
  - If you need to delete it, use the cHinfo() method
- **A simple example**
``` python
import tinyOpenAI

g = tinyOpenAI.ChatGPT('your OpenAI API_Key', stream=True))
# g = tinyOpenAI.ChatGPT('your OpenAI API_Key','http://192.168.3.2:3128', Model='gpt-3.5-turbo-0301',Debug=True)
# Conversation
# if using stream=True mode, you don't neet print, otherwise using print()
# print( g.query('Write a rhyming poem with the sea as the title', system='You are a master of art, answer questions with emoji icons') )
g.query('Write a rhyming poem with the sea as the title', system='You are a master of art, answer questions with emoji icons')
# Continuous dialogue
print('======== continuous dialogue ============')
g.query('charles has $500, tom has $300, how much money do they have in total', True, 6)
g.query('charles and Tom who has more money', True, 6)
g.query('Sort them in order of money', True, 6)
# print history
print(g.Hinfo)
# clear Histroy
g.cHinfo()
# Statistics 
print('Call cnt: %d, Total using tokens: %d' % (g.Call_cnt, g.Total_tokens) )
```

### Whisper (speech-to-text interface)
- **__init__(API_Key='', Proxy='', Model='whisper-1', URL=('https://api.openai.com/v1/audio/transcriptions','https://api.openai.com/v1/ audio/translations'), Debug=False)**
  - Initialize the Whisper object, with the following parameters
  - API_Key: your openAI API Key
  - Proxy: If needed, set your http proxy server, e.g.: http://192.168.3.1:3128
  - Model: If needed, you can set it according to the OpenAI API documentation.
  - URL: If OpenAI changed the API address, you can change it here. Note that this is a list of two items, the first URL is the original language output, the second URL is translated into English.
  - Debug: If there is a network error or call error, whether to print out the error message, the default is not to print out the error message.
- **call(file, Type=0)**
  - file: voice file, format can be mp3/m4a/wav/mp4 with voice, refer to OpenAI API documentation
  - Type: Type of processing,  0.transcribes in source language  1.transcribes into English
- **Statistics**
  - Call_cnt: Total number of Whisper calls
  - Total_tokens: Total number of transcribed text (Note: OpenAI is billed for the length of audio, not the number of text)
- **Simple example**
``` python
import tinyOpenAI

w = tinyOpenAI.Whisper('your OpenAI API_Key', Debug=True)
print(w.call('test1.m4a')) # or mp3/mp4 file
print(w.call('test2.m4a')) # or mp3/mp4 file
print('Call cnt: %d, Total Texts: %d' % (w.Call_cnt, w.Total_tokens) )
```

### Embedding (get the embedding vector of the text)
- __init__(self, API_Key='', Proxy='', Model='text-embedding-ada-002', URL='https://api.openai.com/v1/embeddings', Debug=False)
  - Initialize the creation of the Embedding object, with the following parameters
  - API_Key: your openAI API Key
  - Proxy: If needed, set your http proxy server, e.g.: http://192.168.3.1:3128
  - Model: If needed, you can set it according to the OpenAI API documentation.
  - URL: If OpenAI changes the API call address, you can change it here. Note that this is a list of two addresses, the first address is the original language output, the second address is translated into English.
  - Debug: if there is a network error or call error, whether to print out the error message, the default is not
- embed(data)
  - data: the string or list of strings to be encoded
  - The result is a list of embed vectors (1536 dimensions) corresponding to the strings, which can be obtained by
    - For the input string, ret[0].get('embedding') can be used to get the vector
    - For a list of input strings, you can get the list of vectors with [i.get('embedding') for i in ret]
- Statistics
  - Call_cnt: the cumulative number of calls to Whisper
  - Total_tokens: cumulative number of transcribed texts (Note: OpenAI is billed for the length of the audio, not the number of texts)
- Simple example  
``` python
import tinyOpenAI

Embedding('your OpenAI API_Key', Debug=True)
r = e.embed('just for fun')
print('vector dimension:',len(r[0].get('embedding')))
# Compare the similarity of two texts
r = e.embed(['just for fun','hello world.'])
import numpy as np
print('Similarity result:',np.dot(r[0].get('embedding'), r[1].get('embedding')))
```