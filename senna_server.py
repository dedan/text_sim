
import subprocess as sp
import os
import sys
import Pyro4

senna_path = '/Users/dedan/Downloads/senna/'
executable = 'senna_new'


class SennaServer(object):
    """ keep SENNA always in memory

        The SENNA executable is quite big and it made my program very slow
        to always load it into memory when I wanted to tag a sentence. This
        can be avoided by this senna server. Start the server and then easily
        acces it throuh pyro. Here a short example of how to access the server

        import Pyro4
        senna_server = Pyro4.Proxy("PYRONAME:servers.senna")
        print senna_server.tag('I have a head')
    """

    def __init__(self, senna_path, executable):
        """Spawn the background process (SENNA)"""
        self.senna_path = senna_path
        self.p = sp.Popen(['blabla', '-path', senna_path],
                            executable=os.path.join(senna_path, executable),
                            stdin=sp.PIPE,
                            stdout=sp.PIPE)

    def tag(self, sentence):
        """tag one sentence"""
        res = ''
        self.p.stdin.write(sentence+'\n')
        for i in range(len(sentence.split())):
            res += self.p.stdout.readline()
        return res

senna_server = SennaServer(senna_path, executable)


try:
    # start nameserver in background
    p = sp.Popen([sys.executable, '-m', 'Pyro4.naming'],
                  stdout=sp.PIPE, stderr=sp.STDOUT)
    daemon = Pyro4.Daemon()                   # make a Pyro daemon
    ns = Pyro4.locateNS()                     # find the name server
    uri = daemon.register(senna_server)       # register as a Pyro object
    ns.register("servers.senna", uri)         # register with nameserver

    print "Funky Senna Server is running"
    daemon.requestLoop()

except Exception, e:
    raise e
finally:
    # kill nameserver
    p.terminate()
