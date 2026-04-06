import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Obsidian Auto-Researcher", page_icon="🕵️", layout="centered")


def main():
    st.title("🕵️ Obsidian Auto-Researcher")
    st.markdown("### Version 1.0 - Local RAG Pipeline")

    # Sidebar for configurations
    with st.sidebar:
        st.header("Settings")
        # Placeholder for local Ollama models we will connect later
        available_models = ["llama3", "mistral", "phi3"]
        selected_model = st.selectbox("Select Local Model", available_models)
        st.info(f"Currently selected: {selected_model}")

    # Main interface
    st.write("Welcome to the workspace. The RAG pipeline and HITL editor will appear here.")

    # A simple form for our future query input
    with st.form("research_form"):
        query = st.text_input("Enter your research topic:")
        submitted = st.form_submit_button("Generate Research")

        if submitted:
            st.warning("Pipeline not connected yet. Proceed to Phase 2 & 3!")

if __name__ == "__main__":
    main()