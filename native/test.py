# import openai
#
#
#
# import openai
#
# # Apply the API key
# openai.api_key = "sk-de77806abc64a9683eef044a78520ad4"
#
# # Define the text prompt
# prompt = "In a shocking turn of events, scientists have discovered that "
#
# # Generate completions using the API
# completions = openai.Completion.create(
#     engine="text-davinci-002",
#     prompt=prompt,
#     max_tokens=100,
#     n=1,
#     stop=None,
#     temperature=0.5,
# )
#
# # Extract the message from the API response
# message = completions.choices[0].text
# print(message)


# import openai
# import os
# from dotenv import load_dotenv,find_dotenv
# _=load_dotenv(find_dotenv())
# openai.api_key = "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"
#
# # openai.api_key = os.getenv('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')
#
# def get_completion(prompt,model='gpt-3.5-turbo'):
#     messages = [{"role":"user","content":prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0,
#     )
#     return response.choices[0].message["content"]

# if __name__ == '__main__':
#     prompt = "加拿大在哪里"
#     response = get_completion(prompt)
#     print(response)
import json

from flask import Flask, render_template, request

app = Flask(__name__)
zhusizhe_prompt = '你是一个具有极强的批判性思维的导师，你总能从正反(好或坏)两个方面去看待问题和现象。并会利用问题温和的引导对方进行自我思考。你将按照json的格式进行返回回答。{"POSITIVE":["1...,2...,3..."],"NEGATIVE"["1...,2...,3..."],"CONCLUSION":["..."]}'

import openai
import re
import os
from dotenv import load_dotenv,find_dotenv
_=load_dotenv(find_dotenv())
openai.api_key = "sk-...."
app.config['NEGATIVE'] = 'bad'
app.config['POSITIVE'] = 'good'
# openai.api_key = os.getenv('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')

def get_completion(prompt,model='gpt-3.5-turbo'):
    messages = [{"role":"user","content":zhusizhe_prompt+ "<" +prompt + ">"}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]




@app.route("/read_pdf",methods=['POST'])
def read_pdf():
    import PyPDF2
    pdf_file = request.files['pdf']
    print("pdf_file:",pdf_file)
    # pdf_content = pdf_file.read()
    # print("pdf:content:",pdf_content)
    # 打开pdf文件
    # pdf_file = open(pdf_file, 'rb')

    # 创建一个PDF对象
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # 遍历每一页
    for page_num in range(pdf_reader.numPages):
        # 获取当前页对象
        page = pdf_reader.getPage(page_num)
        # 获取当前页中的文本
        text = page.extractText()
        # 打印文本
        print("开始:")
        print(text)
        return text.replace(' ','')

    # 关闭pdf文件
    pdf_file.close()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_input = request.args.get('msg')
    if user_input == "你是谁？":
        return str("我是一个由曹博士进行训练并部署的大语言模型!很高兴见到你！")
    response = get_completion(user_input)
    response_dict = json.loads(response)

    print(response_dict)
    positive = str(response_dict['POSITIVE'][0]) + "\n" +str(response_dict['POSITIVE'][1]) + "\n" +str(response_dict['POSITIVE'][2]) + "\n"
    negative = str(response_dict['NEGATIVE'][0]) + "\n" +str(response_dict['NEGATIVE'][1]) + "\n" +str(response_dict['NEGATIVE'][2]) + "\n"
    app.config.update(
        POSITIVE=positive,
        NEGATIVE=negative
    )
    # print(positive)
    # print(negative)
    # d = eval('{' + response + '}')
    # print(d)
    # print(response)
    # match = re.search(r'POSITIVE:(.*?)', response)
    # positive_answers = match.group(1).split('\n')
    # print(positive_answers)
    # positive = response.split()

    return positive

@app.route("/get1",methods=['GET'])
def get_bot_response1():
    print("get_bot_response1")
    print(app.config.get('POSITIVE'))
    return app.config.get('POSITIVE')

@app.route("/get2",methods=['GET'])
def get_bot_response2():
    print("get_bot_response2")
    print(app.config.get('NEGATIVE'))
    return app.config.get('NEGATIVE')

# @app.route("get_jinrong")
# def get_jinrong():


if __name__ == "__main__":
    app.run(debug=True)
