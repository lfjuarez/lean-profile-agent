# CV files

Drop the CV PDFs here. They are served at `/cv/<file>` and linked from the page:

- `Leandro_Juarez_CV_EN.pdf`
- `Leandro_Juarez_CV_ES.pdf`

The PDFs are git-ignored on purpose (deploy-time assets, not repository content). The Docker
build copies this folder, so the files must exist locally when you run `deploy/cloud-run.sh`.
