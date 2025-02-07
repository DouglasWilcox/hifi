# Post build script
import os
import sys
import json
import boto3
import glob
from github import Github


def main():
    bucket_name = os.environ['BUCKET_NAME']
    upload_prefix = os.environ['UPLOAD_PREFIX']
    context = json.loads(os.environ['GITHUB_CONTEXT'])
    baseUrl = 'https://{}.s3.amazonaws.com/{}/'.format(bucket_name, upload_prefix)
    S3 = boto3.client('s3')
    g = Github(os.environ['GITHUB_TOKEN'])
    repo = g.get_repo(context['repository'])
    pr = repo.get_pull(context['event']['number'])

    path = os.path.join(os.getcwd(), os.environ['ARTIFACT_PATTERN'])
    files = glob.glob(path, recursive=False)
    for archiveFile in files:
        filePath, fileName = os.path.split(archiveFile)
        pr.create_issue_comment("Build artifact uploaded as [{}]({}{})".format(fileName, baseUrl, fileName))
        S3.upload_file(os.path.join(filePath, fileName), bucket_name, upload_prefix + '/' + fileName)

main()
