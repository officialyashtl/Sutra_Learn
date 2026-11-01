import subprocess
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
OUTPUT_DIR = ROOT_DIR / "screenshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PYTHON_EXE = BACKEND_DIR / ".venv" / "Scripts" / "python.exe"
if not PYTHON_EXE.exists():
    PYTHON_EXE = Path(sys.executable)

SCREENS = [
    ("01_root_gateway", "http://127.0.0.1:5173/"),
    ("02_student_login", "http://127.0.0.1:5173/student/login"),
    ("03_teacher_login", "http://127.0.0.1:5173/teacher/login"),
    ("04_student_home", "http://127.0.0.1:5173/student/home"),
    ("05_student_pathway", "http://127.0.0.1:5173/student/pathway"),
    ("06_student_lesson", "http://127.0.0.1:5173/student/lesson/MATH-C01"),
    ("07_student_assessment", "http://127.0.0.1:5173/student/assessment/MATH-C01"),
    ("08_student_progress", "http://127.0.0.1:5173/student/progress"),
    ("09_teacher_dashboard", "http://127.0.0.1:5173/teacher/dashboard"),
    ("10_teacher_learners", "http://127.0.0.1:5173/teacher/learners"),
    ("11_teacher_profile", "http://127.0.0.1:5173/teacher/learners/student-01"),
    ("12_teacher_insights", "http://127.0.0.1:5173/teacher/insights"),
    ("13_teacher_interventions", "http://127.0.0.1:5173/teacher/interventions"),
    ("14_teacher_audit", "http://127.0.0.1:5173/teacher/audit"),
    ("15_student_tutor", "http://127.0.0.1:5173/student/tutor"),
    ("16_teacher_assistant", "http://127.0.0.1:5173/teacher/assistant"),
]

VIEWPORTS = [
    ("desktop", 1440, 960),
    ("tablet", 1024, 768),
    ("mobile", 390, 844),
]


def is_url_alive(url: str, timeout: float = 1.0) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status in (200, 304)
    except Exception:
        return False


def capture(screen_name, url, vp_name, width, height):
    out_file = OUTPUT_DIR / f"{screen_name}_{vp_name}.png"
    args = [
        CHROME_PATH,
        "--headless=new",
        f"--user-data-dir={os.environ.get('TEMP', 'C:/tmp')}/chrome_snap_{vp_name}",
        f"--window-size={width},{height}",
        "--hide-scrollbars",
        "--virtual-time-budget=2500",
        f"--screenshot={out_file}",
        url,
    ]
    res = subprocess.run(args, capture_output=True)
    if out_file.exists():
        size_kb = round(out_file.stat().st_size / 1024, 1)
        print(f"  [OK] {screen_name:25} ({vp_name:7} {width}x{height}) -> {out_file.name} ({size_kb} KB)")
        return True
    else:
        print(f"  [ERR] Failed to capture {screen_name} ({vp_name}): {res.stderr.decode('utf-8', errors='ignore')}")
        return False


def main():
    print("=" * 70)
    print("SUTRA LEARN — BROWSER VISUAL SCREENSHOT VERIFICATION")
    print(f"Targeting: {len(SCREENS)} screens x {len(VIEWPORTS)} viewports")
    print("=" * 70)

    backend_proc = None
    frontend_proc = None

    try:
        # Check if backend running
        if not is_url_alive("http://127.0.0.1:8000/api/v1/health"):
            print("Starting local backend server on 127.0.0.1:8000...")
            backend_env = os.environ.copy()
            backend_env["PYTHONPATH"] = str(BACKEND_DIR)
            backend_proc = subprocess.Popen(
                [
                    str(PYTHON_EXE),
                    "-m",
                    "uvicorn",
                    "app.main:app",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "8000",
                    "--log-level",
                    "warning",
                ],
                cwd=str(BACKEND_DIR),
                env=backend_env,
            )
            for _ in range(15):
                time.sleep(0.4)
                if is_url_alive("http://127.0.0.1:8000/api/v1/health"):
                    print("Backend server is healthy.")
                    break

        # Check if frontend running
        if not is_url_alive("http://127.0.0.1:5173/"):
            print("Starting local frontend preview on 127.0.0.1:5173...")
            npx_cmd = "npx.cmd" if sys.platform == "win32" else "npx"
            frontend_proc = subprocess.Popen(
                [npx_cmd, "vite", "preview", "--port", "5173", "--host", "127.0.0.1"],
                cwd=str(FRONTEND_DIR),
            )
            for _ in range(15):
                time.sleep(0.4)
                if is_url_alive("http://127.0.0.1:5173/"):
                    print("Frontend preview server is healthy.")
                    break

        success_count = 0
        total_count = len(SCREENS) * len(VIEWPORTS)

        for screen_name, url in SCREENS:
            for vp_name, w, h in VIEWPORTS:
                if capture(screen_name, url, vp_name, w, h):
                    success_count += 1

        print("\n" + "=" * 70)
        print(f"CAPTURED {success_count}/{total_count} SCREENSHOTS TO {OUTPUT_DIR}")
        print("=" * 70)

    finally:
        if frontend_proc:
            print("Shutting down frontend preview...")
            frontend_proc.terminate()
            try:
                frontend_proc.wait(timeout=3)
            except Exception:
                frontend_proc.kill()

        if backend_proc:
            print("Shutting down backend server...")
            backend_proc.terminate()
            try:
                backend_proc.wait(timeout=3)
            except Exception:
                backend_proc.kill()


if __name__ == "__main__":
    main()
