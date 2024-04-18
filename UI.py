import streamlit as st
import os
from pathlib import Path
import basic_rag as Manual_Reader
# import fitz
import io
from PIL import Image
from pymongo import MongoClient
from streamlit_feedback import streamlit_feedback

st.set_page_config(page_title="Justice", page_icon="📒")
st.title("Justice Justified ⚖️")
st.header("Built by - Gautham K, Gautham P A, Nandan N, Shreya C.")

client = MongoClient("mongodb://localhost:27017/")
mydatabase = client['Stats'] 
mycollection = mydatabase['likes_and_dislikes'] 
mycollection3=mydatabase['Failures']
mycollection2=mydatabase['questions']
# def fimage(file,pg):
#   size=[]
#   pdf_file = fitz.open(file)
#   list=[]
#   try:
#     for page_index in range(pg,pg+1):
#       page = pdf_file[page_index]
#       image_list = page.get_images()
#       if image_list:
#         print(
#           f"[+] Found a total of {len(image_list)} images in page {page_index}")
#       else:
#         print("[!] No images were found on page", page_index)
#       for image_index, img in enumerate(page.get_images(), start=1):
#         xref = img[0]
#         base_image = pdf_file.extract_image(xref)
#         image_bytes = base_image["image"]
#         image_ext = base_image["ext"]
#         image = Image.open(io.BytesIO(image_bytes))
#         height,width=image.size
#         size.append(height+width)
        
#         list.append(f"image{page_index+1}_{image_index}.{image_ext}")
#         image.save(open(f"./image{page_index+1}_{image_index}.{image_ext}", "wb"))
#   except:
#     pass
      
#   return list,size    


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
    
