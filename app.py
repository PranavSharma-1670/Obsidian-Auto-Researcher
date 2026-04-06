import streamlit as st
from rag_pipeline import generate_research
from exporter import save_to_obsidian

st.set_page_config(page_title="Obsidian Auto-Researcher", page_icon="🕵️", layout="centered")

if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""

def main():
    st.title("🕵️ Obsidian Auto-Researcher")
    st.markdown("### Version 1.1 - Settings & HITL")

    # --- SIDEBAR & SETTINGS ---
    with st.sidebar:
        st.header("Model Selection")
        # Placeholder for local Ollama models
        available_models = ["gemma4:e4b", "qwen3:4b", "tinyllama"]
        selected_model = st.selectbox("Select Local Model", available_models)
        st.info(f"Currently selected: {selected_model}")

        st.markdown("---")

        st.header("Advanced Settings")
        settings_mode = st.radio("Settings Mode", ["Default", "Custom"])

        # Initialize default variables so they exist even if "Default" is selected
        ui_temp = 0.0
        ui_instructions = None

        if settings_mode == "Custom":
            ui_temp = st.slider(
                "Temperature",
                min_value=0.0, max_value=1.0, value=0.0, step=0.1,
                help="0.0 is strict/factual. 1.0 is highly creative."
            )
            ui_instructions = st.text_area(
                "System Instructions",
                value="You are a Senior Research Assistant.\nUse ONLY the provided context to answer the user's question.\nIf the answer is not contained in the context, say \"I cannot answer this based on the provided documents.\"",
                height=150
            )

    # Main interface
    st.write("Welcome to the workspace. Ask a question based on your Raw Sources.")

    # A simple form for our query input
    with st.form("research_form"):
        query = st.text_input("Enter your research topic:")
        submitted = st.form_submit_button("Generate Research")

        if submitted and query:
            with st.spinner(f"Querying ChromaDB and Generating with {selected_model} (Temp: {ui_temp})..."):
                # Call our RAG function!
                result = generate_research(
                    query,
                    model_name=selected_model,
                    temperature=ui_temp,
                    custom_instructions=ui_instructions
                )
                # Save the result to Streamlit's memory so it survives button clicks!
                st.session_state.ai_response = result
                st.success("Research Generated!")
        elif submitted and not query:
            st.warning("Please enter a query.")

    # --- HITL EDITOR ---
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