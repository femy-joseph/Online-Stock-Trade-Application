import unittest
from http.client import HTTPConnection
import pickle

# import the MyHandler class from the main script

class TestMyHandler(unittest.TestCase):
    # TC1 - Create a mock GET request to retrieve stock data for a known stock
    def test_do_GET_POS(self):
        conn = HTTPConnection("localhost", 8001)
        conn.request("GET", "/Lookup_csv/GameStart")
        res = conn.getresponse()
        res_data = pickle.loads(res.read())
        print("Request sending is: GET /Lookup_csv/GameStart")
        print("res.status",res.status)
        print("result data",res_data)
        # Check that the response code is 200 and that the stock data is returned in the expected format
        self.assertEqual(res.status, 200)
        self.assertIsInstance(res_data, dict)
        self.assertIn("name", res_data)
        self.assertIn("price", res_data)
        self.assertIn("quantity", res_data)
        del res_data['max_trade']
        print("\n")

    # TC2 - Create a mock GET request to retrieve stock data for an unknown stock
    def test_do_GET_NEG(self):
        conn = HTTPConnection("localhost", 8001)
        conn.request("GET", "/Lookup_csv/Dominos")
        print("Request sending is: GET /Lookup_csv/Dominos")
        res = conn.getresponse()
        res_data = pickle.loads(res.read())
        self.assertEqual(res_data,'stock not found')
        print("res.status",res.status)
        print("result data",res_data)

        # Check that the response code is 404 when the stock is not found
        self.assertEqual(res.status, 404)


if __name__ == '__main__':
    unittest.main()
