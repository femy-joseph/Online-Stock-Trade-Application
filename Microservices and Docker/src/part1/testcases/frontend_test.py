import socket
import json
import time
import random
import unittest

class TestMyHandler(unittest.TestCase):
    '''
    #TC1 to lookup for a valid stockname
    def test_lookup(self):
        s = socket.socket()
        host='localhost'
        port = 12345  # Specify the port to connect to
        s.connect((host, port))

        type_of_request='lookup'
        stock_name='FishCo'
        http_request = "GET /stocks/%s / HTTP/1.1\r\nHost:%s\r\n\r\n" %(stock_name,host)
        print("Type of request sending: ",type_of_request)
        print(http_request)
        s.send(http_request.encode())
        response = s.recv(1024)
        header_end = response.find(b'\r\n\r\n')
        header = response[:header_end].decode()
        body = response[header_end+4:]
        res_data = json.loads(body.decode('utf-8'))
        print(res_data)
        print("\n")
        self.assertIsInstance(res_data, dict)
        self.assertIn("data", res_data)
        s.close()
        
    def test_lookup_invalid(self):
        s = socket.socket()
        host='localhost'
        port = 12345  # Specify the port to connect to
        s.connect((host, port))

        type_of_request='lookup'
        stock_name='Dominos'
        http_request = "GET /stocks/%s / HTTP/1.1\r\nHost:%s\r\n\r\n" %(stock_name,host)
        print("Type of request sending: ",type_of_request)
        print(http_request)
        s.send(http_request.encode())
        response = s.recv(1024)
        header_end = response.find(b'\r\n\r\n')
        header = response[:header_end].decode()
        body = response[header_end+4:]
        res_data = json.loads(body.decode('utf-8'))
        print(res_data)
        print("\n")
        self.assertIsInstance(res_data, dict)
        self.assertIn("error", res_data)
        s.close()
        
    def test_buy_valid(self):
        s = socket.socket()
        host='localhost'
        port = 12345  # Specify the port to connect to
        s.connect((host, port))

        type_of_request='trade'
        stock_name='FishCo'
        quantity=5
        trade_type='buy'
        request_body=json.dumps({
            "name": stock_name,
            "quantity": quantity,
            "type": trade_type
        })
        http_request = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"

        print("Type of request sending: ",type_of_request)
        print(http_request)
        s.send(http_request.encode())
        response = s.recv(1024)
        header_end = response.find(b'\r\n\r\n')
        header = response[:header_end].decode()
        body = response[header_end+4:]
        res_data = json.loads(body.decode('utf-8'))
        print(res_data)
        print("\n")
        self.assertIsInstance(res_data, dict)
        self.assertIn("data", res_data)
        s.close()
        

    def test_sell_valid(self):
        s = socket.socket()
        host='localhost'
        port = 12345  # Specify the port to connect to
        s.connect((host, port))

        type_of_request='trade'
        stock_name='MenhirCo'
        quantity=5
        trade_type='sell'
        request_body=json.dumps({
            "name": stock_name,
            "quantity": quantity,
            "type": trade_type
        })
        http_request = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"

        print("Type of request sending: ",type_of_request)
        print(http_request)
        s.send(http_request.encode())
        response = s.recv(1024)
        header_end = response.find(b'\r\n\r\n')
        header = response[:header_end].decode()
        body = response[header_end+4:]
        res_data = json.loads(body.decode('utf-8'))
        print(res_data)
        print("\n")
        self.assertIsInstance(res_data, dict)
        self.assertIn("data", res_data)
        s.close()
        
    def test_buy_invalid(self):
        s = socket.socket()
        host='localhost'
        port = 12345  # Specify the port to connect to
        s.connect((host, port))

        type_of_request='trade'
        stock_name='Startbucks'
        quantity=5
        trade_type='buy'
        request_body=json.dumps({
            "name": stock_name,
            "quantity": quantity,
            "type": trade_type
        })
        http_request = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"

        print("Type of request sending: ",type_of_request)
        print(http_request)
        s.send(http_request.encode())
        response = s.recv(1024)
        header_end = response.find(b'\r\n\r\n')
        header = response[:header_end].decode()
        body = response[header_end+4:]
        res_data = json.loads(body.decode('utf-8'))
        print(res_data)
        print("\n")
        self.assertIsInstance(res_data, dict)
        self.assertIn("error", res_data)
        s.close()
        
    def test_sell_invalid(self):
        s = socket.socket()
        host='localhost'
        port = 12345  # Specify the port to connect to
        s.connect((host, port))

        type_of_request='trade'
        stock_name='Dominos'
        quantity=5
        trade_type='sell'
        request_body=json.dumps({
            "name": stock_name,
            "quantity": quantity,
            "type": trade_type
        })
        http_request = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"

        print("Type of request sending: ",type_of_request)
        print(http_request)
        s.send(http_request.encode())
        response = s.recv(1024)
        header_end = response.find(b'\r\n\r\n')
        header = response[:header_end].decode()
        body = response[header_end+4:]
        res_data = json.loads(body.decode('utf-8'))
        print(res_data)
        print("\n")
        self.assertIsInstance(res_data, dict)
        self.assertIn("error", res_data)
        s.close()
        
    def test_buy_highstocks(self):
        s = socket.socket()
        host='localhost'
        port = 12345  # Specify the port to connect to
        s.connect((host, port))

        type_of_request='trade'
        stock_name='FishCo'
        quantity=500
        trade_type='buy'
        request_body=json.dumps({
            "name": stock_name,
            "quantity": quantity,
            "type": trade_type
        })
        http_request = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"

        print("Type of request sending: ",type_of_request)
        print(http_request)
        s.send(http_request.encode())
        response = s.recv(1024)
        header_end = response.find(b'\r\n\r\n')
        header = response[:header_end].decode()
        body = response[header_end+4:]
        res_data = json.loads(body.decode('utf-8'))
        print(res_data)
        print("\n")
        self.assertIsInstance(res_data, dict)
        self.assertIn("error", res_data)
        s.close()
        '''
    def test_sell_highstocks(self):
        s = socket.socket()
        host='localhost'
        port = 12345  # Specify the port to connect to
        s.connect((host, port))

        type_of_request='trade'
        stock_name='FishCo'
        quantity=500
        trade_type='sell'
        request_body=json.dumps({
            "name": stock_name,
            "quantity": quantity,
            "type": trade_type
        })
        http_request = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"

        print("Type of request sending: ",type_of_request)
        print(http_request)
        s.send(http_request.encode())
        response = s.recv(1024)
        header_end = response.find(b'\r\n\r\n')
        header = response[:header_end].decode()
        body = response[header_end+4:]
        res_data = json.loads(body.decode('utf-8'))
        print(res_data)
        print("\n")
        self.assertIsInstance(res_data, dict)
        self.assertIn("error", res_data)
        s.close()
        

if __name__ == '__main__':
    unittest.main()


