pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot app
pybabel update -i messages.pot -d app/translations
pybabel compile -d app/translations