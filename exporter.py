import os
import re
from datetime import datetime

# Your specific Obsidian Vault path
OBSIDIAN_VAULT_PATH = "/Users/pranavsharma/Developer/Core_HQ/03_Knowledge_Base"

def sanitize_filename(title):
    """Removes illegal characters from the title so macOS doesn't throw an error."""
    clean_name = re.sub(r'[\\/*?:"<>|]', "", title)
    return clean_name.strip()


def save_to_obsidian(title, content, custom_tags="Auto-Researcher"):
    """Writes the final text to a .md file in the Obsidian vault."""

    # 1. Safety check
    if not os.path.exists(OBSIDIAN_VAULT_PATH):
        return False, f"Could not find the vault path: {OBSIDIAN_VAULT_PATH}"

    # 2. Clean the filename
    safe_title = sanitize_filename(title)
    if not safe_title:
        # Fallback if the user left the title blank
        safe_title = f"AI_Research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    filename = f"{safe_title}.md"
    file_path = os.path.join(OBSIDIAN_VAULT_PATH, filename)

    # 3. Create Obsidian Frontmatter
    today = datetime.now().strftime('%Y-%m-%d')

    # Convert a comma-separated string "Auto-Researcher, AI" into a list format Obsidian likes
    tag_list = [t.strip() for t in custom_tags.split(",") if t.strip()]
    formatted_tags = "[" + ", ".join(tag_list) + "]"

    frontmatter = f"---\ntags: {formatted_tags}\ndate: {today}\n---\n\n"
    final_content = frontmatter + content

    # 4. Write the physical file
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(final_content)
        return True, file_path
    except Exception as e:
        return False, str(e)