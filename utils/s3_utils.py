from six import BytesIO

import boto3
import re
import time
from hashlib import md5
from os import path

from django.conf import settings

# from storages.backends.s3boto import S3BotoStorage
from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.key import Key

MD5_HEXDIGEST_REGEX = re.compile("([A-Fa-f0-9]{32})")

COMMON_EXTENSIONS = ({'.bmp': 'image/x-ms-bmp',
                      '.gif': 'image/gif',
                      '.png': 'image/png',
                      '.jpe': 'image/jpeg',
                      '.jpeg': 'image/jpeg',
                      '.jpg': 'image/jpeg',
                      '.tif': 'image/tiff',
                      '.tiff': 'image/tiff',
                      '.txt': 'text/plain', },)


def add_md5_to_filename(filename, md5_hexdigest):
    """
    add md5 to file name and remove old mdf if present
    :param filename: full file name
    :param md5_hexdigest: md5 to insert
    :return: full file name whit md5
    >>> add_md5_to_filename('/finds/myfind.png', md5('content'.encode()).hexdigest())
    '/finds/myfind.9a0364b9e99bb480dd25e1f0284c8555.png'

    >>> add_md5_to_filename('/finds/myfind.12345678901234567890123456789012.png', md5('content'.encode()).hexdigest())
    '/finds/myfind.9a0364b9e99bb480dd25e1f0284c8555.png'
    """
    file_path, file_extension = path.splitext(filename)
    if MD5_HEXDIGEST_REGEX.match(file_path.split('.')[-1]):
        file_path = file_path[:-33]
    return "{0}.{1}{2}".format(file_path, md5_hexdigest, file_extension)


def init_s3_obj():
    """
    create boto.s3.key and init from settings
    :return: boto.s3.key.Key object
    >>> type(init_s3_obj())
    <class 'boto.s3.key.Key'>
    """

    if '.' in settings.AWS_STORAGE_BUCKET_NAME:
        connection = S3Connection(settings.AWS_S3_ACCESS_KEY_ID, settings.AWS_S3_SECRET_ACCESS_KEY,
                                  calling_format=OrdinaryCallingFormat())
    else:
        connection = S3Connection(settings.AWS_S3_ACCESS_KEY_ID, settings.AWS_S3_SECRET_ACCESS_KEY)

    bucket = connection.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
    return Key(bucket=bucket)


def store_s3(filename, content, add_md5=None, delete_old=None, md5_hexdigest=None, extra_headers=None, no_cache=None):
    """
    store file to s3, key from settings
    :param filename: full file name
    :param content: file
    :param add_md5: True if you want to add md5 to filename
    :param delete_old: True if old file must be deleted
    :param md5_hexdigest: precalculated md5, if None - auto calculated
    :param extra_headers: dict extra headers, like {"Cache-Control":"no-cache"}
    :param no_cache: True if {"Cache-Control":"no-cache"} header needed
    :return: dict {'new_name': 'media/testFile.png',
                'old_name': 'media/testFile.png',
                's3_response': 44514,
                'time': 1.0104351043701172}
    >>> store_result = store_s3('development/tests/store_s3_test_file.txt', 'file content', add_md5=True)
    >>> store_result.get('s3_response')
    12
    >>> store_result.get('new_name')[-55:]
    'store_s3_test_file.d10b4c3ff123b26dc068d43a8bef2d23.txt'
    """
    timestamp = time.time()  # timestamp to calculate execution time
    if hasattr(settings, 'AWS_LOCATION'):
        filename = '{0}/{1}'.format(settings.AWS_LOCATION, filename)
    s3_obj = init_s3_obj()  # create boto.s3.key and init from settings
    file_path, file_extension = path.splitext(filename)
    content_type = COMMON_EXTENSIONS[0].get(file_extension)  # get content type from dict
    if not content_type:
        content_type = 'application/octet-stream'  # default content  type
    if not type(extra_headers) is dict:
        extra_headers = {}
    extra_headers["Content-Type"] = content_type  # add content type to headers dict
    if no_cache:
        extra_headers["Cache-Control"] = "no-cache"  # add no-cache header
    if add_md5:
        if not md5_hexdigest:
            if isinstance(content, str):
                md5_hexdigest = md5(content.encode()).hexdigest()  # calculate md5
            else:
                md5_hexdigest = md5(content).hexdigest()  # calculate md5

        s3_obj.key = add_md5_to_filename(filename, md5_hexdigest)
    else:
        s3_obj.key = filename
    s3_response = s3_obj.set_contents_from_string(content, headers=extra_headers)  # save file to s3
    # delete old image if md5 changed
    if filename != s3_obj.key and delete_old:
        delete_obj_from_s3(filename)
    result = {"s3_response": s3_response, "new_name": s3_obj.key, "old_name": filename, "time": time.time() - timestamp}
    return result


def add_prefix(s3_key):
    """
    >>> add_prefix('key')
    'development/key'

    >>> add_prefix('development/key')
    'development/key'
    """
    if hasattr(settings, 'AWS_LOCATION'):
        prefix = settings.AWS_LOCATION
        if not s3_key[:len(prefix)] == prefix:
            return "{0}/{1}".format(prefix, s3_key)
        else:
            return s3_key
    else:
        return s3_key


def delete_obj_from_s3(s3_key_or_s3_obj):
    """
    delete file from s3
    :param s3_key_or_s3_obj: full file name or  boto.s3.key object
    :return: s3_result
    """
    try:
        if type(s3_key_or_s3_obj) is str:
            s3_obj = init_s3_obj()
            if hasattr(settings, 'AWS_LOCATION'):
                s3_key_or_s3_obj = add_prefix(s3_key_or_s3_obj)
            s3_obj.key = s3_key_or_s3_obj
            s3_result = s3_obj.delete()
        elif type(s3_key_or_s3_obj) is Key:
            s3_result = s3_key_or_s3_obj.delete()
    except:
        return None
    return s3_result


def check_s3(filename):
    """
    :param filename:
    :return:
    >>> check_s3('profile_icon/something_wrong.jpg')
    False
    """
    # check to see if s3 file exists
    s3_obj = init_s3_obj()
    s3_obj.key = add_prefix(filename)
    return s3_obj.exists()

# example of storage class overwriting
# class DecS3BotoStorage(S3BotoStorage):
#     """
#     Rewriting url() method for default class S3BotoStorage
#     """
#     def url(self, name, headers=None, response_headers=None):
#         # Preserve the trailing slash after normalizing the path.
#         name = self._normalize_name(self._clean_name(name))
#         # return filepath_to_uri(name)
#         if self.custom_domain:
#             return "%s//%s/%s" % (self.url_protocol,
#                                   self.custom_domain, filepath_to_uri(name))
#         return self.connection.generate_url(
#             self.querystring_expire, method='GET', bucket=self.bucket.name,
#             key=self._encode_name(name), headers=headers,
#             query_auth=self.querystring_auth, force_http=not self.secure_urls,
#             response_headers=response_headers)


def save_image_to_s3(image, file_path, img_format, add_md5=True):
    """
    image from function is object image opened by PIL

    from PIL import Image
    temp_image = obj.image
    image = Image.open(temp_image)

    save_image_to_s3(image, ...)
    """
    image_buffer = BytesIO()
    image.save(image_buffer, img_format)
    image_buffer.seek(0)
    content = image_buffer.read()
    image_buffer.close()
    result = store_s3(file_path, content, add_md5=add_md5, extra_headers={'Cache-Control': getattr(settings, 'DEFAULT_CACHE_CONTROL', '')})
    return result

def init_s3_client(aws_access_key_id, aws_secret_access_key):
    return boto3.client('s3',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)
