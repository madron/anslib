

# You can override this settings fragment in
# files/django_site/<site_slug>/settings_override.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ site_db_name }}',
        'USER': '{{ site_db_user }}',
        'PASSWORD': '{{ site_db_pass }}',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = '{{ site_user_base|default('/var/www') }}/{{ site_slug }}/static/'
MEDIA_ROOT = '/var/www/{{ site_slug }}/media/'

ALLOWED_HOSTS = ['*']
