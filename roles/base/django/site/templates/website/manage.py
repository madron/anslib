#!{{ site_user_base|default('/var/www') }}/{{ site_slug }}/env/bin/python

# {{ ansible_managed }}

import os
import sys

{% for path in site_python_path|default([]) %}
sys.path.insert(0, '{{ path }}')
{% else %}
sys.path.insert(0, '{{ site_user_base|default('/var/www') }}/{{ site_slug }}/src')
{% endfor %}

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
