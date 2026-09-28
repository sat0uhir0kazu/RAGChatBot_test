import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=api_key,
    task_type="retrieval_document",
    output_dimensionality=768
)

vector = embeddings.embed_query("テストです。")

print("Embedding成功")
print("次元数:", len(vector))