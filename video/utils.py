import os
import subprocess
#from PIL import Image
import boto3
import io
from django.conf import settings
import string
import random
import ffmpeg
import sys
import datetime
MAX_SIZE_FULL = 600
MAX_SIZE_FLOOR = 731
MAX_SIZE_THUMB = 50
THUMB_W180 = 180
THUMB_90x90 = 90

 
def get_random_num():
    return ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 8))

def get_video_duration(path):
    try:
        input_video = path.url
        p1 = subprocess.Popen(['ffmpeg',  '-i', input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p2 = subprocess.Popen(["grep",  "-o", "-P", "(?<=Duration: ).*?(?=,)"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        vtime = str(p2.communicate()[0].decode("utf-8").strip())
        return time_to_second(vtime)
    except Exception as e:
        print('error in get_video_duration', str(e))
    return 10

def get_thumbnail(path):
    in_filename = path.url
    probe = ffmpeg.probe(in_filename)
    time = float(probe['streams'][0]['duration']) // 2
    width = probe['streams'][0]['width']
    out_filename = get_random_num()+'.jpg'
    try:
        (
            ffmpeg
            .input(in_filename, ss=time)
            .filter('scale', width, -1)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name='ap-south-1')   
        client.upload_file(out_filename, 'gtouch-static', 'static/video_thumbnail/'+out_filename)
        return 'static/video_thumbnail/'+out_filename
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)



def time_to_second(time_string):
    time_string = time_string.split('.')[0]
    date_time = datetime. datetime. strptime(time_string, "%H:%M:%S")
    a_timedelta = date_time - datetime. datetime(1900, 1, 1)
    return int(a_timedelta. total_seconds())

def create_thumb(image_path):
    original_image = Image.open(
        urllib.request.urlopen(image_path)
    )

    in_mem_file = io.BytesIO()
    original_image.save(in_mem_file, format=original_image.format)
    in_mem_file.seek(0)

    width, height = original_image.size
    # jpg, png
    img_format = original_image.format

    # create thumb
    factor_thumb_w180 = (
        (float(THUMB_W180) / width) if (width > THUMB_W180) else 1
    )
    factor_thumb_90x90 = (
        (float(THUMB_90x90) / height)
        if (width < height)
        else (float(THUMB_90x90) / width)
    )
    size_thumb_w180 = (
        int(width * factor_thumb_w180),
        int(height * factor_thumb_w180),
    )
    size_thumb_90x90 = (
        int(width * factor_thumb_90x90),
        int(height * factor_thumb_90x90),
    )

    thumb_image_w180 = original_image.resize(
        size_thumb_w180, Image.ANTIALIAS
    )
    thumb_image_90x90 = original_image.resize(
        size_thumb_90x90, Image.ANTIALIAS
    )

    (
        thumb_w180_file_path,
        thumb_90x90_file_path,
    ) = thumbnail_w180_90x90_full_file_paths(find.image.name)
    print(thumb_image_w180,thumb_w180_file_path)
    print(thumb_image_90x90,thumb_90x90_file_path)

    save_image_to_s3(
        thumb_image_w180, thumb_w180_file_path, img_format, add_md5=False
    ),
    save_image_to_s3(
        thumb_image_90x90, thumb_90x90_file_path, img_format, add_md5=False
    )