#!/usr/bin/env python

# Testing how to run AWS CLI from Python

import awsutil as aws

aws.start()
print(aws.config)

#out = aws.run("nosuch")

# Should not appear if error
print("Done.")
