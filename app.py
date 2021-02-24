from flask import Flask,render_template,request
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


app = Flask(__name__)


@app.route('/upload')
def load_file():
    return render_template('index.html')

@app.route('/uploader',methods=['GET','POST'])
def upload_file():
    if request.method=='POST':
        f = request.files['file']
        # f.save(f.filename)
        # filenameA = 'hihi'
        try:
            print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")
            # Create a local directory to hold blob data
            local_path = "flasksta"
            connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
            # Create the BlobServiceClient object which will be used to create a container client
            blob_service_client = BlobServiceClient.from_connection_string(connect_str)

            # Create a unique name for the container
            container_name = "flasksta" ##azure blob storage 에서 사용되는 컨테이너 이름

            # Create the container
            # container_client = blob_service_client.create_container(container_name)
            # Create a file in the local data directory to upload and download
            local_file_name = f.filename
            upload_file_path = os.path.join(local_path, local_file_name)

            # Write text to the file
            file = open(upload_file_path, 'w')
            file.write("Hello, World!")
            file.close()

            # Create a blob client using the local file name as the name for the blob
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

            print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

            # Upload the created file
            with open(upload_file_path, "rb") as data:
                blob_client.upload_blob(data)

        except Exception as ex:
            print('Exception:')
            print(ex)
            return 'fail to upload'
        # f=request.files['file']
        # f.save(f.filename)
        # return 'file upload success'
        return 'file is uploaded'

@app.route('/')
def hello_world():
    # filenameA='hihi'
    return 'hey'


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=9900)
