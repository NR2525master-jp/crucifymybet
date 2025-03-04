import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY のチェック
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY が設定されていません。環境変数を設定してください。")

# 本番/開発切り替え
DEBUG = os.getenv("DEBUG", "False") == "False"

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"

# ALLOWED_HOSTS の設定
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS")
if ALLOWED_HOSTS:
    ALLOWED_HOSTS = ALLOWED_HOSTS.split(",")
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

X_FRAME_OPTIONS = "DENY"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
# 開発環境のみ debug_toolbar を有効化
if DEBUG:
    if "debug_toolbar" not in INSTALLED_APPS:
        INSTALLED_APPS.append("debug_toolbar")
    if "debug_toolbar.middleware.DebugToolbarMiddleware" not in MIDDLEWARE:
        MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")


# 本番環境の設定
SECURE_BROWSER_XSS_FILTER = True  # XSS対策
SECURE_CONTENT_TYPE_NOSNIFF = True  # MIME スニッフィング対策
SECURE_HSTS_SECONDS = 31536000  # HSTS（1年間）
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # サブドメインも HSTS 適用
SECURE_HSTS_PRELOAD = True  # HSTS Preload 対応
SESSION_COOKIE_SECURE = True  # HTTPS のみでクッキー送信
CSRF_COOKIE_SECURE = True  # CSRF クッキーを HTTPS のみに制限
SECURE_SSL_REDIRECT = True  # HTTP から HTTPS へ強制リダイレクト

# 開発環境の設定
# 開発環境用に一時的に無効化する（HTTPS リダイレクトをしない）
#SECURE_SSL_REDIRECT = False  # ローカルでのデバッグ用
#SECURE_HSTS_SECONDS = 3600  # 1時間（テスト用）
#SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # サブドメインは適用しない
#SECURE_HSTS_PRELOAD = False  # プリロードリストに登録しない

# CORS の設定
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "False") == "True"

if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if os.getenv("CORS_ALLOWED_ORIGINS") else []

CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
#開発用　CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "x-csrftoken",
    "x-requested-with"
]

ROOT_URLCONF = 'myproject.urls'

# 内部IPを開発環境でのみ許可
INTERNAL_IPS = ["127.0.0.1"] if DEBUG else []


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'myapp' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# Database 設定
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True
USE_TZ = True

# 静的ファイルのURLパス（URLはそのままで大丈夫）
STATIC_URL = '/static/'

# 静的ファイルを集める場所（ディレクトリ）
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# プロジェクト内で静的ファイルを検索するディレクトリ（ファビコンなど）
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
