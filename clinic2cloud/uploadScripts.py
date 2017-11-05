""" Classes for uploading to the various cloud services for processing.

Copyright 2017 The Clinic2Cloud Team
Licence: BSD 2-Clause
"""

from google.cloud import storage as gstorage

class uploadBase:
    """ Base class for uploads. """

    def __init__(self, uid):
        self.uid = uid
    
    def upload(self, uploadFilename, processingOptions):
        """ Create a new bucket and upload blobs for the file and options.

        @param uploadFilename       MINC file to be uploaded.
        @param processingOptions    String with processing options.
        """
        pass

    def isDone(self):
        """ Poll the status of the submitted job. """
        pass

    def download(self, downloadFilename):
        pass

class uploadGoogle(uploadBase):
    """ Upload to a google cloud instance. """

    def __init__(self, uid):
        uploadBase.__init__(self, uid)

        self.storage_client = None
        self.bucket = None

    def upload(self, uploadFilename, processingOptions):
        uploadBase.upload(self, uploadFilename, processingOptions)

        self.storage_client = gstorage.Client.from_service_account_json(
            '/src/HealthHack/clinic2cloud-ce7ac00ac070.json')

        # Create a new bucket with the uid
        self.bucket = self.storage_client.create_bucket(self.uid)

        # Upload the file to be processed
        blobInput = self.bucket.blob('inputFile.mnc')
        blobInput.upload_from_filename(uploadFilename)

        # Upload the processing options into a string
        blobOpts = self.bucket.blob('options.dat')
        blobOpts.upload_from_string(processingOptions)

    def isDone(self):
        """ Poll the status of the submitted job. """
        uploadBase.isDone(self)

        blobDone = self.bucket.blob('done')
        return blobDone.exists()

    def download(self, downloadFilename):
        uploadBase.download(self, downloadFilename)

        # Download output
        blobOutput = self.bucket.blob('output.tar')
        blobOutput.download_to_filename(downloadFilename)

        # Cleanup resources
        self.bucket.delete(force=True)

class uploadAws(uploadBase):
    """ Upload to a AWS instance. """

    def __init__(self, uid):
        uploadBase.__init__(self, uid)

    def upload(self, uploadFilename, processingOptions):
        uploadBase.upload(self, uploadFilename, processingOptions)
        # TODO

    def isDone(self):
        """ Poll the status of the submitted job. """
        uploadBase.isDone(self)
        # TODO

    def download(self, downloadFilename):
        uploadBase.download(self, downloadFilename)
        # TODO

class uploadNectar(uploadBase):
    """ Upload to a Nectar Cloud instance. """

    def __init__(self, uid):
        uploadBase.__init__(self, uid)

    def upload(self, uploadFilename, processingOptions):
        uploadBase.upload(self, uploadFilename, processingOptions)
        # TODO

    def isDone(self):
        """ Poll the status of the submitted job. """
        uploadBase.isDone(self)
        # TODO

    def download(self, downloadFilename):
        uploadBase.download(self, downloadFilename)
        # TODO

def get_class(name):
    """ Get a class from a string name. """

    if name in ['google']: return uploadGoogle
    if name in ['aws']: return uploadAws
    if name in ['nectar']: return uploadNectar

    raise Exception('Unknown class name: {}'.format(name))

