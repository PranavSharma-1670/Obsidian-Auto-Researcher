import chromadb


def peek_database():
    # 1. Connect to the existing local database
    CHROMA_PATH = "./chroma_db"
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # 2. Access our specific collection
    collection = client.get_collection(name="research_materials")

    # 3. Get the total number of chunks stored
    count = collection.count()
    print(f"Total chunks in database: {count}\n")
    print("-" * 50)

    # 4. 'Peek' grabs the first few entries so we can inspect them
    if count > 0:
        results = collection.peek(limit=2)  # Change limit to see more chunks

        for i in range(len(results['ids'])):
            print(f"ID: {results['ids'][i]}")
            print(f"Metadata: {results['metadatas'][i]}")
            print(f"Document Text:\n{results['documents'][i][:200]}...")  # Printing just the first 200 chars
            print("-" * 50)
    else:
        print("The database is empty.")


if __name__ == "__main__":
    peek_database()