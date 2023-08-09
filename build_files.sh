echo "BUILD START"
python3.9 -m pip install -r requirements.txt
python3.9 projectile/manage.py collectstatic --oninput --clear
echo "BUILD END"