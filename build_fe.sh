cd frontend
npm install
npm run build
cd ..
python manage.py collectstatic --noinput
pre-commit run -a
git add static/
git commit -m "build frontend"
git push
