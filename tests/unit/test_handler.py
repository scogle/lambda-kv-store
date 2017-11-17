
import unittest
import mock
import handler

class TestHandler(unittest.TestCase):

    @mock.patch('handler.aws_resource')
    def test_get_table(self, mock_rsrc):
        handler.get_table()
        mock_rsrc.assert_called_with('dynamodb')
        mock_rsrc.return_value.Table.assert_called_with('nike-test')

    @mock.patch('json.dumps')
    def test_form_http_response(self, mock_json):
        body = {"hello": "world"}
        handler.form_http_response(200, body)
        mock_json.assert_called_with(body, cls=handler.DecimalEncoder)

    @mock.patch('handler.form_http_response')
    def test_ping(self, mock_form_http_response):
        event = mock.Mock()
        context = mock.Mock()
        handler.ping(event, context)
        mock_form_http_response.assert_called_with(200, {"message": "PONG"})

    @mock.patch('handler.form_http_response')
    @mock.patch('handler.get_table')
    def test_get_all_keys(self, mock_get_table, mock_form_http_response):
        event = mock.Mock()
        context = mock.Mock()
        handler.get_all_keys(event, context)
        mock_get_table.assert_called_with()
        mock_get_table.return_value.scan.assert_called_with()
        mock_items = mock_get_table.return_value.scan.return_value['Items']
        mock_form_http_response.assert_called_with(200, mock_items)

    @mock.patch('handler.DynamoKey')
    @mock.patch('handler.form_http_response')
    @mock.patch('handler.get_table')
    def test_get_key(self, mock_get_table, mock_form_http_response, mock_key):
        event = mock.MagicMock()
        context = mock.Mock()
        mock_get_table.return_value.query.return_value = {'Items': [{'hello': 'world'}]}
        handler.get_key(event, context)
        mock_get_table.assert_called_with()
        mock_key.return_value.eq.assert_called_with(event['pathParameters']['key'])
        mock_get_table.return_value.query.assert_called_with(
            KeyConditionExpression=mock_key.return_value.eq.return_value
        )
        mock_form_http_response.assert_called_with(200, {'hello': 'world'})

        mock_get_table.return_value.query.return_value = {'Items': []}
        handler.get_key(event, context)
        mock_form_http_response.assert_called_with(404, {"error": "key not found"})

    @mock.patch('handler.form_http_response')
    @mock.patch('handler.get_table')
    def test_add_key(self, mock_get_table, mock_form_http_response):
        event = mock.MagicMock()
        context = mock.Mock()
        handler.add_key(event, context)
        mock_get_table.assert_called_with()
        mock_get_table.return_value.put_item.assert_called_with(
            Item={
                'key': event['pathParameters']['key'],
                'value': event.get.return_value.get.return_value
            }
        )
        mock_form_http_response.assert_called_with(200, {"message": "success"})

    @mock.patch('handler.form_http_response')
    @mock.patch('handler.get_table')
    def test_update_key(self, mock_get_table, mock_form_http_response):
        event = mock.MagicMock()
        context = mock.Mock()
        handler.update_key(event, context)
        mock_get_table.assert_called_with()
        mock_get_table.return_value.update_item.assert_called_with(
            Key={"key": event['pathParameters']['key']},
            AttributeUpdates={
                "value": {
                    'Value': event.get.return_value.get.return_value
                }
            }
        )
        mock_form_http_response.assert_called_with(200, {"message": "success"})

        event.get.return_value.get.return_value = None
        handler.update_key(event, context)
        mock_form_http_response.assert_called_with(400, {"error": "Missing required querystring parameter 'value'"})


    @mock.patch('handler.form_http_response')
    @mock.patch('handler.get_table')
    def test_delete_key(self, mock_get_table, mock_form_http_response):
        event = mock.MagicMock()
        context = mock.Mock()
        handler.delete_key(event, context)
        mock_get_table.assert_called_with()
        mock_get_table.return_value.delete_item.assert_called_with(
            Key={'key': event['pathParameters']['key']}
        )
        mock_form_http_response.assert_called_with(200, {"message": "success"})


if __name__ == '__main__':
    unittest.main()


