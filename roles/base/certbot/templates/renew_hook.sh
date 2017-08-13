#!/bin/sh

/usr/bin/logger -t certbot_renew_hook "Lineage: $RENEWED_LINEAGE"

{% for domain, hooks in certbot_renew_hook.items() %}
# {{ domain }}
if [ "$RENEWED_LINEAGE" = "/etc/letsencrypt/live/{{ domain }}" ]; then
    /usr/bin/logger -t certbot_renew_hook "Domain: {{ domain }}"
{% for hook in hooks %}
    {{ hook }} 2>&1 | /usr/bin/logger -t certbot_renew_hook
{% endfor %}
fi

{% endfor %}
