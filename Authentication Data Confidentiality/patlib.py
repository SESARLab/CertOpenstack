'''
@author: Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>
'''

import socket,paramiko,select,threading
try:
	import SocketServer
except ImportError:
	import socketserver as SocketServer

from keyczar import keyczar
from keyczar import readers
from keyczar import *

def verbose(msg=''):
	#print msg
	pass

class SSHClient(object):

	class PortForward(object):
		fwd = False
		class Handler(SocketServer.BaseRequestHandler):
			def handle(self):
				try:
					chan = self.ssh_transport.open_channel('direct-tcpip',
														   (self.chain_host, self.chain_port),
														   self.request.getpeername())
				except Exception as e:
					verbose('Incoming request to %s:%d failed: %s' %
							(
								self.chain_host, self.chain_port,	repr(e)
							)
						)
					return

				if chan is None:
					verbose('Incoming request to %s:%d was rejected by the SSH server.' %
							(
								self.chain_host, self.chain_port
							)
						)
					return

				while self.status == [True]:
					try:
						r, w, x = select.select([self.request, chan], [], [])
						if self.request in r:
							data = self.request.recv(1024)
							if len(data) == 0:
								break
							chan.send(data)
						if chan in r:
							data = chan.recv(1024)
							if len(data) == 0:
								break
							self.request.send(data)
					except Exception as e:
						verbose('Channel interrupted: %s' % (repr(e)))
						break

				peername = self.request.getpeername()
				chan.close()
				self.request.close()

		class Forwarder(SocketServer.ThreadingTCPServer):
			daemon_threads = True
			allow_reuse_address = True
			stopped = False
			def serve_until(self):
				while not self.stopped:
					self.handle_request()
			def stopNow(self):
				self.stopped = True

		def buildTunnel(self,local_port, remote_host,remote_port,transport):
			self.status = [True];
			self.local_port = local_port;
			class SSHPortForwardSubHandler (SSHClient.PortForward.Handler):
				chain_host = remote_host
				chain_port = remote_port
				ssh_transport = transport
				status = self.status

			self.fwd = SSHClient.PortForward.Forwarder(('localhost',local_port), SSHPortForwardSubHandler)
			self.fwd.serve_until();

		def destroyTunnel(self):
			try:
				if (self.status[0] == True):
					self.status[0] = False
				if self.local_port:
					closeAllSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					closeAllSocket.connect(("localhost", self.local_port))
					closeAllSocket.send('')
					self.local_port = False
			except:
				pass
			if hasattr(self.fwd,"stopNow"):
				self.fwd.stopNow()

	def __init__(self,hostname,username,keyfile,serverkeyfile,port=22):
		self.hostname = hostname
		self.ip = socket.gethostbyname(hostname)
		self.username = username
		self.keyfile = keyfile
		self.port = port
		self.connected = False
		self.client = paramiko.SSHClient()
		self.client.load_host_keys(serverkeyfile)
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


	def connect(self):
		self.client.connect(self.hostname, self.port, self.username, key_filename=self.keyfile)
		self.connected = True
		return self

	def forwardPort(self,localPortNo=8080,remotePortNo=8080,remotePortHost="localhost"):
		self.pf = self.PortForward()
		if (self.connected == False):
			raise Exception, "Not connected"

		self.fwd_thread = threading.Thread(target=self.pf.buildTunnel, args=(localPortNo, remotePortHost, remotePortNo, self.client.get_transport()))
		self.fwd_thread.start()
		return self

	def stopForwarding(self):
		t = self
		self = self.pf
		self.destroyTunnel()
		return t

	def executeCommand(self,command=""):
		if (self.connected == False):
			raise Exception, "Not connected"
		if (command==""):
			raise Exception, "No command"
		stdin,stdout,stderr = self.client.exec_command(command)
		out = stdout.readlines()
		output=""
		for line in out:
			if line != '':
				output=output+line
		return output

	def close(self):
		self.stopForwarding()
		self.client.close()



def convertChmodToBinary(chmod):
	chmod = str(chmod)
	a = [['0','0','0'],['0','0','0'],['0','0','0']]
	for i in range(0,3):
		digit = int(chmod[i])
		for j in range(0,3):
			a[i][j] = str(int(digit/pow(2,2-j)) % 2)
	return a





class DjangoDecryptor():
	class Crypter(object):
		@staticmethod
		def _read(meta,key):
			return DjangoDecryptor.ModifiedKeyczar(DjangoDecryptor.StringReader.CreateReader(meta,key))

		def __init__( self, meta,key):
			#try:
			self.crypt = self._read( meta, key)
			#except:
			#_init( meta, key)
			#self.crypt = self._read( meta, key )

		def encrypt( self, s):
			return self.crypt.Encrypt( s)

		def decrypt( self, s):
			return self.crypt.Decrypt( s)

	class StringReader(readers.Reader):
		def __init__(self,meta,key):
			self.meta = meta
			self.key  = key
		def GetMetadata(self):
			return self.meta
		def GetKey(self,ctx):
			return self.key
		def Close(self):
			return
		@classmethod
		def CreateReader(self,meta,key):
			return DjangoDecryptor.StringReader(meta,key)

	class ModifiedKeyczar(keyczar.Crypter):
		def ReadFromStrings(self,meta,key):
			return StringReader.CreateReader(meta,key)

	def decrypt(self,meta,key,crypted):
		crypter = DjangoDecryptor.Crypter(meta,key)
		plain = crypter.decrypt(crypted)
		return plain.decode('utf-8')

