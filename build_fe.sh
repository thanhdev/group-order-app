git submodule update --init --recursive
cd group-order
npm install
npm run build --prod
cd ..
python manage.py collectstatic --noinput -c
pre-commit run -a
git add static/
git commit -m "build frontend"
git push
