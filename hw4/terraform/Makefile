REPO_SRC_FLAG=--repo DataTalksClub/nyc-tlc-data
GZIPPED := $(wildcard *.csv.gz)
GUNZIPPED := $(GZIPPED:.gz=)

dl-assets:
	echo Download green for 2019-2020
	gh release ${REPO_SRC_FLAG} download green \
		--pattern 'green*2019*.csv.gz' \
		--pattern 'green*2020*.csv.gz'

	echo Downloading yellow for 2019-2020
	gh release ${REPO_SRC_FLAG} download yellow \
		--pattern 'yellow*2019*.csv.gz' \
		--pattern 'yellow*2020*.csv.gz'

	echo Downloading FHV for 2019
	gh release ${REPO_SRC_FLAG} download fhv \
		--pattern 'fhv*2019*.csv.gz' \

.PHONY: gunzip_all
gunzip_all: $(GUNZIPPED)

%: %.gz
	gunzip -k $<

fmt:
	terraform fmt
keys-list:
	@gcloud iam service-accounts keys list --iam-account=${GCP_SA_EMAIL}

tell-bucket:
	@echo $(shell terraform output -raw hw4-bucket-name)

upload:
	uv run upload_csv.py $(shell terraform output -raw hw4-bucket-name)
