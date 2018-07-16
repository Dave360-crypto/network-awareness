
**Cryptofinder** is a project developed in 2018, in an academic context. This project detects cripto-mining traffic through network monitoring. This software is supposed to be instaled in a side server, in which no ones needs to maintain.
This project contains a dashboard where the employees of a company may only check the probability of the traffic being or not crypto-mining traffic.
The malicious software can be in any local machine, including datacenters. Because it's supposed to be installed in a side server, there are no effects on the network.

**Company Deploy**
<p align="center">
  <img src="https://preview.ibb.co/gQTEMy/Captura_de_ecra_2018_07_16_a_s_16_26_31.png" border="0" /></a>
</p>

**PoC Solution**
<p align="center">
  <img src="https://preview.ibb.co/i31R1y/Captura_de_ecra_2018_07_16_a_s_16_27_18.png" border="0" /></a>
</p>

# Considered Datasets

* YouTube 
* Spotify
* Netflix
* Browsing
* Social Networking (Facebook, Instagram, Twitter, Pinterest, ...)
* Email
* VPN tunneling (Browsing)
* Variety of mining algorithms (Cryptonight, Keccak, Neoscrypt, ...)


# How to use

The current repository presents a variety of solutions, using a few different classifiers you can use.
In the academic context, the most beneficial result was the distance classifier, so you can run the live_capture.py, that will use the distance classifier,
but can be changed to others, that are also present in this repository.

Plus, the listen_and_process.py generates new datasets in case of need.


# Results
Using the distance classifier we obtained > 75% of detection and only 13% of false positives and 0% of false negatives.
