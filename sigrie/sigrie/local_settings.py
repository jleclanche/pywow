
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql_psycopg2", # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
		"NAME": "sigrie2",                      # Or path to database file if using sqlite3.
		"USER": "postgres",                      # Not used with sqlite3.
		"PASSWORD": "postgres",                  # Not used with sqlite3.
		"HOST": "",                      # Set to empty string for localhost. Not used with sqlite3.
		"PORT": "",                      # Set to empty string for default. Not used with sqlite3.
	}
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
