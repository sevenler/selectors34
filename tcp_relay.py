import selectors34 as selectors
import socket

response = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
response += b'Hello, world!\r\n'


def run():
    sel = selectors.DefaultSelector()

    def accept(sock, mask):
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, read)

    def read(conn, mask):
        data = conn.recv(1024)  # Should be ready
        if data:
            print('echoing', repr(data), 'to', conn)
            conn.send(response)  # Hope it won't block
        else:
            print('closing', conn)
            sel.unregister(conn)
            conn.close()

    sock = socket.socket()
    sock.bind(('localhost', 1235))
    sock.listen(100)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

if __name__ == '__main__':
    run()
