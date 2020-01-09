import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

# Using the boto 3 resource command
s3 = boto3.resource('s3',config = Config(signature_version='s3v4'))
portfolio_bucket=s3.Bucket('portfolio.quichenews.net')
build_bucket=s3.Bucket('portfoliobuild.quichenews.net')

#String IO just holds a file in memory
portfolio_zip=StringIO.StringIO()

# Downloads the file 'portfoliobuild.zip' from the build_bucket and loads it into the String IO param portfolio_zip
build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj= myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj,nm,
            ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0],
            'ACL':'public-read'})
#ExtraArgs here just sets all the objects in the zip file to public and also sets the right Mime type depending upon the file extension

        #portfolio_bucket.Object(nm).Acl().put(ACL='public_read')
#{}
