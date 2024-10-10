# Receptor AI test task

*To start the project you need to execute:**

* clone project repo
* Create an .env file and populate it following the default.env file example

* execute the command `make build`
* execute the command `make run`


you can check swagger on http://0.0.0.0:8080/docs

you can fill initial db data in [initial_data.py](src%2Fdb_utils%2Finitial_data.py)

you can get token on POST http://0.0.0.0:8080/auth/login

you can send events on POST http://0.0.0.0:8080/event

you can see logs in you terminal