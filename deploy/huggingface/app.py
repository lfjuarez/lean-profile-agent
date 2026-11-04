"""Hugging Face Space entry point.

The Space runs the same FastAPI app as Cloud Run. The package comes from requirements.txt;
the knowledge base is fetched from the public repo at the same pinned commit, and CV PDFs
uploaded next to this file are served at /cv/.
"""

import os
import pathlib
import shutil
import subprocess

REF = "c6903535d48ec36fadf3a45fd1dfcadadb628240"
HERE = pathlib.Path(__file__).resolve().parent
REPO = pathlib.Path("/tmp/lean-profile-agent")

if not (REPO / "knowledge").is_dir():
    subprocess.run(
        ["git", "clone", "--quiet", "https://github.com/lfjuarez/lean-profile-agent.git", str(REPO)],
        check=True,
    )
    subprocess.run(["git", "-C", str(REPO), "checkout", "--quiet", REF], check=True)

cv_dir = REPO / "cv"
cv_dir.mkdir(exist_ok=True)
for pdf in HERE.glob("*.pdf"):
    shutil.copy(pdf, cv_dir / pdf.name)

os.environ.setdefault("PROFILE_KB_DIR", str(REPO / "knowledge"))
os.environ.setdefault("PROFILE_CV_DIR", str(cv_dir))
os.environ.setdefault("PROFILE_PROVIDER", "gemini")
os.environ.setdefault("GEMINI_MODEL", "gemini-flash-lite-latest")

import uvicorn  # noqa: E402

uvicorn.run("profile_agent.web:get_app", factory=True, host="0.0.0.0", port=7860, proxy_headers=True)
