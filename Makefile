preview:
	find src/ | entr -rc poetry run uvicorn "utils.preview:app"