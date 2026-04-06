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


def generate_research(query, model_name="gemma4:e4b", temperature=0.0, custom_instructions=None):
    """Combines context and query, then asks Ollama for an answer."""

    print(f"Retrieving context for: '{query}'...")
    context_chunks = retrieve_context(query)

    if not context_chunks:
        return "No relevant context found in the database. Please add more documents."

    # Combine the chunks into a single string
    context_text = "\n\n---\n\n".join(context_chunks)

    # Use default instructions unless the user provides custom ones
    if custom_instructions:
        instructions = custom_instructions
    else:
        instructions = """You are a Senior Research Assistant. 
    Use ONLY the provided context to answer the user's question. 
    If the answer is not contained in the context, say "I cannot answer this based on the provided documents."
    """

    # Combine the chosen instructions with the actual retrieved text
    system_prompt = f"{instructions}\n\nCONTEXT:\n{context_text}"

    print(f"Sending prompt to local Ollama ({model_name}) at temp {temperature}...")

    # Send to Ollama with dynamic temperature
    response = ollama.chat(model=model_name, messages=[
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': f"Based STRICTLY on the context provided above, answer this: {query}"
        }
    ], options={
        'temperature': temperature
    })

    return response['message']['content']


# Testing block
if __name__ == "__main__":
    test_query = "What is the main topic of the documents?"
    answer = generate_research(test_query, model_name="gemma4:e4b")
    print("\n--- AI RESPONSE ---")
    print(answer)