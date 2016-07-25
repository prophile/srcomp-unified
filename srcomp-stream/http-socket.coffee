http = require 'http'

server = (comp) ->
  svr = http.createServer (request, response) ->
    valid = true
    valid = false if request.url isnt '/'

    if not valid
      response.writeHead 404, 'Not Found', 'Content-Type': 'text/plain'
      response.end "Not a thing.\n", 'utf-8'
      return

    allowHeaders = {
      'Content-Type': 'text/plain',
      'Allow': 'GET, HEAD, OPTIONS',
      'Access-Control-Allow-Origin': '*'
    }
    mainHeaders = {
      'Content-Type': 'text/event-stream',
      'Access-Control-Allow-Origin': '*'
    }

    if request.method is 'OPTIONS'
      response.writeHead 200, 'OK', allowHeaders
      response.end '', 'utf-8'
      return

    if request.method is 'HEAD'
      response.writeHead 200, 'OK', mainHeaders
      response.end '', 'utf-8'
      return

    if request.method isnt 'GET'
      response.writeHead 405, 'Method Not Allowed', allowHeaders
      response.end '', 'utf-8'
      return

    response.writeHead 200, 'OK', mainHeaders

    sendEvent = (event) ->
      try
        response.write "event: " + event.event + "\n", 'utf-8'
        response.write "data: " + JSON.stringify(event.data) + "\n\n", 'utf-8'
      catch error
        do stopListening

    stopListening = comp.events.onValue sendEvent

    for event in comp.seedRecords()
      sendEvent event

    response.on 'end', ->
      do stopListening
  # Time out after 25 minutes
  svr.timeout = 25 * 60 * 1000
  svr

module.exports = server

