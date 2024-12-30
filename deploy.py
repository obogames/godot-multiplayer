import os
import sys
import zipfile
import platform

import boto3

# doesn't work:
# godot --headless --export-release Uwupoly .
bucket_name = "dkgs-public"
region = "eu-central-1"


export_path = None
with open('export_presets.cfg') as fh:
  for line in fh:
    if line.startswith("export_path="):
      export_path = line.split('=')[1].rstrip('\n').strip('"')

baseexec, base_ext = os.path.splitext(os.path.basename(export_path))
# _dir = os.path.dirname(export_path) or './'
export_dir = os.path.dirname(export_path)

# files: list = [
#   os.path.join('./icon.svg')
# ]

# if platform.system() == 'Windows':
#   files.extend([
#     os.path.join(_dir, baseexec+'.exe'),
#     os.path.join(_dir, baseexec+'.console.exe'),
#     os.path.join(_dir, baseexec+'.pck'),
#   ])

#   for file in os.listdir(_dir):
#     if file.endswith('.dll'):
#       files.append(os.path.join(_dir, file))

zip_filepath = baseexec+'.zip'
with zipfile.ZipFile(zip_filepath, 'w') as zipf:
  for file in os.listdir(export_dir):
    zipf.write(os.path.join(export_dir, file), arcname=file.split('/')[-1])
  zipf.write('./icon.svg')

print("Uploading bundle to S3...")
key = os.path.basename(zip_filepath)
s3 = boto3.client('s3', region_name=region)
resp = s3.upload_file(
  Filename=os.path.basename(zip_filepath),
  Bucket=bucket_name,
  Key=key
)


# https://dkgs-public.s3.eu-central-1.amazonaws.com/yolo.zip
url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{key}"
print(f"URL:\n{url}")

# Clean up
os.unlink(zip_filepath)
