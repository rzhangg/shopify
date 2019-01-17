# Partner Ticket Intelligence: Python Backend

The backend application is responsible for providing RESTful services, which are written using [Python 3](https://www.python.org/) and [Flask](http://flask.pocoo.org/).

## Running locally

### Virtual environment
To avoid the mess of multiple versions, due to multiple local projects, it's recommended to take advantage of Python Virtual Enviromments, or simply [venv](https://docs.python.org/3/tutorial/venv.html).

On MacOS:
```
cd partner-ticket-ml-v2/python
python3 -m venv venv
. venv/bin/activate
```

On Windows:
```
cd partner-ticket-ml-v2\python
py -3 -m venv venv
venv\Scripts\activate
```

### Install support tools
Once you are inside the Virtual Environment, upgrade the following tools, which are going to be used for development.

```
pip install --upgrade pip wheel
pip install -U pylint
```

### Downloading required dependencies
Still in your Virtual Environment, execute the following command, which will download required dependencies and install in the project.

```
pip install -r requirements.txt --index-url http://nexus.wdf.sap.corp:8081/nexus/content/groups/build.milestones.pypi/simple/ --trusted-host nexus.wdf.sap.corp
```

### Running Visual Studio Code
As long as you run VSCode (running ```code .```) from inside your Virtual Environment, no further configuration is required.

## Tests
Tests are located in the ```/tests``` folder and executed by **PyTest**, which can be installed by

```
pip install pytest
pytest --version 
```