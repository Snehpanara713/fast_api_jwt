<!-- do we run project  -->

uvicorn main:app --reload


<!-- how to get authjwt_secret_key -->

open cmd and write a below command

=> python
    => import secrets
    => secrets.token_hex()



<!-- Signup Employee -->

Endpoint: POST /employee/

Description: Registers a new employee.

=> Request Body:

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "password123",
  "phone": "1234567890",
  "Role": "Employee",
  "Date_of_birth": "1990-01-01"
}

-> Response

{
  "hasError": false,
  
  "result": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "Role": "Employee",
    "phone": "1234567890",
    "Date_of_birth": "1990-01-01"
  }
  "statusCode": 200,
  "errorMsg": ""
}


<!-- Login -->

Endpoint: POST /employee/login
Description: Logs in an existing employee.

=> Request Body:

{
  "email": "john@example.com",
  "password": "password123"
}


-> Response:

{
  "hasError": false,
 
  "result": {
    "access_token": "your_access_token",
    "refresh_token": "your_refresh_token"
  }
   "statusCode": 200,
    "errorMsg": ""
}



<!-- Get Employee -->

Endpoint: GET /employee/get_employee

Description: Retrieves details of all employees.
Authorization: Bearer Token (Access Token)

=> Response:


{
  "hasError": false,
  "result": [
    {
      "emp_id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "phone": "1234567890",
      "Role": "Employee",
      "Date_of_birth": "1990-01-01"
    },
    {
      "emp_id": 2,
      "first_name": "Jane",
      "last_name": "Doe",
      "email": "jane@example.com",
      "phone": "0987654321",
      "Role": "Manager",
      "Date_of_birth": "1985-05-05"
    }
      "statusCode": 200,
      "errorMsg": ""
  ]
}



<!-- Authentication -->

This API uses JWT (JSON Web Tokens) for authentication.

=> When an employee signs up or logs in successfully, they receive an access token and a refresh token.

=> The access token should be included in the Authorization header of subsequent requests for protected endpoints.

=> The access token has a limited lifespan. When it expires, the refresh token can be used to obtain a new access token without needing to log in again.



<!-- Built With -->

=> FastAPI - FastAPI framework for building APIs with Python

=> SQLAlchemy - SQL toolkit and Object-Relational Mapping (ORM) for Python

=> AuthJWT - FastAPI JWT Authentication library

