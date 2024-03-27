# Auto TA

## Installation

### Prerequisites

We need 2 servers:

| Server | Public | Default Port | Runs on |
| :- | :- | :-: | :-: |
| Jupyter Lab | Yes | 8889 | CPU server |
| Proxy | Yes | 8888 | CPU server |
| Backend | No | 8000 | GPU server |

Software: [Miniconda](https://docs.anaconda.com/free/miniconda/index.html#quick-command-line-install)

Alternatively, you can use other Python virtual environment tools and install NodeJS separately.


### Backend

The backend server runs on a GPU server.

1. Create and setup Python virtual environment
   ```bash
   # Create a Python virtual environment
   conda create -n auto-ta python=3.9
   
   # Install the packages
   pip install -r requirements.txt
   ```
2. Under the repo directory, unzip `corpus.zip` and name the folder `corpus`. [Corpus link](https://drive.google.com/file/d/19AmN427dTgKQc1KRUUZUfvPwjZKECSRn)


### Proxy

The proxy server runs on a server that connects to the backend server.

Under directory `proxy/`
  ```bash
  conda env create  # Create a NodeJS virtual environment
  npm install       # Install the packages
  ```


### Jupyter Lab

The JupyterLab server exposes to the public and connects to the proxy server.

[Original Link](https://github.com/jupyterlab/extension-examples/tree/main/react-widget)

1. Clone the Jupyter Lab extention examples repo:
   ```bash
   git clone https://github.com/jupyterlab/extension-examples.git
   ```
2. In `extension-examples`, create and setup environment
   ```bash
   cd extension-examples/
   conda env create
   conda activate jupyterlab-extension-examples
   source ../config_addrs.sh
   ```
3. Install Node modules
   ```bash
   cd react-widget
   jlpm
   jlpm build
   jupyter labextension install .
   ```
4. Copy source code to directory and rebuild Typescript source
   ```bash
   cp ../../jlserver_src/* src/
   jlpm build
   jupyter lab build
   ```

## Launch

On the GPU server:

```bash
source config_addrs.sh
python launch_backend.py
```

On the CPU server:

```bash
# Proxy
conda activate proxy
source config_addrs.sh
cd proxy/
npm start

# JupyterLab
conda activate jupyterlab-extension-examples
source config_addrs.sh
jupyter lab --ip 0.0.0.0 --port ${JPL_PORT}
```
