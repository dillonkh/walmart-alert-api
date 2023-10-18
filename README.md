
# walmart-alert-api
API that enables users to send requests for reading and writing alert data to a data storage system.

## local setup
This project uses poetry. Follow the [normal installation instructions](https://python-poetry.org/docs/)

In the project root, run the following to install dependencies:
```
poetry shell
poetry install
```
Start the server:
```
uvicorn main:app --reload
```

Go to http://127.0.0.1:8000/docs to see the interactive Swagger docs (this is the easiest way to test)

## bonus points 
### tests
See `pytest` tests in the `tests` directory
Tests all routes to ensure accuracy
**Note**: If I had more time I would make these better. As it is there is sometimes an issue with the sqlite db locking, causing tests to fail. You may have to rerun failing tests to get them all to pass. sqlite does *not* like concurrency turns out :(
### GET /alerts V2
I added an additional route at GET `/v2/alerts`. This route differs in the fact that it allows the end user to pass any one of the three params instead of forcing all three. 

## additional notes
Thank you for your time reviewing this little app! 
I've tried to keep this repo really clean by following conventional commits and styling my code with `isort` and `black`. 
