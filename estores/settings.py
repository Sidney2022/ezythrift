
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
from django.contrib import messages
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['ezythrift.pythonanywhere.com', 'www.ezythrift.pythonanywhere.com', 'localhost']
EMAIL_TIMEOUT = 60  # Increase the timeout value (in seconds)

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',


    'core',
    'accounts',
    'cloudinary',
    'cloudinary_storage',

    'django_password_validators',
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.common.BrokenLinkEmailsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",

]

ROOT_URLCONF = 'estores.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.generalContext'
            ],
        },
    },
]

WSGI_APPLICATION = 'estores.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
        'accounts.backends.EmailBackend',
        'django.contrib.auth.backends.ModelBackend',

        ]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'django_password_validators.password_character_requirements.password_validation.PasswordCharacterValidator',
        'OPTIONS': {
             'min_length_digit': 3,
             'min_length_alpha': 2,
             'min_length_special': 1,
             'min_length_lower': 4,
             'min_length_upper': 1,
             'special_characters': "~!@#$%^&*()_+{}\":;'[]"
         }
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_TZ = True

LOGIN_URL = '/accounts/auth'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
# @Thrift124
STATIC_URL = 'static/'
STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS=[os.path.join(BASE_DIR, 'static')]
MEDIA_URL = 'media/'
MEDIA_ROOT = '/home/Ezythrift/ezythrift/media/'
#MEDIA_ROOT = 'C:/Users/USER/desktop/proj/estores/media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.Profile'

MESSAGE_TAGS = {
    messages.ERROR : 'danger'
}

ADMIN_MEDIA_PREFIX='/static/admin'

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_UESR')
EMAIL_PORT = os.getenv('PORT')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SECURE_HSTS_SECONDS = 3600
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE  = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS =True
SECURE_HSTS_PRELOAD=True

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "EzyThrift Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "EzyThrift Admin",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "EzyThrift",

    # Logo to use for your site, must be present in static files, used for brand on top left
    # "site_logo": f"logo.svg",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Login to EzyThrift Admin",

    # Copyright on the footer
    "copyright": "EzyThrift  Ltd",

   

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["accounts.view_user"]},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "core"},
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ['auth'],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [ "products.name"],

   
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "accounts.Profile": "fas fa-user",
        "core.Seller": "fas fa-user",
        "core.WishList": "fas fa-heart",
        "core.Cart": "fas fa-shopping-cart",
        "core.Newsletter": "fas fa-mail-bulk",
        "auth.Group": "fas fa-users",
        "core.Product":"fas fa-shopping-bag",
        "core.BannerProduct":"fas fa-shopping-bag",
        "core.Order":"fas fa-cart-plus",
        "core.OrderItem":"fas fa-luggage-cart",
        "core.Category":"fas fa-layer-group",
        "core.ProductType":"fas fa-layer-group",
        "core.SubCategory":"fas fa-layer-group",
        "core.Brand":"fas fa-building",
        "core.Review":"fas fa-edit",
        "core.Faq":"fas fa-question",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fa fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

  
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "collapsible",
    # override change forms on a per modeladmin basis
    # "changeform_format_overrides"/: {"accounts.profile": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    # "language_chooser": True,
    
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-info",
    "accent": "accent-navy",
    "navbar": "navbar-cyan navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-info",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "sandstone",
    "dark_mode_theme": "cyborg",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-outline-success"
    }
}
