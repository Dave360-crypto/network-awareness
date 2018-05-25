
"""
------------------------------ START MINING -------------------------------
"""

"""
Bytes: download upload
"""
download_bytes = open("mining_download_bytes.txt", "r")
upload_bytes = open("mining_upload_bytes.txt", "r")

download_upload_bytes = open("mining_download_upload_bytes.dat", "w")

lines_download = download_bytes.readlines()
lines_upload = upload_bytes.readlines()

if len(lines_download) < len(lines_upload):
    size_bytes = len(lines_download)
else:
    size_bytes = len(lines_upload)

for i in range(0, size_bytes):
    download_upload_bytes.write(lines_download[i].rstrip() + " " + lines_upload[i].rstrip() + "\n")

"""
Ports: download upload
"""

download_ports = open("mining_download_ports.txt", "r")
upload_ports = open("mining_upload_ports.txt", "r")

download_upload_ports = open("mining_download_upload_ports.dat", "w")

lines_download = download_ports.readlines()
lines_upload = upload_ports.readlines()

if len(lines_download) < len(lines_upload):
    size_bytes = len(lines_download)
else:
    size_bytes = len(lines_upload)

for i in range(0, size_bytes):
    download_upload_ports.write(lines_download[i].rstrip() + " " + lines_upload[i].rstrip() + "\n")

"""
------------------------------ END MINING -------------------------------
"""

"""
------------------------------ START YOUTUBE -------------------------------
"""

"""
Bytes: download upload
"""
download_bytes = open("../data/youtube_download_bytes.txt", "r")
upload_bytes = open("../data/youtube_upload_bytes.txt", "r")

download_upload_bytes = open("../data/youtube_download_upload_bytes.dat", "w")

lines_download = download_bytes.readlines()
lines_upload = upload_bytes.readlines()

if len(lines_download) < len(lines_upload):
    size_bytes = len(lines_download)
else:
    size_bytes = len(lines_upload)

for i in range(0, size_bytes):
    download_upload_bytes.write(lines_download[i].rstrip() + " " + lines_upload[i].rstrip() + "\n")

"""
Ports: download upload
"""

download_ports = open("../data/youtube_download_ports.txt", "r")
upload_ports = open("../data/youtube_upload_ports.txt", "r")

download_upload_ports = open("youtube_download_upload_ports.dat", "w")

lines_download = download_ports.readlines()
lines_upload = upload_ports.readlines()

if len(lines_download) < len(lines_upload):
    size_bytes = len(lines_download)
else:
    size_bytes = len(lines_upload)

for i in range(0, size_bytes):
    download_upload_ports.write(lines_download[i].rstrip() + " " + lines_upload[i].rstrip() + "\n")

"""
------------------------------ END YOUTUBE -------------------------------
"""

"""
------------------------------ START BROWSING -------------------------------
"""

"""
Bytes: download upload
"""
download_bytes = open("../data/browsing_download_bytes.txt", "r")
upload_bytes = open("../data/browsing_upload_bytes.txt", "r")

download_upload_bytes = open("../data/browsing_download_upload_bytes.dat", "w")

lines_download = download_bytes.readlines()
lines_upload = upload_bytes.readlines()

if len(lines_download) < len(lines_upload):
    size_bytes = len(lines_download)
else:
    size_bytes = len(lines_upload)

for i in range(0, size_bytes):
    download_upload_bytes.write(lines_download[i].rstrip() + " " + lines_upload[i].rstrip() + "\n")

"""
Ports: download upload
"""

download_ports = open("../data/browsing_download_ports.txt", "r")
upload_ports = open("../data/browsing_upload_ports.txt", "r")

download_upload_ports = open("../data/browsig_download_upload_ports.dat", "w")

lines_download = download_ports.readlines()
lines_upload = upload_ports.readlines()

if len(lines_download) < len(lines_upload):
    size_bytes = len(lines_download)
else:
    size_bytes = len(lines_upload)

for i in range(0, size_bytes):
    download_upload_ports.write(lines_download[i].rstrip() + " " + lines_upload[i].rstrip() + "\n")

"""
------------------------------ END BROWSING -------------------------------
"""