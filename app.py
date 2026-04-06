import streamlit as st
from rag_pipeline import generate_research

# Set the page configuration
st.set_page_config(page_title="Obsidian Auto-Researcher", page_icon="🕵️", layout="centered")


def main():
    st.title("🕵️ Obsidian Auto-Researcher")
    st.markdown("### Version 1.0 - Local RAG Pipeline")

    # Sidebar for configurations
    with st.sidebar:
        st.header("Settings")
        # Placeholder for local Ollama models we will connect later
        available_models = ["gemma4:e4b", "qwen3:8b", "tinyllama"]
        selected_model = st.selectbox("Select Local Model", available_models)
        st.info(f"Currently selected: {selected_model}")

    # Main interface
    st.write("Welcome to the workspace. Ask a question based on your Raw Sources.")

    # A simple form for our query input
    with st.form("research_form"):
        query = st.text_input("Enter your research topic:")
        submitted = st.form_submit_button("Generate Research")

        if submitted and query:
            with st.spinner(f"Querying ChromaDB and generating with {selected_model}..."):
                # Call our RAG function!
                result = generate_research(query, model_name=selected_model)
                st.success("Research Generated!")
                st.write(result)
        elif submitted and not query:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()