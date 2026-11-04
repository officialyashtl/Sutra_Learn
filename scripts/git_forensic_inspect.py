import os
import sys

def main():
    if not os.path.exists(".git"):
        print("No .git directory found.")
        return

    # 1. Read HEAD
    with open(".git/HEAD", "r") as f:
        head = f.read().strip()
    print("HEAD reference:", head)

    commit = None
    if head.startswith("ref: "):
        ref = head[5:]
        ref_path = os.path.join(".git", ref.replace("/", os.sep))
        if os.path.exists(ref_path):
            with open(ref_path, "r") as f:
                commit = f.read().strip()
    else:
        commit = head
    print("Current commit:", commit)

    # 2. Read logs/HEAD (last 5 commits)
    log_path = os.path.join(".git", "logs", "HEAD")
    if os.path.exists(log_path):
        print("\nRecent Git Commit History (from .git/logs/HEAD):")
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        for line in lines[-5:]:
            parts = line.strip().split("\t")
            meta = parts[0] if parts else ""
            msg = parts[1] if len(parts) > 1 else ""
            tokens = meta.split(" ")
            old_h = tokens[0] if len(tokens) > 0 else ""
            new_h = tokens[1] if len(tokens) > 1 else ""
            print(f"- Commit: {new_h[:8]} | Message: {msg}")

    # 3. Check git config
    config_path = os.path.join(".git", "config")
    if os.path.exists(config_path):
        print("\nGit Config (Remotes):")
        with open(config_path, "r") as f:
            for l in f:
                if "url =" in l or "[remote" in l or "[branch" in l:
                    print("  ", l.strip())

if __name__ == "__main__":
    main()

