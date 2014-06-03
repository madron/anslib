FROM svendowideit/ambassador
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it

CMD `env | grep _TCP= | sed 's/.*_PORT_\([0-9]*\)_TCP=tcp:\/\/\(.*\):\(.*\)/socat TCP4-LISTEN:\1,fork,reuseaddr TCP4:\2:\3 /'`
