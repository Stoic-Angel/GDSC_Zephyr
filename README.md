# GDSC Zypher

## How to run it locally?

- Clone the repository
- Create virtual environment using `python -m venv venv`
- Activate the virtual environment using `source venv/bin/activate`
- Install the dependencies using `pip install -r requirements.txt`
- Run the development server using `uvicorn main:app --reload`

## How to run it using Docker? (for production)

- Clone the repository
- Build the docker image using `docker build -t gdsc-zypher .`
- Run the docker container using `docker run -d --name gdsc-zypher -p 8000:8000 gdsc-zypher`
