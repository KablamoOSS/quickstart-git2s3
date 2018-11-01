# quickstart-git2s3

## Git webhooks with AWS services

### Deployment with AWS CLI and make

There is a simplified procedure to deploy the Git2S3 solution to AWS by means
of AWS CLI, invoked from the Makefile. In order to employ it, make sure to have
the latest version of AWS CLI installed, as well as the `make`.

Please perform the following changes in the [makefile.inc](deployment/build/makefile.inc) file:

- set `aws_profile` variable to the name of the appropriate AWS account profile
  set in your `~/.aws/credentials` and `aws_region` to the AWS region where the
  CloudFormation stack should be deployed.
- set `s3_bucket_files` variable to the existing S3 bucket where the code for
  all Lambda functions will be uploaded for deployment

Make sure to also edit the [CDPoC-GitS3.parameters](deployment/build/CDPoC-Git2S3.parameters) file:

- cross check the value of the `QSS3BucketName` parameter, holding the name of
  the S3 bucket for Lambda code, should be the same as `s3_bucket_files`
  variable from the `makefile.inc` above
- `OutputBucketName` parameter: set to the name of the S3 bucket where the
  checked-out code from Git will be stored

Now you can run `make` in the `deployment` directory.

### Changes to the code of Lambda functions

In case any changes are done to the source code of Lambda functions in
`functions/source/<Name of the Lambda>/lambda_function.py`, the updated
file should be added to the `lambda.zip` archive under respective directory
in `functions/packages/`. I.e. change directory to the
`functions/source/<Name of the Lambda>/` and run

    zip -u ../../../functions/packages/<Name of the Lambda>/lambda.zip lambda_function.py 

then, run `make` as outlined in the above paragraph.

### Linking your Git repository to Amazon S3 and AWS services for continuous code integration, testing, and deployment 

This Quick Start deploys HTTPS endpoints and AWS Lambda functions for implementing webhooks, to enable event-driven integration between Git services and Amazon Web Services (AWS) on the AWS Cloud.

After you deploy the Quick Start, you can set up a webhook that uses the endpoints to create a bridge between your Git repository and AWS services like AWS CodePipeline and AWS CodeBuild. With this setup, builds and pipeline executions occur automatically when you commit your code to a Git repository, and your code can be continuously integrated, tested, built, and deployed on AWS with each change. 

The Quick Start includes an AWS CloudFormation template that automates the deployment. You can also use the AWS CloudFormation template as a starting point for your own implementation.

![Quick Start architecture for implementing webhooks on AWS](https://d0.awsstatic.com/partner-network/QuickStart/datasheets/git-to-s3-webhooks-architecture-on-aws.png)

For implementation details, deployment instructions, and customization options, see the [deployment guide](https://fwd.aws/QQBRr).

To post feedback, submit feature ideas, or report bugs, use the **Issues** section of this GitHub repo.
If you'd like to submit code for this Quick Start, please review the [AWS Quick Start Contributor's Kit](https://aws-quickstart.github.io/). 
