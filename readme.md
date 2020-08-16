# Databases Classifier

Databases Classifier is a Python application which enables to classify columns of MySQL databases based on the names. For that purpose, a set of classifiers formed by a name and a list of regular expressions can be defined and will be used to tag each column. More than one type is supported per column.

## Requirements

1. MongoDB Server
1. Docker

## How to build the API

1. Build Docker image replacing the required arguments.

    | Argument                | Description                                                                  |
    | ----------------------- | ---------------------------------------------------------------------------- |
    | MONGO_CONNECTION_STRING | Connection string of MongoDB.                                                |
    | CRYPTOGRAPHY_KEY        | A URL-safe base64-encoded 32-byte key use for encrypting database passwords. |
    | JWT_KEY                 | Key used for signing JSON Web Tokens.                                        |
  
   ```shell
   docker build --build-arg MONGO_URI=<MONGO_CONNECTION_STRING> --build-arg CRYPTO_KEY=<CRYPTOGRAPHY_KEY> --build-arg JWT_KEY=<JWT_KEY> -t classifier-api .\
   ```

2. Run Docker image:

   ```shell
   docker run -p 8080:8080 --rm --name classifier-api classifier-api
   ```

## Documentation

### Swagger

1. API Swagger documentation can be accesed by navigating to <http://API_ADDRESS:8080/api/v1>.

### Authentication

Most of the API endpoints require a JSON Web Token to be provided as an authentication mechanism. For that reason, the following header must be provided:

```markdown
Authorization: Bearer JSON_WEB_TOKEN
```

#### Login

To request a new token, a POST request should be made to _/api/v1/auth/login_ endpoint with the username and password.

#### Register

By default, _/auth/register_ is enabled and supports the creation of new users. Passwords will be hashed using [bcrypt](https://github.com/pyca/bcrypt/) library. **This endpoint must be disabled or secured when running in a production environment**

### Classifiers

Classifiers are regular expressions used to categorize each column of the databases. Each classifier should have a unique name and a list of expressions.

#### Define a new classifier

For defining a new classifier, a POST request should be made to _/api/v1/classifier_ endpoint providing the name and the list of regular expressions. Note that the classifiction process is case insensitive.

### MySQL Databases

#### Add a new database

Databases intended to be scanned must be added making POST requests to _/api/v1/database_ endpoint providing all the connection details. Note that the connection password will be saved as an encrypted value using symmetric authenticated cryptography provided by [Fernet](https://cryptography.io/en/latest/fernet/) library.

As a response, an ID will be outputted which can then be used for starting the scanning process.

#### Get all databases

Databases can be retrieved by making a GET request to _/api/v1/database_ endpoing.

#### Scan a database

To start a database scan, a POST request should be done to _/api/v1/database/scan/:DATABASE_ID_ endpoint.

This will trigger a process which will:

- Connect to the desired database and retrieve the structure of all of its schemas by running an SQL query. The following system schemas will be skipped: _information\_schema_, _performance\_schema_, _sys_ and _mysql_.
- Retrieve all defined classifiers.
- For each column of each table of each schema, the classifiers are compared to validate if matches are found.

As the process can take some time, a history object will be outputted which can then be referenced to view then scan status. Once the scan is completed, the history object will be updated with the execution results. In case of success, the database structure will also be updated.

#### Get last scan

To view the last database scan, a GET request should be done to _/api/v1/database/scan/:DATABASE_ID_ endpoint. The history reference and the structure will be outputted.

Also, _/api/v1/database/scan/:DATABASE_ID_/render can be navigated from a web broser to view the response as an HTML.

### History

All scan executions and the results will be stored. For getting all the logs, a GET request should be done to _/history_ or to _/history/:id_ if a specific record is desired. The status code will represent the following:

| Status | Description |
| ------ | ----------- |
| 0      | Running     |
| 1      | Success     |
| -1     | Error       |

## Example

An example is provided for testing purposes. To execute it, follow the steps:

1. Build and run the Docker image with the following arguments:

    | Argument                | Value                                        |
    | ----------------------- | -------------------------------------------- |
    | MONGO_CONNECTION_STRING | mongodb://MONGO_URL:27017/classifier         |
    | CRYPTOGRAPHY_KEY        | KYCbSsOCWCOSZ_J1St6se_HW8ne0mOOJFgOutSsnCxo= |
    | JWT_KEY                 | dBClas$ifier@2o2o                            |

1. Open a Mongo shell and load the _.\example\mongo.js_ file. This will create a sample user and the following classifiers:

    | Name          | Regex                |
    | ------------- | -------------------- |
    | USERNAME      | ^.*username.*$       |
    | EMAIL_ADDRESS | ^.*email.*$          |
    |               | ^.*mailbox.*$        |
    | PASSWORD      | ^pass.*$             |
    | CREDIT_CARD   | ^.*card((?!type).)*$ |
    | PHONE_NUMBER  | ^.*phone.*$          |

    ```shell
    load(".\\example\\mongo.js")
    ```

1. Execute the SQL script _.\example\test_data.sql_ on a MySQL Server. It will create the following schemas:

    | Schema  | Table        | Column      |
    | ------- | ------------ | ----------- |
    | schema1 | payments     | id          |
    |         |              | user_id     |
    |         |              | credit_card |
    |         |              | total       |
    |         | users        | id          |
    |         |              | username    |
    |         |              | password    |
    |         |              | email       |
    | schema2 | customers    | id          |
    |         |              | Mailbox     |
    |         |              | Passphrase  |
    |         |              | WorkPhone   |
    |         |              | MobilePhone |
    |         | transactions | id          |
    |         |              | customerId  |
    |         |              | cardType    |
    |         |              | cardNumber  |
    |         |              | Total       |

1. Authenticate with the API by calling POST _/api/v1/auth/login_ with the following body:

    ```JSON
    {
      "username": "admin",
      "password": "classifier2020"
    }
    ```

    A token will be generated and must be provided to the authorization header to all the following requests.

    ```markdown
    Authorization: Bearer JSON_WEB_TOKEN
    ```

1. Add the MYSQL Server to the application using POST _/api/v1/database_ endpoint with the following body:

    ```JSON
    {
      "host": "MYSQL_HOST",
      "port": 3306,
      "username": "MYSQL_USERNAME",
      "password": "MYSQL_PASSWORD",
    }
    ```

   The created database ID will be outputted.

1. Start a scan by making a request to POST _/api/v1/database/scan/:db\_id_. A history ID will be retrieved to check the execution status.

1. Check the scan status by making a request to GET _/api/v1/history/:history\_id_. Wait until status is 1.

1. Get the results by calling GET _/api/v1/database/scan/:db\_id_ or GET _/api/v1/database/scan/:db\_id/render_ if an HTML output is desired. The expected result should be:

    | Schema  | Table        | Column      | Type          |
    | ------- | ------------ | ----------- | ------------- |
    | schema1 | payments     | id          | N/A           |
    |         |              | user_id     | N/A           |
    |         |              | credit_card | CREDIT_CARD   |
    |         |              | total       | N/A           |
    |         | users        | id          | N/A           |
    |         |              | username    | USERNAME      |
    |         |              | password    | PASSWORD      |
    |         |              | email       | EMAIL_ADDRESS |
    | schema2 | customers    | id          | N/A           |
    |         |              | Mailbox     | EMAIL_ADDRESS |
    |         |              | Passphrase  | PASSWORD      |
    |         |              | WorkPhone   | PHONE_NUMBER  |
    |         |              | MobilePhone | PHONE_NUMBER  |
    |         | transactions | id          | N/A           |
    |         |              | customerId  | N/A           |
    |         |              | cardType    | N/A           |
    |         |              | cardNumber  | CREDIT_CARD   |
    |         |              | Total       | N/A           |
