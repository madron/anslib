#!/bin/sh

set -e

{% for host in k8s_hosts %}
{% if hostvars[host]['dc'] is defined or hostvars[host]['disktype'] is defined %}
# {{ host }}
{{ k8s_bin_dir }}/kubectl label node {{ host }} --overwrite{% if hostvars[host]['dc'] is defined %} dc={{ hostvars[host]['dc'] }}{% endif %}{% if hostvars[host]['disktype'] is defined %} disktype={{ hostvars[host]['disktype'] }}{% endif %}
{% endif %}


{% endfor %}

