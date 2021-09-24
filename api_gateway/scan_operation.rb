require 'net/http'
require 'uri'
require 'json'

target_url = 'https://8oplra75uf.execute-api.ap-northeast-1.amazonaws.com/demo'
uri = URI.parse(target_url)

request = Net::HTTP::Post.new(uri)
request.body = JSON.dump({
  "OperationType" => "SCAN"
})

req_options = {
  use_ssl: uri.scheme == "https",
}

response = Net::HTTP.start(uri.hostname, uri.port, req_options) do |http|
  http.request(request)
end

result = response.body.scan(/"person_id": "([0-9]{3})", "name": "([a-zA-Z0-9]*)"/)
ans = []
result.each do |r|
  ans << [r[0].to_i, r[1]]
end

print ans
