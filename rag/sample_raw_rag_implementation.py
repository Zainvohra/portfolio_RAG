from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import aisuite as ai
from singleton_decorator import singleton


class DocumentQA:
    def __init__(self, document_path, embeddings_model="sentence-transformers/all-MiniLM-L6-v2"):
        self.document_path = document_path
        self.embeddings_model = embeddings_model
        self.vectorstore = None
        self.embedding_model = HuggingFaceEmbeddings(model_name=self.embeddings_model)

    def process_pdf(self):
        # Load PDF
        loader = PyPDFLoader(self.document_path)
        documents = loader.load()

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        return text_splitter.split_documents(documents)

    def create_chunks_embeddings(self, chunks):
        # Create a FAISS vectorstore
        self.vectorstore = FAISS.from_texts(
            [chunk.page_content for chunk in chunks],
            self.embedding_model
        )
        return self.vectorstore

    def create_query_embedding(self, query):
        return self.embedding_model.embed_query(query)

    def semantic_search(self, query_embedding):
        return self.vectorstore.similarity_search_by_vector(query_embedding, k=3)

    def normalize_response(self, matched_text, query):
        _query = f"{query}, based on attached text below: {matched_text}"
        client = ai.Client()

        messages = [
            {"role": "system", "content": "Respond in precise 2 liner maximum"},
            {"role": "user", "content": _query},
        ]

        response = client.chat.completions.create(
            model="groq:llama-3.1-70b-versatile",
            messages=messages,
            temperature=0.75
        )
        print("="*50)
        print(response.choices[0].message.content)
        print("="*50)

    def process_query(self, query):
        # Step 1: Process the PDF if vectorstore doesn't exist
        if not self.vectorstore:
            chunks = self.process_pdf()
            self.create_chunks_embeddings(chunks)

        # Step 2: Create query embedding
        query_embedding = self.create_query_embedding(query)

        # Step 3: Perform a semantic search
        results = self.semantic_search(query_embedding)
        result = "\n\n".join([res.page_content for res in results])

        # Step 4: Normalize and get response
        self.normalize_response(matched_text=result, query=query)


def main():
    qa = DocumentQA("employee_handbook.pdf")
    while True:
        question = "Enter question to be asked from document: If my tenure within company is 2.5 years and my PF share is around 200k rupees, if i leave the company today then how much Provident fund, i will receive today"
        qa.process_query(question)


if __name__ == "__main__":
    main()