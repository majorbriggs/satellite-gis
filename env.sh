if [ ! -d venv ]; then
    virtualenv -p python3 venv
fi
. venv/bin/activate
cat requirements.txt | xargs pip install
