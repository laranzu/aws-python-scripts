# aws-python-scripts

Python utility code and scripts for working with the AWS CLI.

I believe in building IT systems with scripts rather than web
interfaces, not because it's traditional but because automation
is more reliable and repeatable. The `aws` command line tool is
powerful and well documented, but it still takes many steps to
accomplish common tasks. I prefer Python over Bash for such
scripts because IMNSHO Python is easier to read and has better
libraries for string handling and JSON.

Everything here is under the MIT license.

##

    awsutil.py

This is the actual utility code. Most important is function `run()`
to execute a single `aws` command, check for errors, and either
display the error message and re-raise or return the command
output.

Other utility funcs are for testing that the AWS CLI is present,
that the user is logged in, getting details about the current
user/profile.

And finally there is `allowCancel()` which gives the user a short
pause to Control-C before doing something permanent. HCI research
has shown that asking people "are you sure you want to X?" rarely
works, because the user is focussed on the steps needed to get
a task done, not the outcome, so typing "y" or "yes" becomes
automatic. This function instead adds a short delay, which still
gives you a chance to realise "oh crap!" but doesn't require
any action if it really is what you wanted. And you can start a
script and then go get a coffee if you are really confident.

    makeStaticSite.py

Creates an S3 bucket (if necessary), uploads a source directory
into it, and configures as a static web page.

    testaws.py

Very simple test program.
