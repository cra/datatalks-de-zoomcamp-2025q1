fmt:
	terraform fmt
keys-list:
	@gcloud iam service-accounts keys list --iam-account=${GCP_SA_EMAIL}

tell-bucket:
	@echo $(shell terraform output -raw hw3-bucket-name)

upload:
	uv run upload_script.py $(shell terraform output -raw hw3-bucket-name)
