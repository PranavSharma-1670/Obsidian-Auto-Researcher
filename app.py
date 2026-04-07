import streamlit as st
from rag_pipeline import generate_research
from exporter import save_to_obsidian

st.set_page_config(page_title="Obsidian Auto-Researcher", page_icon="🕵️",layout="wide")

# --- INITIALIZE SESSION STATE ---
if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""
if "save_success" not in st.session_state:
    st.session_state.save_success = False
if "save_message" not in st.session_state:
    st.session_state.save_message = ""
if "drafts" not in st.session_state:
    st.session_state.drafts = {}
if "active_query" not in st.session_state:
    st.session_state.active_query = ""


def main():
    st.title("🕵️ Obsidian Auto-Researcher")
    st.markdown("### Version 1.2 - Multi-Model Comparison Grid")

    # --- CHECK FOR SUCCESSFUL SAVE ---
    if st.session_state.save_success:
        st.success(st.session_state.save_message)
        st.balloons()
        # Reset so it doesn't show up again on the next click
        st.session_state.save_success = False
        st.session_state.save_message = ""

    # --- SIDEBAR & SETTINGS ---
    # with st.sidebar:
    #     st.header("Initial Model Selection")
    #     # Placeholder for local Ollama models
    #     available_models = ["gemma4:e4b", "qwen3:4b", "tinyllama"]
    #     selected_models = st.multiselect(
    #         "Select Models to Compare",
    #         available_models,
    #         default=["gemma4:e4b"]  # Default to at least one so the app doesn't complain
    #     )

    # --- SIDEBAR & SETTINGS ---
    with st.sidebar:
        st.header("Initial Model Selection")

        # Ask Ollama what is physically installed on your Mac right now!
        import ollama
        try:
            local_models_info = ollama.list()
            # Extract the names of the models
            available_models = [m['model'] for m in local_models_info['models']]
        except Exception:
            available_models = ["Error: Could not connect to Ollama"]

        selected_models = st.multiselect(
            "Select Models to Compare",
            available_models,
            # Use the first available model as the default to prevent UI errors
            default=[available_models[0]] if available_models else None
        )

        st.markdown("---")
        st.header("Advanced Settings")
        settings_mode = st.radio("Settings Mode", ["Default", "Custom"])

        # Initialize default variables so they exist even if "Default" is selected
        ui_temp = 0.0
        ui_instructions = None
        ui_tags = "Auto-Researcher"

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
            ui_tags = st.text_input(
                "Obsidian Tags (comma separated)",
                value="Auto-Researcher, AI"
            )

    # --- MAIN SEARCH INTERFACE ---
    # Hide the search bar if we are currently editing a final draft in the HITL
    if not st.session_state.ai_response:
        st.write("Welcome to the workspace. Ask a question based on your Raw Sources.")

        with st.form("research_form"):
            query = st.text_input("Enter your research topic:")
            submitted = st.form_submit_button("Generate Draft")

            if submitted and query:
                if not selected_models:
                    st.warning("Please select at least one model from the sidebar first.")
                else:
                    # Clear any old drafts just in case
                    st.session_state.drafts = {}

                    # FIX : Loop through all selected models sequentially to prevent Mac memory crash
                    for model in selected_models:
                        with st.spinner(f"Generating draft with {model}... (This happens sequentially)"):
                            result = generate_research(query, model_name=model, temperature=ui_temp,
                                                       custom_instructions=ui_instructions)
                            st.session_state.drafts[model] = result

                    st.session_state.active_query = query
                    st.rerun()

    # --- THE DRAFTS WORKSPACE ---
    if st.session_state.drafts and not st.session_state.ai_response:
        st.markdown("---")
        st.subheader("⚖️ Model Comparison Workspace")
        st.caption(f"**Current Query:** {st.session_state.active_query}")

        # The "+" Feature: Find models we haven't run yet
        unrun_models = [m for m in available_models if m not in st.session_state.drafts]

        if unrun_models:
            with st.expander("➕ Add another model to comparison"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    new_model = st.selectbox("Select Model to Add", unrun_models, label_visibility="collapsed")
                with col2:
                    if st.button("Generate & Add"):
                        with st.spinner(f"Spinning up {new_model}..."):
                            # Reuse the active query so the user doesn't type it again
                            new_result = generate_research(st.session_state.active_query, model_name=new_model,
                                                           temperature=ui_temp, custom_instructions=ui_instructions)
                            st.session_state.drafts[new_model] = new_result
                            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Draw dynamic columns based on how many drafts we have
        draft_cols = st.columns(len(st.session_state.drafts))

        for idx, (model_key, draft_text) in enumerate(st.session_state.drafts.items()):
            with draft_cols[idx]:
                st.markdown(f"### `{model_key}`")
                # Show the text in a read-only scrollable container
                st.text_area("Draft Output", value=draft_text, height=400, disabled=True, key=f"text_{model_key}")

                # The crucial selection button
                if st.button(f"✨ Send {model_key} to Editor", key=f"btn_{model_key}", use_container_width=True):
                    # Push the winning draft to the final editor and clear the workspace
                    st.session_state.ai_response = draft_text
                    st.session_state.drafts = {}
                    st.session_state.active_query = ""
                    st.rerun()

        # Added a global discard button for the drafts view so you aren't stuck if you hate all outputs!
        st.markdown("---")
        if st.button("🗑️ Discard All Drafts & Start Over", type="primary"):
            st.session_state.drafts = {}
            st.session_state.active_query = ""
            st.rerun()

    # --- HITL EDITOR ---
    if st.session_state.ai_response:
        st.markdown("---")
        st.subheader("📝 Human-in-the-Loop Editor")

        edited_content = st.text_area("Review and tweak the winning output before saving:",
                                      value=st.session_state.ai_response,
                                      height=400)
        note_title = st.text_input("Obsidian Note Title:", value="AI Research Notes")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save to Obsidian", use_container_width=True):
                success, message = save_to_obsidian(note_title, edited_content, custom_tags=ui_tags)
                if success:
                    st.session_state.save_success = True
                    st.session_state.save_message = f"File successfully created in your vault at:\n`{message}`"
                    st.session_state.ai_response = ""
                    st.rerun()
                else:
                    st.error(f"Failed to save file: {message}")
        with col2:
            if st.button("🗑️ Discard & Start Over", type="primary", use_container_width=True):
                st.session_state.ai_response = ""
                st.rerun()


if __name__ == "__main__":
    main()