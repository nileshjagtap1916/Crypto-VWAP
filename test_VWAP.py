import unittest
from business.business import Business
import asyncio


class TestMethods(unittest.TestCase):

    def test_invalid_pair(self):
        loop = asyncio.get_event_loop()
        obj = Business(loop)

        message = {"product_id": "Dummy_product", "size": "2", "price": "1000"}

        output = loop.run_until_complete(obj.process_message(message))

        self.assertEqual(output, None)

    def test_invalid_price(self):
        loop = asyncio.get_event_loop()
        obj = Business(loop)

        message = {"product_id": "Dummy_product", "size": "2", "price": "abc"}
        output = loop.run_until_complete(obj.process_message(message))
        self.assertEqual(output, None)

    def test_invalid_size(self):
        loop = asyncio.get_event_loop()
        obj = Business(loop)

        message = {"product_id": "Dummy_product", "size": "xyz", "price": "10"}
        output = loop.run_until_complete(obj.process_message(message))
        self.assertEqual(output, None)

    def test_BTC_USD(self):
        loop = asyncio.get_event_loop()
        obj = Business(loop)

        message = {"product_id": "BTC-USD", "size": "2", "price": "1000"}
        output = loop.run_until_complete(obj.process_message(message))
        self.assertEqual(output, 1000.0)

        message = {"product_id": "BTC-USD", "size": "3", "price": "500"}
        output = loop.run_until_complete(obj.process_message(message))
        self.assertEqual(output, 700.0)

    def test_ETH_USD(self):
        loop = asyncio.get_event_loop()
        obj = Business(loop)

        message = {"product_id": "ETH-USD", "size": "2", "price": "1000"}
        output = loop.run_until_complete(obj.process_message(message))
        self.assertEqual(output, 1000.0)

        message = {"product_id": "ETH-USD", "size": "3", "price": "500"}
        output = loop.run_until_complete(obj.process_message(message))
        self.assertEqual(output, 700.0)

    def test_ETH_BTC(self):
        loop = asyncio.get_event_loop()
        obj = Business(loop)

        message = {"product_id": "ETH-BTC", "size": "2", "price": "1000"}
        output = loop.run_until_complete(obj.process_message(message))
        self.assertEqual(output, 1000.0)

        message = {"product_id": "ETH-BTC", "size": "3", "price": "500"}
        output = loop.run_until_complete(obj.process_message(message))
        self.assertEqual(output, 700.0)

    def test_pair_combination(self):
        loop = asyncio.get_event_loop()
        obj = Business(loop)

        message = {"product_id": "ETH-BTC", "size": "2", "price": "1000"}
        output = loop.run_until_complete(obj.process_message(message))
        self.assertEqual(output, 1000.0)

        message = {"product_id": "ETH-USD", "size": "2", "price": "1000"}
        output = loop.run_until_complete(obj.process_message(message))
        self.assertEqual(output, 1000.0)


if __name__ == '__main__':
    unittest.main()
