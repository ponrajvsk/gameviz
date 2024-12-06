# Ecommerce

## Setting up Virtual Env

1. Create a virtual environment
    ```bash
    python3.12 -m venv <virtual_env>
    ```
   or
    ```bash
    # If you have virtualenv installed

    virtualenv -p python3.12 <virtual_env>
    ```

2. Activate the virtual environment
    ```bash
    source ./<virtual_env>/bin/activate
    ```

3. Install all dependency
    ```bash
    pip intall -r requirements.txt
    ```
   
You can simply do all the steps by running a command like this
   ```bash
   /bin/bash createNewVirtualenv.sh
   ```
