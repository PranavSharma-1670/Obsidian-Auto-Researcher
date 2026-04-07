import streamlit as st
from rag_pipeline import generate_research
from exporter import save_to_obsidian
import ollama

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
if "winning_model" not in st.session_state:
    st.session_state.winning_model = ""

def main():
    st.title("🕵️ Obsidian Auto-Researcher")
    st.markdown("### Version 1.2 - Multi-Model Comparison Grid")

    if st.session_state.save_success:
        st.success(st.session_state.save_message)
        st.balloons()
        st.session_state.save_success = False
        st.session_state.save_message = ""

    # --- SIDEBAR & SETTINGS ---
    with st.sidebar:
        st.header("Initial Model Selection")
        # Ask Ollama what is physically installed on your Mac right now!
        try:
            local_models_info = ollama.list()
            available_models = [m['model'] for m in local_models_info['models']] # Extract the names of the models
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
    if not st.session_state.ai_response and not st.session_state.drafts:
        st.write("Welcome to the workspace. Ask a question based on your Raw Sources.")

        with st.form("research_form"):
            query = st.text_input("Enter your research topic:")
            submitted = st.form_submit_button("Generate Draft")

            if submitted and query:
                if not selected_models:
                    st.warning("Please select at least one model from the sidebar first.")
                else:
                    st.session_state.drafts = {}
                    # FIX : Loop through all selected models sequentially to prevent Mac memory crash
                    for model in selected_models:
                        with st.spinner(f"Generating draft with {model}..."):
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
        draft_items = list(st.session_state.drafts.items())

        for i in range(0, len(draft_items), 2):
            cols = st.columns(2)  # Always create exactly 2 columns per row

            # First item in the row
            with cols[0]:
                model_key, draft_text = draft_items[i]
                st.markdown(f"### `{model_key}`")
                st.text_area("Draft Output", value=draft_text, height=400, disabled=True, key=f"text_{model_key}")
                if st.button(f"✨ Send {model_key} to Editor", key=f"btn_{model_key}", use_container_width=True):
                    st.session_state.ai_response = draft_text
                    st.session_state.winning_model = model_key  # Remember which one we picked
                    st.rerun()

            # Second item in the row (if it exists)
            if i + 1 < len(draft_items):
                with cols[1]:
                    model_key_2, draft_text_2 = draft_items[i + 1]
                    st.markdown(f"### `{model_key_2}`")
                    st.text_area("Draft Output", value=draft_text_2, height=400, disabled=True,
                                 key=f"text_{model_key_2}")
                    if st.button(f"✨ Send {model_key_2} to Editor", key=f"btn_{model_key_2}", use_container_width=True):
                        st.session_state.ai_response = draft_text_2
                        st.session_state.winning_model = model_key_2
                        st.rerun()

        # Added a global discard button for the drafts view so you aren't stuck if you hate all outputs!
        st.markdown("---")
        if st.button("🗑️ Discard All Drafts & Start Over", type="primary"):
            st.session_state.drafts = {}
            st.session_state.active_query = ""
            st.rerun()

    # --- HITL EDITOR WITH REFERENCE WINDOWS ---
    if st.session_state.ai_response:
        st.markdown("---")
        st.subheader("📝 Human-in-the-Loop Editor")

        # Split the screen: 60% for your editor, 40% for reference materials
        editor_col, ref_col = st.columns([6, 4])

        with editor_col:
            edited_content = st.text_area("Review and tweak the winning output before saving:",
                                          value=st.session_state.ai_response,
                                          height=500)
            note_title = st.text_input("Obsidian Note Title:", value="AI Research Notes")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save to Obsidian", use_container_width=True):
                    success, message = save_to_obsidian(note_title, edited_content, custom_tags=ui_tags)
                    if success:
                        st.session_state.save_success = True
                        st.session_state.save_message = f"File successfully created in your vault at:\n`{message}`"
                        st.session_state.ai_response = ""
                        st.session_state.drafts = {}  # Wipe drafts ONLY on successful save
                        st.session_state.active_query = ""
                        st.rerun()
                    else:
                        st.error(f"Failed to save file: {message}")
            with col2:
                if st.button("🗑️ Discard Draft & Start Over", type="primary", use_container_width=True):
                    st.session_state.ai_response = ""
                    st.session_state.drafts = {}
                    st.session_state.active_query = ""
                    st.rerun()

        # ---------------------------------------------------------
        # NEW FEATURE: Reference Expanders
        # ---------------------------------------------------------
        with ref_col:
            st.markdown("##### 📚 Alternate Drafts")
            st.caption("Choose a tab to view alternate model outputs.")
            reference_models = {k: v for k, v in st.session_state.drafts.items() if k != st.session_state.winning_model}

            if reference_models:
                tabs = st.tabs(list(reference_models.keys()))
                for idx, (model_name, draft_text) in enumerate(reference_models.items()):
                    with tabs[idx]:
                        # The "slider rim" - locks the height to match your main editor
                        with st.container(height=500):
                            st.write(draft_text)

if __name__ == "__main__":
    main()