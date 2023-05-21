
test:
	bundle install && bundle exec jekyll serve


# make notion_export_to_md NOTION_EXPORT_ZIP_FILE=<NOTION_EXPORT_ZIP_FILE>
NOTION_EXPORT_ZIP_FILE=
notion_export_to_md:
	python _scripts/import_notion_md.py --notion-md-zip=$(NOTION_EXPORT_ZIP_FILE)

