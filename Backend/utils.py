import os
import shutil


def get_github_username(links):
    github_profile = ""
    for link in links:
        if "github.com" in link:
            parts = link.split("/")
            github_profile = (
                len(parts) > parts.index("github.com") + 1
                and parts[parts.index("github.com") + 1]
            )
            if github_profile == "":
                github_profile = "Profile not found"
            break

    return github_profile


def clear_directory(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
