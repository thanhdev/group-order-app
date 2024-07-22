git submodule update --init --recursive
npm install --prefix group-order
npm run build --prefix group-order
python manage.py collectstatic --noinput -c
