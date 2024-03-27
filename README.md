# Auto TA

## Installation

| Server | Public | Default Port | Runs on |
| :- | :- |
| Jupyter Lab | Yes | 8889 | CPU server |
| Proxy | Yes | 8888 | CPU server |
| Backend | No | 8000 | GPU server |


### Backend

The backend server runs on a GPU server.

1. Create and setup Python virtual environment
   ```bash
   # Create a Python virtual environment
   conda create -n auto-ta python=3.9
   
   # Install the packages
   pip install -r requirements.txt
   ```
2. Under the repo directory, put documents in `corpus/`.
3. Configuring addresses: `source config_addrs.sh`


### Proxy

The proxy server runs on a server that connects to the backend server.

1. In `proxy/`, create a NodeJS virtual environment
  ```bash
  conda env create
  ```
2. Install packages: `npm install`
3. Configuring addresses: `source config_addrs.sh`


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

```bash
# On the GPU server
python launch_backend.py

# On the CPU server
# Proxy
conda activate proxy
cd proxy/
npm start

# On the CPU server
# JupyterLab
conda activate jupyterlab-extension-examples
jupyter lab --ip 0.0.0.0 --port ${JPL_PORT}
```
