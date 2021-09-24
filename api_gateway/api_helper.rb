require 'net/http'
require 'uri'
require 'json'
require './url_record'

module ApiControl
  include UrlRecord
  
  def url_parse
    target_url = UrlRecord::TARGET_URL
    uri = URI.parse(target_url)
    return uri
  end
  
  def request_action(uri, type, person_id=nil, name=nil)
    begin
      request = Net::HTTP::Post.new(uri)
    rescue
      puts "Invalid URI : #{uri}"
    end
    
    request_params = case type
      when 'SCAN'
        { "OperationType": type }
      when 'QUERY'
        { 
          "OperationType": type,
          "Keys": { "person_id": format("%03d", person_id) }
        }
      when 'PUT'
        {
          "OperationType": type,
          "Keys": {
            "person_id": format("%03d", person_id),
            "name": name.to_s
          }
        }
      else
        raise TypeError, "Invalid Operation Type : #{type}"
      end
      
      request.body = JSON.dump(request_params)
      req_options = { use_ssl: uri.scheme == "https" }
      
      response = Net::HTTP.start(uri.hostname, uri.port, req_options) do |http|
        http.request(request)
      end
      
      return response
  end
end