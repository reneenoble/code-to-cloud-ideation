from flask import Flask, render_template, request
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import os

invite_app = Flask('app')

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
# Create a unique name for the container
container_name = "reneemydata"
# Create the container
# container_client = blob_service_client.create_container(container_name)


local_path = "./data"
# os.mkdir(local_path)

# Create a file in the local data directory to upload and download
local_file_name = "test.txt"
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




@invite_app.route('/')
def input_info():
  return render_template('form.html')

@invite_app.route('/view', methods=('GET', 'POST'))
def view_invite():
  date = request.form['date']
  time = request.form['time']
  date = datetime(*[int(i) for i in date.split("-")] + [int(i) for i in time.split(":")])
  d = date.strftime("%A %B %-d, %Y")
  t = date.strftime("%-I:%S %p")
  # print(datetime(*date))

  return render_template('invite-basic.html', event=request.form['event'], to=request.form['to'], date=d, time=t, sender=request.form['sender'])





if __name__ == '__main__':
    invite_app.run(debug=True, use_reloader=True, host='0.0.0.0', port=8080)