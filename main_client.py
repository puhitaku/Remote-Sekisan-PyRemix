import socket, requests, json, codecs, requests as req



def acquire(address):
	response = req.get(address).text.encode(src.encoding)
