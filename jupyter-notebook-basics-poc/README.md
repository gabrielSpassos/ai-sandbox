# Jupyter Notebook Basics POC

## Setup 

* Check python3 installed

```bash
python3 --version
```

* Create virtual env

```bash
python3 -m venv .venv
source .venv/bin/activate
```

* Install Jupyter

```bash
pip3 install notebook ipykernel

or:

pip3 install -r requirements.txt
```

* Register kernal

```bash
python -m ipykernel install --user --name=jupyter-notebook-basics-poc --display-name "Python3 Jupyter Notebook Basics POC"
```
