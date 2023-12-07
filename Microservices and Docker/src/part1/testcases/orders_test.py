import unittest
from http.client import HTTPConnection
import pickle,json

# import the MyHandler class from the main script
host='localhost'
port=8080
class TestMyHandler(unittest.TestCase):
    # TC1 - Create a mock POST request to buy a valid stock
    def test_do_POST_buy_POS(self):
        conn = HTTPConnection(host, port)
        request_body=json.dumps({
        "name": 'GameStart',
        "quantity": 5,
        "type": "buy"
    })
        http_req = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"
        print("request sent is:",http_req)
        http_req=http_req.split("\r\n")
        content_type=http_req[2]
        body=json.loads(http_req[5])
        contenttype=content_type.split(':')
        content={}
        content[contenttype[0]]=contenttype[1]
        body=json.dumps(body)
        conn.request('POST','/trade_stocks',body,content)
        res = conn.getresponse()
        res_data = pickle.loads(res.read())
        print(res_data)
        print("\n")

        # Check that the response code is 200 and that the stock data is returned in the expected format
        self.assertEqual(res.status, 200)
        self.assertIsInstance(res_data, dict)
        self.assertIn("transaction_number", res_data)

      # TC2 - Create a mock POST request to sell a valid stock
    def test_do_POST_sell_POS(self):
        conn = HTTPConnection(host, port)
        request_body=json.dumps({
        "name": 'FishCo',
        "quantity": 5,
        "type": "sell"
    })
        http_req = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"
        print("request sent is:",http_req)
        http_req=http_req.split("\r\n")
        content_type=http_req[2]
        body=json.loads(http_req[5])
        contenttype=content_type.split(':')
        content={}
        content[contenttype[0]]=contenttype[1]
        body=json.dumps(body)
        conn.request('POST','/trade_stocks',body,content)
        res = conn.getresponse()
        res_data = pickle.loads(res.read())
        print(res_data)
        print("\n")

        # Check that the response code is 200 and that the stock data is returned in the expected format
        self.assertEqual(res.status, 200)
        self.assertIsInstance(res_data, dict)
        self.assertIn("transaction_number", res_data)

        
      # TC3 - Create a mock POST request to buy a stock that is not present
    def test_do_POST_buy_NEG(self):
        conn = HTTPConnection(host, port)
        request_body=json.dumps({
        "name": 'Dominos',
        "quantity": 5,
        "type": "buy"
    })
        http_req = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"
        print("request sent is:",http_req)
        http_req=http_req.split("\r\n")
        content_type=http_req[2]
        body=json.loads(http_req[5])
        contenttype=content_type.split(':')
        content={}
        content[contenttype[0]]=contenttype[1]
        body=json.dumps(body)
        conn.request('POST','/trade_stocks',body,content)
        res = conn.getresponse()
        res_data = pickle.loads(res.read())
        print(res_data)
        print("\n")

        # Check that the response code is 404 and that the stock data is returned in the expected format
        self.assertEqual(res.status, 404)
        self.assertEqual(res_data,'stock not found')

    
      # TC4 - Create a mock POST request to sell a stock that is not present
    def test_do_POST_sell_NEG(self):
        conn = HTTPConnection(host, port)
        request_body=json.dumps({
        "name": 'StartBucks',
        "quantity": 5,
        "type": "sell"
    })
        http_req = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"
        print("request sent is:",http_req)
        http_req=http_req.split("\r\n")
        content_type=http_req[2]
        body=json.loads(http_req[5])
        contenttype=content_type.split(':')
        content={}
        content[contenttype[0]]=contenttype[1]
        body=json.dumps(body)
        conn.request('POST','/trade_stocks',body,content)
        res = conn.getresponse()
        res_data = pickle.loads(res.read())
        print(res_data)
        print("\n")

        # Check that the response code is 404 and that the stock data is returned in the expected format
        self.assertEqual(res.status, 404)
        self.assertEqual(res_data,'stock not found')

    
      # TC5 - Create a mock POST request to buy a stock that exceeds the trading volume 
    def test_do_POST_buy_NEG_max(self):
        conn = HTTPConnection(host, port)
        request_body=json.dumps({
        "name": 'GameStart',
        "quantity": 5000,
        "type": "buy"
    })
        http_req = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"
        print("request sent is:",http_req)
        http_req=http_req.split("\r\n")
        content_type=http_req[2]
        body=json.loads(http_req[5])
        contenttype=content_type.split(':')
        content={}
        content[contenttype[0]]=contenttype[1]
        body=json.dumps(body)
        conn.request('POST','/trade_stocks',body,content)
        res = conn.getresponse()
        res_data = pickle.loads(res.read())
        print(res_data)
        print("\n")

        # Check that the response code is 422 and that the stock data is returned in the expected format
        self.assertEqual(res.status, 422)
        self.assertEqual(res_data,'max trading volume exceeded')

    
      # TC6 - Create a mock POST request to sell a stock that exceeds the trading volume
    def test_do_POST_sell_NEG_max(self):
        conn = HTTPConnection(host, port)
        request_body=json.dumps({
        "name": 'MenhirCo',
        "quantity": 5000,
        "type": "sell"
    })
        http_req = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"
        print("request sent is:",http_req)
        http_req=http_req.split("\r\n")
        content_type=http_req[2]
        body=json.loads(http_req[5])
        contenttype=content_type.split(':')
        content={}
        content[contenttype[0]]=contenttype[1]
        body=json.dumps(body)
        conn.request('POST','/trade_stocks',body,content)
        res = conn.getresponse()
        res_data = pickle.loads(res.read())
        print(res_data)

        # Check that the response code is 422 and that the stock data is returned in the expected format
        self.assertEqual(res.status, 422)
        self.assertEqual(res_data,'max trading volume exceeded')
if __name__ == '__main__':
    unittest.main()
