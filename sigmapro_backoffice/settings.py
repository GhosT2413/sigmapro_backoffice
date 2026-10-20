from pathlib import Path
import pymysql

pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-sigmapro-backoffice-secret-key-production-ready'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sigmapro_backoffice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sigmapro_backoffice.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sigmapro_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración personalizada de Django Unfold con la paleta de colores de SIGMAPRO
# Mint: #6ee7b7 / #059669 | Orange: #ff8000 | Dark background & Modern UI
UNFOLD = {
    "SITE_TITLE": "SIGMAPRO Backoffice",
    "SITE_HEADER": "SIGMAPRO Administración Central",
    "SITE_URL": "http://localhost:4200",
    "SITE_ICON": {
        "light": lambda request: "/static/images/logo-icon.svg",
        "dark": lambda request: "/static/images/logo-icon.svg",
    },
    "SITE_LOGO": {
        "light": lambda request: "/static/images/logo.svg",
        "dark": lambda request: "/static/images/logo.svg",
    },
    "THEME": "dark",
    "STYLES": [
        lambda request: "/static/css/sigmapro_admin.css",
    ],
    "COLORS": {
        "primary": {
            "50": "240 253 244",
            "100": "209 250 229",
            "200": "167 243 208",
            "300": "110 231 183",  # #6ee7b7 Mint
            "400": "52 211 153",
            "500": "16 185 129",
            "600": "5 150 105",   # #059669 Mint Dark
            "700": "4 120 87",
            "800": "6 95 70",
            "900": "6 78 59",
            "950": "2 44 34",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Gestión de Usuarios",
                "separator": True,
                "items": [
                    {
                        "title": "Usuarios del Sistema",
                        "icon": "people",
                        "link": "/admin/core/usuario/",
                    },
                    {
                        "title": "Roles y Privilegios",
                        "icon": "admin_panel_settings",
                        "link": "/admin/core/role/",
                    },
                    {
                        "title": "Cuentas Backoffice (Staff)",
                        "icon": "shield_person",
                        "link": "/admin/auth/user/",
                    },
                ],
            },
            {
                "title": "Operación & Clientes",
                "separator": True,
                "items": [
                    {
                        "title": "Talleres Mecánicos",
                        "icon": "store",
                        "link": "/admin/core/taller/",
                    },
                    {
                        "title": "Clientes",
                        "icon": "badge",
                        "link": "/admin/core/cliente/",
                    },
                    {
                        "title": "Vehículos Registrados",
                        "icon": "directions_car",
                        "link": "/admin/core/vehiculo/",
                    },
                    {
                        "title": "Catálogo de Servicios",
                        "icon": "miscellaneous_services",
                        "link": "/admin/core/servicio/",
                    },
                ],
            },
            {
                "title": "Taller, Fichas & IA",
                "separator": True,
                "items": [
                    {
                        "title": "Fichas de Mantención",
                        "icon": "build",
                        "link": "/admin/core/fichamantencion/",
                    },
                    {
                        "title": "Alertas de Mantención",
                        "icon": "notifications_active",
                        "link": "/admin/core/alertamantencion/",
                    },
                    {
                        "title": "Predicciones IA",
                        "icon": "psychology",
                        "link": "/admin/core/prediccionia/",
                    },
                ],
            },
        ],
    },
}
