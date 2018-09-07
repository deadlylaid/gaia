import botocore

class NoCredentialError(botocore.exceptions.NoCredentialsError):
    fmt = "please create credential in `~/.aws/` Referer - https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html"
