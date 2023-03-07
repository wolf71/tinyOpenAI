# Tiny OpenAI ChatGPT and Whisper API Library
- 2023/3     V0.1       By Charles Lai

## 功能
- 纯 Python 编写的 OpenAI ChatGPT and Whisper API 库, 因此可以在 M1/M2 Mac, iPad/iPhone 等设备上的 Python 环境运行(例如: Pythonista, Juno, CODE, Pyto 等)
- 支持符合 ChatGPT API JSON 格式的接口调用的方法. 并提供一个易用的 query 快速对话方法,支持上下文关联 和 一个快速简单的语言翻译方法
- 支持 Whisper 接口调用, 将上传的 音频文件 识别解析为文本信息或翻译成英语

## 使用
### ChatGPT
- __init__(self, API_Key='', Proxy='', Model='gpt-3.5-turbo', URL='https://api.openai.com/v1/chat/completions', Debug=False)
  - 初始化创建 ChatGPT 对象, 对应参数如下
  - API_Key: 你的 openAI API Key
  - Proxy: 如需要，设置你的 http代理服务器，例如: http://192.168.3.1:3128
  - Model: 如需要，可以根据 OpenAI API文档进行设置，例如将默认的 gpt-3.5-turbo 更改为 gpt-3.5-turbo-0301
  - URL: 若 OpenAI 更改了 API 调用地址，可以在这里更改
  - Debug: 出现网络错误、调用错误，是否打印输出错误信息, 默认不输出
- call(self, data)
  - 调用 ChatGPT 接口, 返回 JSON 格式的数据 (具体JSON内容可参见 OpenAI API 文档)
  - data 为 Python 字典类型 (和JSON格式一样),具体要求参见 OpenAI API 文档, 例如:
``` python
  data = [ {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is the OpenAI mission?"} ]
```  
- query(data, flag=False, hcnt=0, system='You are a helpful assistant.')
  - 为简化操作，query方法实现了最简单、快捷的对话功能, 只需要输入问题, 就会返回 ChatGPT 回答的文本
  - data: 你的问题文本
  - flag: 是否需要在对话中确保上下文连贯. 因为 ChatGPT 的特性，如果你希望后面的问题能够与前面的问题相关联, 则需要进行特殊处理，将以前的内容和回答带上. 这个时候只需要设置 flag 为 True 就可以了
  - hcnt: 上下文连贯的历史对话轮数, 默认为0, 表示每一次对话都会把以前所有历史问答传递给 ChatGPT. 设为6, 表示只保留最后 6 轮的对话. (注意: 因为 ChatGPT 的限制, 每次对话的 tokens 最大是 4096, 因此如果保持所有历史会导致超出限制)
  - system: 用于设置 ChatGPT 的 system 角色描述内容, 具体可以参见 OpenAI 文档
- translate(text, lang='simplified chinese')
  - 为简化操作, 提供一个快速语言翻译的功能, 将输入的 text 翻译为对应的语言
  - text: 需要翻译的文本
  - lang: 希望翻译成什么语言, 例如 english, japans, simplified chinese 等
- cHinfo()
  - 删除 上下文关联对话 历史记录
- 统计数据
  - Call_cnt: 累计调用 ChatGPT 次数
  - Total_tokens: 累计 Tokens 使用量数据 (OpenAI以此为依据进行计费, 数据源自 ChatGPT 接口返回的数据) 
- 对话历史数据 及 删除
  - Hinfo: 当用 query 方法,并设置 flag=True的时, 这个列表保存了所有的历史对话记录
  - 如果需要删除, 使用 cHinfo() 方法
- 简单的例子
``` python
import tinyOpenAI

g = tinyOpenAI.ChatGPT('your OpenAI API_Key')
# g = tinyOpenAI.ChatGPT('your OpenAI API_Key','http://192.168.3.2:3128', Model='gpt-3.5-turbo-0301',Debug=True)
# 对话
print( g.query('以大海为题目,写一首押韵的古诗', system='你是一个艺术大师, 回答问题都会带有emoji图标') )
# 连续对话
print('========连续对话============')
print(g.query('小李有500元, 小张有300元,他们合在一起可以买790元的电视吗?', True, 6))
print(g.query('他们两个谁的钱多? 差别多少？', True, 6))
print(g.query('按照他们的钱数倒排序, 列出名字,钱数量', True, 6))
# 打印历史记录
print(g.Hinfo)
# 清除历史记录
g.cHinfo()
# 统计信息
print('Call cnt: %d, Total using tokens: %d' % (g.Call_cnt, g.Total_tokens) )
```

### Whisper (语音转文字接口)
- __init__(API_Key='', Proxy='', Model='whisper-1', URL=('https://api.openai.com/v1/audio/transcriptions','https://api.openai.com/v1/audio/translations'), Debug=False)
  - 初始化创建 Whisper 对象, 对应参数如下
  - API_Key: 你的 openAI API Key
  - Proxy: 如需要，设置你的 http代理服务器，例如: http://192.168.3.1:3128
  - Model: 如需要，可以根据 OpenAI API文档进行设置
  - URL: 若 OpenAI 更改了 API 调用地址，可以在这里更改, 注意这里是一个包含两个地址的列表, 第一个地址是原语言输出, 第二个地址是翻译成英文后输出
  - Debug: 出现网络错误、调用错误，是否打印输出错误信息, 默认不输出
- call(file, Type=0)
  - file: 语音文件, 格式可以是 mp3/m4a/wav/mp4 等带有语音的格式, 具体参看 OpenAI API文档
  - Type: 处理类型, 0.源语言转录 1.转录成英语
- 统计数据
  - Call_cnt: 累计调用 Whisper 次数
  - Total_tokens: 累计转录文字数量 (注意: OpenAI是按照音频时长计费, 而非文字数量计费)
- 简单例子  
``` python
import tinyOpenAI

w = tinyOpenAI.Whisper('your OpenAI API_Key', Debug=True)
print(w.call('test1.m4a'))   # or mp3/mp4 file
print(w.call('test2.m4a'))   # or mp3/mp4 file
print('Call cnt: %d, Total Texts: %d' % (w.Call_cnt, w.Total_tokens) )
```