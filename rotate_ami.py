import os, argparse
from boto.ec2 import connect_to_region
# magnus

parser = argparse.ArgumentParser(description='This utility will rotate AMI')

parser.add_argument('--name', help='Name that should be rotated. All AMI that contains <name> will be rotated.', required=True)
parser.add_argument('--region', help='Region to search AMI in.', choices=['us-east-1', 'us-west-2', 'us-west-1','eu-west-1','eu-central-1','ap-southeast-1','ap-southeast-2','ap-northeast-1','sa-east-1'], default="eu-west-1")
parser.add_argument('--count', metavar='N', type=int, help='Number of AMI to keep. The rest will be deregistered.', required=True)
parser.add_argument('--dryrun', action='store_true', help='If set, no AMI will be deregistered.', default=False)
args = parser.parse_args()

if not os.environ["AWS_ACCESS_KEY"] or not os.environ["AWS_SECRET_KEY"]:
    print "Missing AWS_ACCESS_KEY or AWS_SECRET_KEY environment variables"

conn = connect_to_region(args.region, aws_access_key_id=os.environ["AWS_ACCESS_KEY"], aws_secret_access_key=os.environ["AWS_SECRET_KEY"])

to_rotate=list()
for image in sorted(conn.get_all_images(owners="self"), key=lambda k: k.creationDate):
    if args.name in image.name and image.state == "available":
        to_rotate.append(image)

print "Found %d images." % len(to_rotate)

to_deregister = to_rotate[:-args.count]
#to_keep = to_rotate[-args.count:]

for image in to_rotate:
    if len([key for key,val in image.tags.iteritems() if key=="build" and val=="latest"]) > 0:
        if args.dryrun:
            print "DRYRUN: would remove tag build=latest from "+image.id
        else:
            print "Removing tag build=latest from "+image.id
            image.remove_tag("build","latest")

for image in to_deregister:
    if args.dryrun:
        print "DRYRUN: would deregister "+image.id, image.name
    else:
        print "Deregister "+image.id, image.name
        try:
            image.deregister()
        except Exception as e:
            print "Failed to deregister "+image.id+": "+str(e)

if len(to_rotate) > 0:
    if args.dryrun:
        print "DRYRUN: would add tag build=latest to "+to_rotate[-1].id
    else:
        print "Adding tag build=latest to "+to_rotate[-1].id
        to_rotate[-1].add_tag("build", "latest")
