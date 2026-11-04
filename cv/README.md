# CV files

Drop the CV PDFs here. They are served at `/cv/<file>` and linked from the page:

- `Leandro_Juarez_CV_EN.pdf`
- `Leandro_Juarez_CV_ES.pdf`

The PDFs are git-ignored on purpose (deploy-time assets, not repository content). The Docker
build copies this folder, so the files must exist locally when you run `deploy/cloud-run.sh`.

They are printed from the CV page (`/cv?lang=es` and `/cv?lang=en`) with `deploy/build-cv-pdfs.sh` while the app runs locally; regenerate them whenever the knowledge base changes.
