import os
import re
from datetime import datetime

OBSIDIAN_VAULT_PATH = "/Users/pranavsharma/Developer/Core_HQ/03_Knowledge_Base"

def get_existing_notes():
    """Reads the Obsidian vault directory and returns a list of .md filenames."""
    if not os.path.exists(OBSIDIAN_VAULT_PATH):
        return []

    # Get all .md files and strip the extension for a cleaner UI
    files = [f.replace(".md", "") for f in os.listdir(OBSIDIAN_VAULT_PATH) if f.endswith(".md")]
    return sorted(files)

def sanitize_filename(title):
    """Removes illegal characters from the title so macOS doesn't throw an error."""
    clean_name = re.sub(r'[\\/*?:"<>|]', "", title)
    return clean_name.strip()

def save_to_obsidian(title, content, custom_tags="Auto-Researcher", mode="create"):
    """Writes the final text to a .md file in the Obsidian vault."""
    if not os.path.exists(OBSIDIAN_VAULT_PATH):
        return False, f"Could not find the vault path: {OBSIDIAN_VAULT_PATH}"

    safe_title = sanitize_filename(title)
    if not safe_title:
        safe_title = f"AI_Research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    filename = f"{safe_title}.md"
    file_path = os.path.join(OBSIDIAN_VAULT_PATH, filename)

    today = datetime.now().strftime('%Y-%m-%d')
    now_time = datetime.now().strftime('%H:%M:%S')

    try:
        if mode == "create":
            # --- NORMAL CREATE LOGIC ---
            tag_list = [t.strip() for t in custom_tags.split(",") if t.strip()]
            formatted_tags = "[" + ", ".join(tag_list) + "]"

            frontmatter = f"---\ntags: {formatted_tags}\ndate: {today}\n---\n\n"
            final_content = frontmatter + content

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(final_content)
            return True, file_path

        elif mode == "append":
            # --- APPEND LOGIC ---
            # Do NOT add frontmatter. Add a clear markdown divider with a timestamp so
            # you know exactly when this block of research was added.
            separator = f"\n\n---\n### 📝 Appended Research ({today} at {now_time})\n\n"
            final_content = separator + content

            # Use 'a' to append to the end of the file instead of 'w' to overwrite
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(final_content)
            return True, file_path

    except Exception as e:
        return False, str(e)