require './api_helper'
include ApiControl

def query_operation(id)
  uri = url_parse
  response = request_action(uri, 'QUERY', id)
  result = response.body.scan(/"person_id": "([0-9]{3})", "name": "([a-zA-Z0-9]*)"/)
  
  print result.map { |result| [result[0].to_i, result[1]] }
  puts "\n"
end

query_operation(4)