require './api_helper'
include ApiControl

def scan_operation
  uri = url_parse
  response = request_action(uri, 'SCAN')
  results = response.body.scan(/"person_id": "([0-9]{3})", "name": "([a-zA-Z0-9]*)"/)
  
  print results.map { |result| [result[0].to_i, result[1]] }
  puts "\n"
end

scan_operation

