import os
import chromadb

# 1. Initialize ChromaDB (This creates a folder called 'chroma_db' in your project to save data locally)
CHROMA_PATH = "./chroma_db"
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Create a collection (like a table in a traditional database)
collection = client.get_or_create_collection(name="research_materials")


def chunk_text(text, chunk_size=1000, overlap=100):
    """
    Splits text into smaller pieces (chunks).
    We use overlap so we don't cut a sentence or idea in half abruptly.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        # Move the start forward, but step back by the overlap amount
        start = end - overlap
    return chunks


def ingest_documents(folder_path="Raw_Sources"):
    """
    Reads all .txt and .md files in the folder, chunks them, and stores them in ChromaDB.
    """
    if not os.path.exists(folder_path):
        print(f"Directory {folder_path} does not exist.")
        return

    documents = []
    metadatas = []
    ids = []

    print(f"Scanning '{folder_path}' for documents...")

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") or filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Split the document into chunks
            chunks = chunk_text(content)

            # Prepare data for ChromaDB
            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                # Store metadata so we know exactly which file a chunk came from
                metadatas.append({"source": filename, "chunk_index": i})
                ids.append(f"{filename}_chunk_{i}")

            print(f"Processed: {filename} ({len(chunks)} chunks)")

    # Add to ChromaDB (Chroma will automatically generate embeddings for us!)
    if documents:
        print("Saving to ChromaDB... (This might take a moment the first time as it downloads the embedding model).")
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("Success! Documents added to the vector database.")
    else:
        print("No .txt or .md files found to process.")


# Block to allow us to test this script directly
if __name__ == "__main__":
    ingest_documents()