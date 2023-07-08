# python

This repository contains all services written in Python. This was originally focused on PDF form creation, but has since included the rebalancer as well as transfer forecasting code. In order to avoid creating several different services as well as hosting infrastructure, unify all of these Python services into a single package.

## Instructions

1. Install a virtual environment: `python3 -m venv env`
2. Activate the virtual environment: `. env/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the service: `quart --app src/app --debug run --port 8080`
5. Go to http://localhost:27017/generate/Victoria
