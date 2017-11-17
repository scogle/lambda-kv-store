
import unittest
import mock
import requests

BASE_URL = "https://3ytleagu47.execute-api.us-east-1.amazonaws.com/dev"

class TestAPIRoutes(unittest.TestCase):

    def test_ping(self):
        req = requests.get("{url}/ping".format(url=BASE_URL))
        res = req.json()
        self.assertEqual(res, {"message": "PONG"})

    def test_get_keys(self):
        req = requests.get("{url}/v1/keys".format(url=BASE_URL))
        res = req.json()
        self.assertTrue(req.ok)
        self.assertGreater(len(res), 0)
        for item in res:
            self.assertTrue('key' in item and 'value' in item)

    def test_get_key(self):
        # Arbitraririly grab the last key
        key = [item['key'] for item in requests.get("{}/v1/keys".format(BASE_URL)).json()][-1]
        req = requests.get("{url}/v1/keys/{key}".format(url=BASE_URL, key=key))
        res = req.json()
        self.assertTrue(req.ok)
        self.assertTrue('key' in res and 'value' in res)

    def test_add_key(self):
        key = "dog_test_key"
        value = "woof"
        req = requests.post(
            "{url}/v1/keys/{key}".format(url=BASE_URL, key=key),
            params={"value": value}
        )
        res = req.json()
        self.assertTrue(req.ok)
        self.assertEqual(res, {"message": "success"})

        item = requests.get("{url}/v1/keys/{key}".format(url=BASE_URL, key=key)).json()
        self.assertEqual(item, {"key": key, "value": value})

    def test_update_key(self):
        key = "dog_test_key"
        value = "bark"
        req = requests.put(
            "{url}/v1/keys/{key}".format(url=BASE_URL, key=key),
            params={"value": value}
        )
        res = req.json()
        self.assertTrue(req.ok)
        self.assertEqual(res, {"message": "success"})

        item = requests.get("{url}/v1/keys/{key}".format(url=BASE_URL, key=key)).json()
        self.assertEqual(item, {"key": key, "value": value})

    def test_delete_key(self):
        key = 'cat_test_key'

        req = requests.delete(
            "{url}/v1/keys/cat_test_key".format(url=BASE_URL)
        )
        res = req.json()
        self.assertTrue(req.ok)
        self.assertEqual(res, {"message": "success"})



if __name__ == '__main__':
    # Add a key/value so we can be sure there's at least one for testing
    requests.post(
        "{url}/v1/keys/cat_test_key".format(url=BASE_URL),
        params={"value": "meow"}
    )

    unittest.main()

    # Clean up
    requests.delete(
        "{url}/v1/keys/cat_test_key".format(url=BASE_URL)
    )
