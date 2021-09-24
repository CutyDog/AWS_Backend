require './api_helper'
include ApiControl

def put_operation(id, name)
  uri = url_parse
  response = request_action(uri, 'PUT', id, name)
  if response.body.scan(/"HTTPStatusCode": ([0-9]*),/)[0][0].to_i == 200
    puts 'Successed!!'
  else
    puts 'Failed...'
  end
end

put_operation(10, 'yamada')