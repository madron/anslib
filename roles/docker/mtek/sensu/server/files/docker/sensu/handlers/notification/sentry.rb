#!/usr/bin/env ruby

require 'rubygems' if RUBY_VERSION < '1.9.0'
require 'sensu-handler'
require 'raven'


class Sentry < Sensu::Handler
  def handle

    # set the sentry level based off of sensus status
    if @event['check']['status'] == 0
      level = 'info'
    elsif @event['check']['status'] == 1
      level = 'warning'
    elsif @event['check']['status'] == 2
      level = 'error'
    else
      level = 'fatal'
    end

    # Configure raven
    Raven.configure() do |config|
      config.dsn = settings['sentry']['dsn']
      if settings['sentry']['timeout']
        config.timeout = settings['sentry']['timeout']
      else
        config.timeout = 5
      end
    end

    # Send message
    message = @event['client']['name'] + ' ' + @event['check']['name']
    Raven.capture_message message,
        server_name: @event['client']['name'],
        level: level,
        extra: {
            output: @event['check']['output'],
            sensu_id: @event['id']
        },
        tags: {
            version: @event['client']['version']
        }

  end

end
