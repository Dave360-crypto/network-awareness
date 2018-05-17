
"""
Bytes: download upload
"""
download_bytes = open("download_bytes.txt", "r")
upload_bytes = open("upload_bytes.txt", "r")

download_upload_bytes = open("download_upload_bytes.dat", "w")

lines_download = download_bytes.readlines()
lines_upload = upload_bytes.readlines()

if len(lines_download) < len(lines_upload):
    size_bytes = len(lines_download)
else:
    size_bytes = len(lines_upload)

for i in range(0, size_bytes):
    download_upload_bytes.write(lines_download[i].rstrip() + " " + lines_upload[i].rstrip() + "\n")

"""
Flags: download upload
"""

download_flags = open("download_flags.txt", "r")
upload_flags = open("upload_flags.txt", "r")

download_upload_flags = open("download_upload_flags.dat", "w")

lines_download = download_flags.readlines()
lines_upload = upload_flags.readlines()

if len(lines_download) < len(lines_upload):
    size_bytes = len(lines_download)
else:
    size_bytes = len(lines_upload)

for i in range(0, size_bytes):
    download_upload_flags.write(lines_download[i].rstrip() + " " + lines_upload[i].rstrip() + "\n")

"""
Ports: download upload
"""

download_ports = open("download_ports.txt", "r")
upload_ports = open("upload_ports.txt", "r")

download_upload_ports = open("download_upload_ports.dat", "w")

lines_download = download_ports.readlines()
lines_upload = upload_ports.readlines()

if len(lines_download) < len(lines_upload):
    size_bytes = len(lines_download)
else:
    size_bytes = len(lines_upload)

for i in range(0, size_bytes):
    download_upload_ports.write(lines_download[i].rstrip() + " " + lines_upload[i].rstrip() + "\n")