import datetime
import pprint
from google.cloud import storage

"""
basic operations on blobs
(objects) in a Google Cloud Storage bucket.
For more information, see the README.md under /storage  and the documentation
at https://cloud.google.com/storage/docs.
"""

def create_bucket(bucket_name):
    """Creates a new bucket."""
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created'.format(bucket.name))

def delete_bucket(bucket_name):
    """Deletes a bucket. The bucket must be empty."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()
    print('Bucket {} deleted'.format(bucket.name))

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))
    
    

def get_bucket_labels(bucket_name):
    """Prints out a bucket's labels."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    labels = bucket.labels
    pprint.pprint(labels)


def add_bucket_label(bucket_name):
    """Add a label to a bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    labels = bucket.labels
    labels['example'] = 'label'
    bucket.labels = labels
    bucket.patch()

    print('Updated labels on {}.'.format(bucket.name))
    pprint.pprint(bucket.labels)


def remove_bucket_label(bucket_name):
    """Remove a label from a bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    labels = bucket.labels

    if 'example' in labels:
        del labels['example']

    bucket.labels = labels
    bucket.patch()

    print('Updated labels on {}.'.format(bucket.name))
    pprint.pprint(bucket.labels)


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)


def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    """Lists all the blobs in the bucket that begin with the prefix.
    This can be used to list all blobs in a "folder", e.g. "public/".
    The delimiter argument can be used to restrict the results to only the
    "files" in the given "folder". Without the delimiter, the entire tree under
    the prefix is returned. For example, given these blobs:
        /a/1.txt
        /a/b/2.txt
    If you just specify prefix = '/a', you'll get back:
        /a/1.txt
        /a/b/2.txt
    However, if you specify prefix='/a' and delimiter='/', you'll get back:
        /a/1.txt
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)

    print('Blobs:')
    for blob in blobs:
        print(blob.name)

    if delimiter:
        print('Prefixes:')
        for prefix in blobs.prefixes:
            print(prefix)


# [START storage_upload_file]
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))
# [END storage_upload_file]


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))


def blob_metadata(bucket_name, blob_name):
    """Prints out a blob's metadata."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)

    print('Blob: {}'.format(blob.name))
    print('Bucket: {}'.format(blob.bucket.name))
    print('Storage class: {}'.format(blob.storage_class))
    print('ID: {}'.format(blob.id))
    print('Size: {} bytes'.format(blob.size))
    print('Updated: {}'.format(blob.updated))
    print('Generation: {}'.format(blob.generation))
    print('Metageneration: {}'.format(blob.metageneration))
    print('Etag: {}'.format(blob.etag))
    print('Owner: {}'.format(blob.owner))
    print('Component count: {}'.format(blob.component_count))
    print('Crc32c: {}'.format(blob.crc32c))
    print('md5_hash: {}'.format(blob.md5_hash))
    print('Cache-control: {}'.format(blob.cache_control))
    print('Content-type: {}'.format(blob.content_type))
    print('Content-disposition: {}'.format(blob.content_disposition))
    print('Content-encoding: {}'.format(blob.content_encoding))
    print('Content-language: {}'.format(blob.content_language))
    print('Metadata: {}'.format(blob.metadata))
    print("Temporary hold: ",
          'enabled' if blob.temporary_hold else 'disabled')
    print("Event based hold: ",
          'enabled' if blob.event_based_hold else 'disabled')
    if blob.retention_expiration_time:
        print("retentionExpirationTime: {}".format(blob.retention_expiration_time))
        
 if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('bucket_name', help='Your cloud storage bucket.')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('create-bucket', help=create_bucket.__doc__)
    subparsers.add_parser('delete-bucket', help=delete_bucket.__doc__)
    subparsers.add_parser('get-bucket-labels', help=get_bucket_labels.__doc__)
    subparsers.add_parser('add-bucket-label', help=add_bucket_label.__doc__)
    subparsers.add_parser(
        'remove-bucket-label', help=remove_bucket_label.__doc__)
    subparsers.add_parser('list', help=list_blobs.__doc__)

    list_with_prefix_parser = subparsers.add_parser(
        'list-with-prefix', help=list_blobs_with_prefix.__doc__)
    list_with_prefix_parser.add_argument('prefix')
    list_with_prefix_parser.add_argument('--delimiter', default=None)

    upload_parser = subparsers.add_parser('upload', help=upload_blob.__doc__)
    upload_parser.add_argument('source_file_name')
    upload_parser.add_argument('destination_blob_name')
