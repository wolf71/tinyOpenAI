'''
  # Tiny OpenAI ChatGPT and Whisper API Library
  - 2023/3     V0.1       By Charles Lai
'''
__version__ = 0.1
__author__ = 'Charles Lai'

import requests

#
# HTTP_Post Function
#
def httpPost(debug, *args, **kw):
  ''' OpenAI API httpPost function 
    debug: True/False - Display Debug info;
    *args/**kw: requests.post args;
  '''
  # init return value
  rdata = {}
  try:
    r = requests.post(*args, **kw)
  except Exception as x:
    if debug:
      if type(x) == requests.exceptions.SSLError:
        print('@ SSL Error, Please using: pip install certifi --upgrade ')
      else:
        print('@ Network Error!')
    # break return 
    return rdata
  # Get Result
  if r.status_code == 200:
    try:
      rdata = r.json()
    except:
      pass
  # status code not 200, print error info
  elif debug:
    # 400-File Problem, 401-API_KEY, 404-URL 
    if r.status_code == 400:
      print('@ Error, Please Check File type(mp3/m4a/wav/... audio file !')
    elif r.status_code == 401:
      print('@ Error, Please Check API_Key !')
    elif r.status_code == 404:
      print('@ Error, Please Check API_URL !')
    else:
      print('@ Error, HTTP Status_code is: %d !' % r.status_code)
  # Return Result JSON
  return rdata

#
# ChatGPT API
#
class ChatGPT():
  def __init__(self, API_Key='', Proxy='', Model='gpt-3.5-turbo', URL='https://api.openai.com/v1/chat/completions', Debug=False):
    ''' ChatGPT API Access, args: API_Key, Proxy, Model, API_URL, Debug '''
    self.API_Key = API_Key
    self.URL = URL
    self.Proxy = Proxy
    self.Model = Model
    self.Debug = Debug      # Debug info print
    self.Call_cnt = 0       # Total Call count
    self.Total_tokens = 0   # Total tokens count
    self.Hinfo = []         # Query History List

  def call(self, data):
    ''' Call ChatGPT '''
    headers = { "Content-Type": "application/json", "Authorization": f"Bearer {self.API_Key}" }
    # Call API
    rdata = httpPost(self.Debug, self.URL, headers = headers, proxies={"http": self.Proxy, "https": self.Proxy}, json = {"model": self.Model, "messages": data})
    # add total_tokens, call times
    if rdata:
      self.Total_tokens += rdata.get('usage', {}).get('total_tokens', 0)
      self.Call_cnt += 1
    # return result
    return rdata
  
  def get_text(self, rdata):
    ''' Return only message text, rdata = chatGPT return json '''
    if rdata:
      # get rdata['choices'][0]['message']['content']
      return rdata.get('choices', [{}])[0].get('message', {}).get('content', '').encode('utf8').decode()
    else:
      return ''

  def query(self, data, flag=False, hcnt=0, system='You are a helpful assistant.'):
    ''' Quick ask ChatGPT, data = Query string 
      flag: Using Query History flag  (Using obj.Hinfo = [] clean history.)
      hcnt: History count, 0:all, >0 last n (etc: 3-last 3, 10-last 10)
      system: ChatGPT system role content
    '''
    if flag:
      # Using Query History [abs to avoid negative numbers, *2 for Q&A paired]
      ret = self.get_text( self.call([{"role": "system", "content": system}] + self.Hinfo[-abs(hcnt*2):] + [{"role": "user", "content": data}]) )
      # add Query + Answer to History list
      self.Hinfo.append({"role": "user", "content": data})
      self.Hinfo.append({"role": "assistant", "content": ret})
    else:
      ret = self.get_text( self.call([{"role": "system", "content": system}, {"role": "user","content": data}]) )
    return ret

  def translate(self, text, lang='simplified chinese'):
    ''' Translate text to Simple Chinese or other '''
    text = text.strip()
    if text:
      return self.get_text( self.call([{"role": "user", "content": f"Please help me to translate,`{text}` to {lang}, please return only translated content not include the origin text"}]) )
    else:
      return ''

  def cHinfo(self):
    ''' Clean query History '''
    self.Hinfo = []

#
# Whisper API
#
class Whisper():
  def __init__(self,API_Key='', Proxy='', Model='whisper-1', URL=('https://api.openai.com/v1/audio/transcriptions','https://api.openai.com/v1/audio/translations'), Debug=False):
    # translations, transcriptions
    ''' Whisper API Access, args: API_Key, Type, Proxy, Model, API_URL, Debug '''
    self.API_Key = API_Key
    self.URL = URL
    self.Proxy = Proxy
    self.Model = Model
    self.Debug = Debug      # Debug info print
    self.Call_cnt = 0       # Total Call count
    self.Total_tokens = 0   # Total tokens count

  def call(self, file, Type=0):
    ''' Call Whisper 
      file: file name
      Type: 0.transcribes in source language  1.transcribes into English
    '''
    # check type
    if Type > len(self.URL): Type = len(self.URL) - 1
    # # Call ChatGPT API
    try:
      rdata = httpPost(self.Debug, self.URL[Type], headers = { "Authorization": f"Bearer {self.API_Key}" }, proxies = {"http": self.Proxy, "https": self.Proxy}, data = {'model': self.Model}, files = {'file': (file, open(file,'rb'))} )
    except FileNotFoundError:
      print('@ Error, File Not Found!')
      rdata = ''
    # get result
    if rdata:
      rdata = rdata.get('text', '')
      # add total_tokens, call times
      self.Total_tokens += len(rdata)
      self.Call_cnt += 1
    else:
      rdata = ''
    # Return result
    return rdata

#
# ChatGPT Query Demo
#
def QueryDemo():
  import sys
  if len(sys.argv) > 1:
    # get API_Key
    API_Key = sys.argv[1]
    # get Proxy
    if len(sys.argv) > 2:
      Proxy = sys.argv[2]
    else:
      Proxy = ''
    r = ChatGPT(API_Key, Proxy, Debug=True)
    print('>>> ChatGPT Query <<<')
    while True:
      try:
        cmd = input('> ').strip()
        if cmd:
          print('= '*36)
          print( r.query(cmd, True, 6) )
          print()
      except KeyboardInterrupt:
        break
  else:
    print('> Using python tinyOpenAI.py your_OpenAI_Key Proxy')

if __name__ == "__main__":
  QueryDemo()