capabilities = CAPABILITY_IAM
aws_profile = kablamo-build
aws_region = ap-southeast-2
s3_bucket_files = cdpoc-artifacts-build
tools ?= ../../bin

all: lambda_uploads default

lambda_uploads:
	@echo ---------- $@ ----------
	@$(build_dir_exists)
	aws \
	$(if ${aws_region},--region ${aws_region},) \
	$(if ${aws_profile},--profile ${aws_profile},) \
	s3 sync ../../functions/packages \
	s3://${s3_bucket_files}/quickstart-git2s3/functions/packages
