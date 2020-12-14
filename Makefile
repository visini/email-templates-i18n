preview:
	# @echo http://127.0.0.1:8000/preview.html
	# @echo http://127.0.0.1:8000/preview.txt
	# poetry run uvicorn "src.preview:app" --reload
	find src/ | entr -rc poetry run uvicorn "utils.preview:app"