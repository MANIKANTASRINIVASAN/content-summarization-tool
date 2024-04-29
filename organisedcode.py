import os
from langchain.chains import LLMChain
from langchain_community.llms import Anyscale
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import DuckDB
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain

# Set API key
os.environ["ANYSCALE_API_KEY"] = "esecret_r1u6kcke1j42yfhmt1kjdh5pv1"

# Prompt template
template = """Question: {question}\nAnswer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)

# Initialize Anyscale model
llm = Anyscale(model_name="mistralai/Mixtral-8x7B-Instruct-v0.1")
llm_chain = prompt | llm

# Load PDF document
pdf_path = r"C:\Users\frost\Desktop\python project\The-Silent-Patient.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load()

# Split PDF document into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "\t"], chunk_size=10000, chunk_overlap=3000)
docs = text_splitter.split_documents(pages)

# Vectorize text chunks and store them in DuckDB
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = DuckDB(embedding=embedding_function)
vectorstore.add_documents(docs)

# Retrieve relevant documents
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Construct RetrievalQAWithSourcesChain
qachain = RetrievalQAWithSourcesChain.from_chain_type(llm, retriever=retriever)

def ask_question(question):
    result = qachain.invoke({"question": question})
    return result

# Example usage
#question = "When was George Washington president?"
#answer = ask_question(question)
#print("Answer:", answer)

# Ask question related to PDF content
pdf_question = "who was the killer?"
pdf_answer = ask_question(pdf_question)
print("Answer from PDF:", pdf_answer)
