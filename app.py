import streamlit as st
from rag_pipeline import generate_research
from exporter import save_to_obsidian

st.set_page_config(page_title="Obsidian Auto-Researcher", page_icon="🕵️", layout="centered")

if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""

def main():
    st.title("🕵️ Obsidian Auto-Researcher")
    st.markdown("### Version 1.0 - Local RAG Pipeline")

    # Sidebar for configurations
    with st.sidebar:
        st.header("Settings")
        # Placeholder for local Ollama models
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
                # Save the result to Streamlit's memory so it survives button clicks!
                st.session_state.ai_response = result
                st.success("Research Generated!")
        elif submitted and not query:
            st.warning("Please enter a query.")

    # --- PHASE 4: HUMAN IN THE LOOP EDITOR ---
    # Only show this section IF there is a response in memory
    if st.session_state.ai_response:
        st.markdown("---")
        st.subheader("📝 Human-in-the-Loop Editor")

        # 1. The editable text box (pre-filled with AI output)
        edited_content = st.text_area("Review and tweak the AI output before saving:",
                                      value=st.session_state.ai_response,
                                      height=350)

        # 2. File naming
        note_title = st.text_input("Obsidian Note Title:", value="AI Research Notes")

        # 3. Export action
        if st.button("💾 Save to Obsidian"):
            success, message = save_to_obsidian(note_title, edited_content)

            if success:
                st.success(f"File successfully created in your vault at:\n`{message}`")
                st.balloons()  # A little celebration for finishing Version 1!
            else:
                st.error(f"Failed to save file: {message}")
if __name__ == "__main__":
    main()