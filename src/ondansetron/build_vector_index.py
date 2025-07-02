import os
import faiss
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

def build_vector_index():
    """
    Builds a FAISS vector index for the clinical trial documents.
    """
    # 1. Load a pre-trained sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 2. Walk through the directory and extract text from PDFs
    pdf_texts = []
    pdf_filepaths = []
    for root, _, files in os.walk('ressources/papers/Exported Items/files'):
        for file in files:
            if file.endswith('.pdf'):
                filepath = os.path.join(root, file)
                try:
                    reader = PdfReader(filepath)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                    pdf_texts.append(text)
                    pdf_filepaths.append(filepath)
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    # 3. Generate embeddings for the extracted text
    print("Generating embeddings...")
    embeddings = model.encode(pdf_texts, convert_to_tensor=True)

    # 4. Build a FAISS index
    print("Building FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings.cpu().detach().numpy())

    # 5. Save the index and the filepaths
    faiss.write_index(index, 'ressources/vector_index.faiss')
    with open('ressources/vector_index.fpaths', 'w') as f:
        for path in pdf_filepaths:
            f.write(f"{path}\n")

    print("Vector index built successfully.")

if __name__ == '__main__':
    build_vector_index()
