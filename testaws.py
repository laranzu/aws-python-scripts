#!/usr/bin/env python

# Testing how to run AWS CLI from Python

import aws

aws.start()
print(aws.config)

#out = aws.run("nosuch")

# Should not appear if error
print("Done.")
