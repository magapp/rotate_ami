# rotate_ami
This Python script rotate and only keep most recent AMIs on Amazon. This is nice if you build AMI automatically from Packer and/or Jenkins.

# Usage
```
# export AWS_ACCESS_KEY=<access key>
# export AWS_SECRET_KEY=<secret key>
# python rotate_ami.py --name mongodb --count 3 --region eu-west-1
Found 5 images.
Deregister: ami-xxxxxxxx mongodb-1432236098
Deregister: ami-xxxxxxxx mongodb-1432236887
```

The command above will get all AMIs that has a name that contains "mongodb" and keep to most three recent. The most recent will be tagged with tag build=latest.


# Dependency
pip install boto

pip install argparse
