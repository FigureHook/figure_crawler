FILE=requirements-top.txt
pip install --upgrade pip
if test -f "$FILE"; then
    pip install -r $FILE
else
    pip install -r requirements.txt
fi