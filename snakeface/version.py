__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2020, Vanessa SOchat"
__license__ = "MPL 2.0"

__version__ = "0.0.0"
AUTHOR = "Vanessa Sochat"
AUTHOR_EMAIL = "vsochat@stanford.edu"
NAME = "snakeface"
PACKAGE_URL = "https://github.com/snakemake/snakeface"
KEYWORDS = "snakemake,workflow management,pipeline,interface, workflows"
DESCRIPTION = "Snakemake Interface"
LICENSE = "LICENSE"

################################################################################
# Global requirements


INSTALL_REQUIRES = (
    ("snakedeploy", {"min_version": None}),
    ("snakemake", {"min_version": None}),
    ("Django", {"exact_version": "3.0.8"}),
    ("django-q", {"exact_version": "1.3.4"}),
    ("django-taggit", {"min_version": "1.3.0"}),
    ("django-gravatar", {"min_version": "1.4.4"}),
    ("django-ratelimit", {"min_version": "3.0.0"}),
    ("django-extensions", {"min_version": "3.0.2"}),
)

# Dependencies provided by snakemake: pyYaml

EMAIL_REQUIRES = (("sendgrid", {"min_version": "6.4.3"}),)
POSTGRES_REQUIRES = (("psycopg2-binary", {"min_version": "2.8.5"}),)
API_REQUIRES = (("djangorestframework", {"min_version": "3.11.1"}),)


TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)

ALL_REQUIRES = INSTALL_REQUIRES + EMAIL_REQUIRES + POSTGRES_REQUIRES + API_REQUIRES
