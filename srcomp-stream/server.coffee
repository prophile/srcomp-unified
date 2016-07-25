configuration = require "./config"
srcomp = require "./srcomp"
Bacon = require 'baconjs'

sse = require './http-socket'

comp = new srcomp.SRComp configuration.SRCOMP

comp.events.onValue (event) ->
  console.log JSON.stringify(event, null, 2)

sse(comp).listen(configuration.WEB_PORT, '::')

