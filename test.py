from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv
from embed import embed
from pdf import read_pdf
load_dotenv()

#text = read_pdf("pdf/2-Xinxiang_CDM PDD.pdf")
text = read_pdf("pdf/1-Xinxiang_VCS Project Description.pdf")
embed(text)
