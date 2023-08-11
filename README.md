# hemav-challenge
To be able to run the repository, you must first clone
Once cloned, it can be run in two ways: from localhost in your machine or using Docker containers.

## Localhost in your machine
- Primero, se deben descargar los módulos a utilizar. En este caso, los módulos se encuentran en el archivo "requirements.txt", para descargar los módulos usas el comando `pip install -r requirements.txt`
- You must create an .env file where the environment variables used by the repository will be stored. To create it, there is a file called "env.txt" which contains a skeleton with the environment variables needed to run the program. The values of the environment variables must be selected by you.
- In order to run the program, you must run the command `uvicorn main:app --reload`, which executes FastAPI using localhost as the server.

## Docker container
. Hay que tener en cuenta que Docker debe estar instalaldo previamente. 
- You must build the container where the application will run. As the Dockerfile is already created, you only need to run the `docker build -t my-fastapi-app .` command for the build.
- After the container has been built, it is necessary to run it. To do so, the command `docker run -d -p 8000:8000 my-fastapi-app` must be entered. Your application will now be running on localhost.

You can enter the url "localhost:8000/docs" to test the generated endpoint. Inside the repository there is a csv file called "test-info.csv", which gets information from different parameters to make several requests to the image API. 

It should be noted that in this case, since the EARTH API from NASA was not working, we made use of the APOD API also from NASA, which returns a JSON but within that json we get different space images that will vary depending on the query params that are entered.
Additionally, remember that a mock was made to the AWS S3 to simplify its use and facilitate access to accounts and everything related.
