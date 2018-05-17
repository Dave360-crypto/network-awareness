import pyshark
import socket

capture = pyshark.LiveCapture(interface='en0', bpf_filter='tcp port 3355')


upload_counter = 0
upload_bytes = []
upload_ports = {}
upload_flags = []
download_counter = 0
download_bytes = []
download_ports = {}
download_flags = []
download_ports_counter = 0
upload_ports_counter = 0

#retirar da janela de dados tudo o que está a zeros para teste (ou seja, quando não há atividade não contar)

#guardar as flags SYN para saber as sessões tcp

#guardar os portos de origem e fazer um contagem dos portos


def print_callback(pkt):
    print('Just arrived:', pkt)
    source = pkt.ip.src

    if source == socket.gethostbyname(socket.gethostname()):
        global upload_counter, upload_bytes, upload_ports, upload_flags, upload_ports_counter
        upload_counter += 1
        upload_bytes.append(pkt.length)
        #contar os portos de origem
        if pkt.tcp.srcport in upload_ports:
            upload_ports[pkt.tcp.srcport] += 1
        else:
            upload_ports[pkt.tcp.srcport] = 1

        upload_flags.append(pkt.tcp.flags)

    else:
        global download_counter, download_bytes, download_ports, download_flags, download_ports_counte
        download_counter += 1
        download_bytes.append(pkt.length)
        #contar os portos de origem
        if pkt.tcp.srcport in download_ports:
            download_ports[pkt.tcp.srcport] += 1
        else:
            download_ports[pkt.tcp.srcport] = 1

        download_flags.append(pkt.tcp.flags)


    #save upload_bytes
    file_upload_bytes = open("upload_bytes.txt", "a")
    for item in upload_bytes:
        file_upload_bytes.write("%s\n" % item)

    file_upload_bytes.close()

    # save download_bytes
    file_download_bytes = open("download_bytes.txt", "a")
    for item in download_bytes:
        file_download_bytes.write("%s\n" % item)

    file_download_bytes.close()

    #save upload_ports
    file_upload_ports = open("upload_ports.txt", "a")
    for item, count in upload_ports.items():
        file_upload_ports.write("%s\n" % [item, count])

    file_upload_ports.close()

    # save download_ports
    file_download_ports = open("download_ports.txt", "a")
    for item, count in download_ports.items():
        file_download_ports.write("%s\n" % [item, count])

    file_download_ports.close()

    # save download_flags
    file_download_flags = open("download_flags.txt", "a")
    for item in download_flags:
        file_download_flags.write("%s\n" % item)

    file_download_flags.close()

    # save upload_flags
    file_upload_flags = open("upload_flags.txt", "a")
    for item in upload_flags:
        file_upload_flags.write("%s\n" % item)

    file_upload_flags.close()

    print("AQUIIIII")

capture.apply_on_packets(print_callback)
