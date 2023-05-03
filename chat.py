import openai
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
import openai
from langchain.document_loaders.csv_loader import CSVLoader
import re



st.set_page_config(page_title="助思者", page_icon="💗", layout="wide",
)


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



def get_text():
    # Create a Streamlit input field and return the user's input
    input_text = st.text_area('输入分析文本', height=5).strip()
    return input_text


col1, col2 = st.columns(2)

with col1:
    user_input = get_text()
    # st.text(user_input)
    click = st.button('发送')

with col2:
    # TODO 上传pdf 识别
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
                st.markdown("#### 正面：")
                for line in text['正面']:
                    st.markdown("- " + line)

            with col4:
                st.markdown("#### 反面：")
                for line in text['反面']:
                    st.markdown("- " + line)

            st.write("----")
            st.markdown("**" + text['结论'].strip() + "**")

        except:
            st.warning("结果异常，请稍后重试")

    else:
        st.text("请输入文本")
