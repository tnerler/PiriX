import os 
from langchain.text_splitter import RecursiveCharacterTextSplitter
import glob
from langchain_community.document_loaders import TextLoader
from utils.compute_hash import compute_hash

def markdown_loader():
    """
    Returns the documents as hashed, preprocessed, compiled.
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    md_dir = os.path.join(BASE_DIR, "data/data_md_format")

    md_files = glob.glob(os.path.join(md_dir, "*.md"))

    all_docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    
    for md_file in md_files: 

        try: 
            file_name = os.path.basename(md_file)
            loader = TextLoader(md_file, encoding="utf-8")
            docs = loader.load()

            split_docs = text_splitter.split_documents(docs)

            for doc in split_docs: 
                doc_hash = compute_hash(doc.page_content)
                doc.metadata["hash"] = doc_hash
            all_docs.extend(split_docs)

        except Exception as e:
            print(f"Error in {file_name}: {e}")
    
    print(f"Total docs: {len(all_docs)}")
    return all_docs


