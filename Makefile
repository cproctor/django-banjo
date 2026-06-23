S3_BUCKET = s3://docs.makingwithcode.org/django-banjo/
CF_DISTRIBUTION = EPA6NHZ2LEH1A

.PHONY: build deploy clean

build:
	$(MAKE) -C docs html

deploy: build
	aws s3 sync docs/_build/html $(S3_BUCKET)
	aws cloudfront create-invalidation --distribution-id $(CF_DISTRIBUTION) --paths "/django-banjo/*"

clean:
	$(MAKE) -C docs clean
