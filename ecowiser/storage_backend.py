from django.core.files.storage import Storage
from b2sdk.v2 import B2Api, InMemoryAccountInfo,UploadSourceBytes
from pathlib import Path
from dotenv import load_dotenv

import os
import b2sdk.v1 as b2sdk

# Load environment variables from .env file
load_dotenv()

class FileWrapper:
    def __init__(self, file):
        self.file = file

    def read(self, size=-1):
        return self.file.read(size)

    def get_content_length(self):
        return self.file.size
    

class B2Storage(Storage):
    def __init__(self, bucket_name=None, application_key_id=None, application_key=None):
        self.bucket_name = bucket_name or os.getenv('B2_BUCKET_NAME')
        self.application_key_id = application_key_id or os.getenv('B2_APPLICATION_KEY_ID')
        self.application_key = application_key or os.getenv('B2_APPLICATION_KEY')
        self._b2_api = None

    @property
    def b2_api(self):
        if not self._b2_api:
            info = InMemoryAccountInfo()
            self._b2_api = B2Api(info)
            self._b2_api.authorize_account('production', self.application_key_id, self.application_key)
        return self._b2_api

    def _open(self, name, mode='rb'):
        file_info = self.b2_api.get_file_info_by_name(self.bucket_name, name)
        return file_info


    def _save(self, name, content):
        # Get the bucket name from environment variable
        bucket_name = os.getenv("B2_BUCKET_NAME")
        
        # Create an instance of B2Api
        b2_api = b2sdk.B2Api()
        
        # Authorize the B2Api object
        b2_api.authorize_account("production", os.getenv("B2_APPLICATION_KEY_ID"), os.getenv("B2_APPLICATION_KEY"))
        
        # Get the bucket object
        bucket = b2_api.get_bucket_by_name(bucket_name)
        
        # Get the content size
        content_size = content.size
        
        # Upload the content to B2
        try:
            uploaded_file = bucket.upload_bytes(
                data_bytes=content.read(),
                file_name=name,
                #file_size=content_size,
            )
            
            # Get the download URL for the uploaded file
            download_url = b2_api.get_download_url_for_fileid(uploaded_file.id_)            
            # Return the download URL as the saved name
            return download_url
        except Exception as e:
            # Handle the exception here
            raise

    
    def delete(self, name):
        bucket = self.b2_api.get_bucket_by_name(self.bucket_name)
        bucket.delete_files_by_name(name)

    def exists(self, name):
        bucket = self.b2_api.get_bucket_by_name(self.bucket_name)
        file_versions = bucket.ls(name)
        return any(file_versions)
            
    def deconstruct(self):
        # Implement the deconstruct method for custom serialization
        # Return a tuple of the form (class_path, args, kwargs)
        # that allows Django to serialize and deserialize the object

        # Replace 'path.to.B2Storage' with the actual import path of the B2Storage class
        class_path = 'ecowiser.storage_backend.B2Storage'

        # Return the tuple with any required arguments or keyword arguments
        # For example, if your B2Storage class takes any arguments in the constructor,
        # you can include them in the args or kwargs tuple accordingly
        args = ()
        kwargs = {}

        return class_path, args, kwargs