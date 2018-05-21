import pyshark
import socket
import datetime

capture = pyshark.LiveCapture(interface='en0', bpf_filter='tcp port 3355')

upload_counter = 0
upload_bytes = []
upload_bytes_counter = 0
download_bytes_counter = 0
upload_ports = {}
download_counter = 0
download_bytes = []
download_ports = {}
download_ports_counter = 0
upload_ports_counter = 0
packets = {}

#retirar da janela de dados tudo o que está a zeros para teste (ou seja, quando não há atividade não contar)

#guardar os portos de origem e fazer um contagem dos portos
index = 0


def print_callback(pkt):
    global index
    packets[index] = pkt
    index += 1

try:
    capture.apply_on_packets(print_callback)
except KeyboardInterrupt:
    last_timestamp = 0

    for index, pkt in packets.items():
        source = pkt.ip.src
        if index==0:
            if source == socket.gethostbyname(socket.gethostname()):
                upload_counter += 1
                upload_bytes_counter += int(pkt.length)
                # contar os portos de origem
                if pkt.tcp.srcport in upload_ports:
                    upload_ports[pkt.tcp.srcport] += 1
                else:
                    upload_ports[pkt.tcp.srcport] = 1

            else:
                download_counter += 1
                download_bytes_counter += int(pkt.length)
                # contar os portos de origem
                if pkt.tcp.srcport in download_ports:
                    download_ports[pkt.tcp.srcport] += 1
                else:
                    download_ports[pkt.tcp.srcport] = 1

            last_timestamp = packets[index].sniff_time
            continue

        timestamp_now = packets[index].sniff_time
        timestamp_now = timestamp_now.replace(tzinfo=datetime.timezone.utc).timestamp()

        delta_time = ((datetime.datetime.utcfromtimestamp(int(timestamp_now))) - last_timestamp).total_seconds()
        #print("AQUIII", delta_time)

        if delta_time >= 1: # if passed more than one second, means we have to write n 0
            #print("AQUIII", delta_time)
            upload_bytes.append(upload_bytes_counter)
            download_bytes.append(download_bytes_counter)

            for i in range(0, int(delta_time)-1):
                upload_bytes.append(0)
                download_bytes.append(0)

            upload_bytes_counter = 0
            download_bytes_counter = 0
        elif int(last_timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()) == int(timestamp_now): # if it's the same timestamp, we have to increment
            source = pkt.ip.src

            if source == socket.gethostbyname(socket.gethostname()):
                upload_counter += 1
                upload_bytes_counter += int(pkt.length)
                # contar os portos de origem
                if pkt.tcp.srcport in upload_ports:
                    upload_ports[pkt.tcp.srcport] += 1
                else:
                    upload_ports[pkt.tcp.srcport] = 1

            else:
                download_counter += 1
                download_bytes_counter += int(pkt.length)
                # contar os portos de origem
                if pkt.tcp.srcport in download_ports:
                    download_ports[pkt.tcp.srcport] += 1
                else:
                    download_ports[pkt.tcp.srcport] = 1

        last_timestamp = packets[index].sniff_time

    # save upload_bytes
    file_upload_bytes = open("mining_upload_bytes.txt", "a")
    for item in upload_bytes:
        file_upload_bytes.write("%s\n" % item)

    file_upload_bytes.close()

    # save download_bytes
    file_download_bytes = open("mining_download_bytes.txt", "a")
    for item in download_bytes:
        file_download_bytes.write("%s\n" % item)

    file_download_bytes.close()

    # save upload_ports
    file_upload_ports = open("mining_upload_ports.txt", "a")
    for item, count in upload_ports.items():
        file_upload_ports.write("%s\n" % [item, count])

    file_upload_ports.close()

    # save download_ports
    file_download_ports = open("mining_download_ports.txt", "a")
    for item, count in download_ports.items():
        file_download_ports.write("%s\n" % [item, count])

    file_download_ports.close()



