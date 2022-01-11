# Start

```bash
pyenv -m venv venv

source venv/bin/activate

python -m pip install -r requirements.txt

python main.py

```

# build exe

```bash
cp QrPay.spec.bak QrPay.spec

pyinstaller QrPay.spec
```
