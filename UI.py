import streamlit as st
import os
from pathlib import Path
import basic_rag as Manual_Reader
# import fitz
import io
from PIL import Image
from pymongo import MongoClient
from streamlit_feedback import streamlit_feedback

st.set_page_config(page_title="Law", page_icon="📒")
st.title("NLP RAG project ⚖️")
st.header("Built by - Nandan N, Vibha M, Utkarsh S.")

client = MongoClient("mongodb://localhost:27017/")
mydatabase = client['Stats'] 
mycollection = mydatabase['likes_and_dislikes'] 
mycollection3=mydatabase['Failures']
mycollection2=mydatabase['questions'] 


if 'files' not in st.session_state:    
    st.session_state.files=[]
if 'count' not in st.session_state:
    st.session_state.count=0

if 'feedback' not in st.session_state:
   st.session_state.feedback=None
if 'help' not in st.session_state:
   st.session_state.help=""
if 'manual_nodes' not in st.session_state:
   st.session_state.manual_nodes=None

with st.sidebar:
    # st.markdown("** Upload File Below: **")
    # with st.form(key="Manual :", clear_on_submit = False):

    #     uploaded_files = st.file_uploader(label = "Upload file", type=["pdf"],accept_multiple_files=True)
        Submit = st.button(label='Load')
        if Submit :
    #         st.markdown("*The file is sucessfully Uploaded.*")
    #         cwd=os.getcwd()
            
    #         for uploaded_file  in uploaded_files:
    #             st.session_state.files.append(uploaded_file.name)
              
    #             save_path=Path(cwd,uploaded_file.name)  
    #             with open(save_path, 'wb') as f: 
    #                 f.write(uploaded_file.getvalue())
            st.session_state.manual_nodes=Manual_Reader.ParseandExtract("./candidate/")        
st.subheader("Ask Question")
question=st.text_input("Enter...")
if st.button("Find Answer"):
    st.session_state.count+=1
 
    # q=st.session_state.questions
    
    print(st.session_state.files)
    Answer=Manual_Reader.ask(st.session_state.manual_nodes,question)
    if Answer!="NO":
    #   rec=mycollection2.insert_one({'question':question})
    # print(Answer,Sources,Page_ref)
      st.write(Answer)
      
    else:
    #    rec3=mycollection3.insert_one({'question':question})
       st.write("Couldnt Find Answer")
       st.markdown("email was sent to manager@example.com")
    
