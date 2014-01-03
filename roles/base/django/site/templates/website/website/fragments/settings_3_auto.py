

# You can override this settings fragment in
# files/django_site/<django_site_slug>/settings_override.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ django_site_db_name }}',
        'USER': '{{ django_site_db_user }}',
        'PASSWORD': '{{ django_site_db_pass }}',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = '{{ django_site_base_dir }}/{{ django_site_slug }}/static/'
MEDIA_ROOT = '/var/www/{{ django_site_slug }}/media/'

ALLOWED_HOSTS = ['*']
