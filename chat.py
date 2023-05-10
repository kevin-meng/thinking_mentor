import openai
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
import openai
from langchain.document_loaders.csv_loader import CSVLoader
import re
import pdfminer
from pdfminer.high_level import extract_pages,extract_text
import streamlit as st





def load_pdf_data(file):
    texts = ""
    for page_layout in extract_pages(file):
        for element in page_layout:
            texts += element.get_text()
            # st.write(element.get_text())
    return texts




st.set_page_config(page_title="", page_icon="💗", layout="wide",
)

st.image("./pic/mentor.png",width=200)
# st.title("助思者")
# Load environment variables from a .env file (containing OPENAI_API_KEY)
load_dotenv()
# Set the title for the Streamlit app
st.title(os.environ.get('SITE_TITLE'))
# Set the OpenAI API key from the environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')

api_base = os.environ.get('OPENAI_API_BASE')
if api_base !='':
    openai.api_base = api_base


# message("My message") 
# message("Hello bot!", is_user=True)  # align's the message to the right




def generate_response(prompt):
    # Generate a response using OpenAI's ChatCompletion API and the specified prompt
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ])
    response = completion.choices[0].message.content
    
    return response



def get_text(text=''):
    # Create a Streamlit input field and return the user's input
    input_text = st.text_area('输入分析文本', text,height=2).strip()
    return input_text




base_prompt = """
        你是一个具有极强的批判性思维的导师，你总能从正反（好或坏）两个方面去看待问题和现象。并会利用问题温和的引导对方进行自我思考。
        你将按照json的格式进行返回回答。
        {"反面":["1. ...", "2. ....", "3. ..."],
        "反面":["1. ...", "2. ....", "3. ..."],
        "结论":"...."}
        ----------------
        """


col1, col2,col3 = st.columns([3, 2,1])

with col1:
    st.info("培养批判性思维，提高问商")
    expander01 = st.expander("上传文件")
    # TODO 上传pdf 识别
    uploaded_file = expander01.file_uploader("", type="pdf", accept_multiple_files=False,  label_visibility="hidden")
    if uploaded_file is not None:
        text = load_pdf_data(uploaded_file)
        user_input = get_text(text)
    else:
        user_input = get_text()

    user_input = base_prompt + user_input
    # st.text(user_input)
    click = st.button('发送')

with col2:

    pass



if click:
    if len(user_input)>0:
        response = generate_response(user_input)
        # st.markdown(response)
        # st.markdown(type(response))

        try:
            text = eval(response.strip())
            col3, col4 = st.columns(2)

            with col3:
                st.markdown("#### :innocent: 正面：")
                for line in text['正面']:
                    st.markdown("- " + line)

            with col4:
                st.markdown("#### :imp: 反面：")
                for line in text['反面']:
                    st.markdown("- " + line)

            st.write("----")
            st.markdown("**" + text['结论'].strip() + "**")

        except:
            st.warning("结果异常，请稍后重试")

    else:
        st.text("请输入文本")


