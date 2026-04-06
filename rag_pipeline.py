import chromadb
import ollama

# Connect to our existing Chroma database
CHROMA_PATH = "./chroma_db"
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(name="research_materials")


def retrieve_context(query, n_results=3):
    """Searches ChromaDB for the most relevant text chunks based on the user's query."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    # Extract the actual text documents from the results
    if results['documents'] and len(results['documents'][0]) > 0:
        return results['documents'][0]
    return []


def generate_research(query, model_name="gemma4:e4b"):
    """Combines context and query, then asks Ollama for an answer."""

    print(f"Retrieving context for: '{query}'...")
    context_chunks = retrieve_context(query)

    if not context_chunks:
        return "No relevant context found in the database. Please add more documents."

    # Combine the chunks into a single string
    context_text = "\n\n---\n\n".join(context_chunks)

    # ---------------------------------------------------------
    # THE PROMPT TEMPLATE: This is the secret sauce of RAG
    # ---------------------------------------------------------
    system_prompt = f"""You are a Senior Research Assistant. 
Use ONLY the provided context to answer the user's question. 
If the answer is not contained in the context, say "I cannot answer this based on the provided documents."

CONTEXT:
{context_text}
"""

    print(f"Sending prompt to local Ollama ({model_name})...")

    # Send to Ollama
    response = ollama.chat(model=model_name, messages=[
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': query
        }
    ])

    return response['message']['content']


# Testing block
if __name__ == "__main__":
    test_query = "What is the main topic of the documents?"
    answer = generate_research(test_query, model_name="gemma4:e4b")
    print("\n--- AI RESPONSE ---")
    print(answer)