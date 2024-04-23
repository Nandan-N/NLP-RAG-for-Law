import nest_asyncio
from llama_index.llms.openai import OpenAI
from llama_index.core.schema import MetadataMode
from llama_index.core.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
    KeywordExtractor,
    BaseExtractor,
)
from llama_index.extractors.entity import EntityExtractor
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.question_gen import LLMQuestionGenerator
from llama_index.core.question_gen.prompts import (
    DEFAULT_SUB_QUESTION_PROMPT_TMPL,
)
from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
import streamlit as st
import openai as oa
import numpy as np

nest_asyncio.apply()

import os
import openai

os.environ["OPENAI_API_KEY"] = "" # Add OpenAI key here!!!
llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo", max_tokens=512)
def ParseandExtract(paths):
    text_splitter = TokenTextSplitter(
    separator=" ", chunk_size=512, chunk_overlap=128
)
    extractors = [
    TitleExtractor(nodes=5, llm=llm),
    QuestionsAnsweredExtractor(questions=3, llm=llm),
    # EntityExtractor(prediction_threshold=0.5),
    # SummaryExtractor(summaries=["prev", "self"], llm=llm),
    KeywordExtractor(keywords=10, llm=llm),
    # CustomExtractor()
]

    transformations = [text_splitter] + extractors
    
    manual = SimpleDirectoryReader(
    input_dir=paths
).load_data()
    pipeline = IngestionPipeline(transformations=transformations)

    manual_nodes = pipeline.run(documents=manual)
    return manual_nodes
def ask(manual_nodes, question):
    question_gen = LLMQuestionGenerator.from_defaults(
    llm=llm,
    prompt_template_str="""
        Follow the example, but instead of giving a question, always prefix the question
        with: 'By first identifying and quoting the most relevant sources, '.
        """
    + DEFAULT_SUB_QUESTION_PROMPT_TMPL,
)
    # for i in range(len(manual_nodes)-1):
    #     if len(manual_nodes[i].get_content())< 30:
    #         manual_nodes.pop(i)
    index = VectorStoreIndex(
    nodes=manual_nodes,
)
    engine = index.as_query_engine(similarity_top_k=3, llm=OpenAI(model="gpt-4"))
    retriever=index.as_retriever()
    nodes=retriever.retrieve(question)
    print(nodes[0].score)
    if nodes[0].score>0.65:
        
        final_engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=[
            QueryEngineTool(
                query_engine=engine,
                metadata=ToolMetadata(
                    name="legal documents. cases and acts",
                    description="Contains information about past cases and relevant details around the cases helping for precedence",
                ),
            )
        ],
        question_gen=question_gen,
        use_async=True,
    )
        response = final_engine.query(question
    )
        print(response.response)
        # sources=[]
        
        # for key in response.metadata:
        
        #     try :
        #         sources.append(((int)(response.metadata[key]["page_label"]),response.metadata[key]["file_name"]))
        #     except:
        #         pass
        # # print(sources)
        # strings=[]

        # l=[]
        # ind=[]
        # nme=[]
        # for key in response.metadata:

        #     try :
        #         l.append(response.metadata[key]['questions_this_excerpt_can_answer'])
        #         ind.append((int)(response.metadata[key]['page_label']))
        #         nme.append(response.metadata[key]['file_name'])
        #     except:
        #         pass
        # sim=[]
        # for i in l:
        #     strings.append(question)
        #     strings.append(i)
        #     sim.append(compare(strings))
        #     strings=[]
        # page_ref=ind[sim.index(max(sim))]
        # name=nme[sim.index(max(sim))]
        # print(name)
        return response.response
    else:
        return "NO",[],(0,"")

def compare(input):
  client=oa.OpenAI()
  resp = client.embeddings.create(
        input=input,
        model="text-embedding-ada-002")
  Absolute_Ans = resp.data[0].embedding #actual
  cosine_sim=[]
  for i in range(1,len(input)):
    cosine_sim.append(np.dot(Absolute_Ans,resp.data[i].embedding))
  return cosine_sim[0]

def main():
    nodes=ParseandExtract(["Path for later ui"])
    ask(nodes,"which acts are used for land related matters")
if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()
