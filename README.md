# Lambda KV Store

[![Build Status](https://travis-ci.org/scogle/lambda-kv-store.svg?branch=master)](https://travis-ci.org/scogle/lambda-kv-store)

A simple KV store written in Python 3.6 using AWS Lambda and DynamoDB

### Endpoints
 - `GET` - https://3ytleagu47.execute-api.us-east-1.amazonaws.com/dev/ping
 - `GET` - https://3ytleagu47.execute-api.us-east-1.amazonaws.com/dev/v1/keys
 - `GET` - https://3ytleagu47.execute-api.us-east-1.amazonaws.com/dev/v1/keys/{key}
 - `POST` - https://3ytleagu47.execute-api.us-east-1.amazonaws.com/dev/v1/keys/{key}?value={value}
 - `PUT` - https://3ytleagu47.execute-api.us-east-1.amazonaws.com/dev/v1/keys/{key}?value={value}
 - `DELETE` - https://3ytleagu47.execute-api.us-east-1.amazonaws.com/dev/v1/keys/{key}

### Functions
 - `ping`: `nike-test-dev-ping`
 - `get_all_keys`: `nike-test-dev-get_all_keys`
 - `get_key`: `nike-test-dev-get_key`
 - `add_key`: `nike-test-dev-add_key`
 - `update_key`: `nike-test-dev-update_key`
 - `delete_key`: `nike-test-dev-delete_key`

https://platform.serverless.com/services/scogle/nike-test