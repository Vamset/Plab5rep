import socket

HOST = '127.0.0.1'
PORT = 65432

def handle_request(request):
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, World!"
    return response.encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        data = conn.recv(1024)
        if data:
            request = data.decode()
            print("Received request:")
            print(request)

            response = handle_request(request)
            conn.sendall(response)
