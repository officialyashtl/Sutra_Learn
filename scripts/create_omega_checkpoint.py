import os
import shutil
import time

def create_checkpoint():
    ts = time.strftime("%Y%m%d_%H%M%S")
    cp_dir = os.path.join("checkpoints", f"checkpoint_omega_infinity_{ts}")
    os.makedirs(cp_dir, exist_ok=True)
    
    # Backup critical source files and configs
    files_to_backup = [
        ".env",
        os.path.join("backend", ".env"),
        os.path.join("backend", "app", "main.py"),
        os.path.join("backend", "app", "auth.py"),
        os.path.join("backend", "app", "db", "database.py"),
        os.path.join("backend", "app", "db", "crud.py"),
        os.path.join("backend", "app", "services", "ai.py"),
        os.path.join("backend", "app", "services", "audit.py"),
        os.path.join("backend", "sutra_learn.db"),
        os.path.join("frontend", "src", "api", "client.ts"),
        os.path.join("frontend", "src", "App.tsx"),
        os.path.join("frontend", "src", "pages", "StudentTutor.tsx"),
        os.path.join("frontend", "src", "pages", "LandingPage.tsx"),
        os.path.join("frontend", "src", "components", "student", "PastSessionsPanel.tsx")
    ]
    
    backed_up = []
    for f in files_to_backup:
        if os.path.exists(f):
            dest = os.path.join(cp_dir, f.replace("/", os.sep))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(f, dest)
            backed_up.append(f)
            
    print(f"Created recovery checkpoint at: {cp_dir}")
    print(f"Backed up {len(backed_up)} files successfully.")
    
    # Save checkpoint manifest
    with open(os.path.join(cp_dir, "MANIFEST.txt"), "w") as mf:
        mf.write(f"OMEGA INFINITY RECOVERY CHECKPOINT\n")
        mf.write(f"Timestamp: {ts}\n")
        mf.write(f"Base commit: dda0b38e77f3b1ac11555312cff4681b59410c3b\n")
        mf.write(f"Backed up files:\n")
        for b in backed_up:
            mf.write(f"  - {b}\n")

if __name__ == "__main__":
    create_checkpoint()

