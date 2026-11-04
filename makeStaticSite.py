#!/usr/bin/env python

""" Usage: makeStaticSite.py bucket-name source-dir
    Create S3 bucket as static website, upload source dir
"""

import json, os, string, sys
from os import path

import awsutil as aws

def makeBucket(name, **config):
    """Use existing, or create if necessary"""
    # At time of writing, must provide LocationConstraint in config
    # Exists?
    out = aws.run("s3api", "list-buckets",
                        "--query", "Buckets[].Name",
                        "--prefix", name)
    buckets = json.loads(out)
    if len(buckets) == 0 or name not in buckets:
        # Create a new bucket
        aws.run("s3api", "create-bucket",
                    "--bucket", name,
                    "--bucket-namespace", "global",
                    "--create-bucket-configuration", json.dumps(config))
    else:
        aws.allowCancel("Overwrite existing bucket {}".format(name))

# Copied from AWS tutorial Hosting a Static Website Using Amazon S3
# https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteAccessPermissionsReqd.html
staticSitePolicy = string.Template('''
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::$BucketName/*"
            ]
        }
    ]
}
''')

def configBucketAccess(name):
    """Allow public read-only access"""
    # Is there a vulnerability between removing the old default and applying
    # the new policy? I don't know, but AWS won't let me reverse the order
    # Remove default
    aws.run("s3api", "delete-public-access-block",
                    "--bucket", name)
    # Set new policy from JSON template
    policy = staticSitePolicy.substitute(BucketName=name)
    # AWS is picky about strings, so convert to JSON canonical and back again
    policy = json.dumps(json.loads(policy))
    aws.run("s3api", "put-bucket-policy",
                    "--bucket", name,
                    "--policy", policy)

def uploadContent(source, bucket):
    """Upload source directory to bucket"""
    dest = "s3://{}/".format(bucket)
    # Add --dryrun to see what would be uploaded without doing so
    out = aws.run("s3", "sync",
                source, dest,
                "--no-follow-symlinks")
    print(out)

def makeBucketIntoSite(source, bucket):
    """Configure S3 bucket as static website"""
    dest = "s3://{}/".format(bucket)
    errName = None
    for target in ("error.html", "404.html"):
        if path.exists(path.join(source, target)):
            errName = target
    if errName is None:
        raise RuntimeError("No error page in {}".format(source))
    aws.run("s3", "website",
                dest,
                "--index-document", "index.html",
                "--error-document", errName)
    # Would be nice to print out URL, but AWS CLI cannot do this

##  Main program

def main(argv):
    if len(argv) == 1:
        print("Usage: {} bucket-name source-dir".format(argv[0]))
        sys.exit(0)
    bucketName = argv[1]
    sourceDir  = argv[2]
    if not (path.exists(sourceDir) and path.isdir(sourceDir)):
            raise RuntimeError("{} is not a directory".format(sourceDir))

    aws.start()
    makeBucket(bucketName, LocationConstraint=aws.config["region"])
    configBucketAccess(bucketName)
    uploadContent(sourceDir, bucketName)
    makeBucketIntoSite(sourceDir, bucketName)

    print("Done! URL is probably")
    print("http://{}.s3-website-{}.amazonaws.com".format(bucketName, aws.config["region"]))

if __name__ == "__main__":
    main(sys.argv)
