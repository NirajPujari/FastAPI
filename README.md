# Fastapi

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python based on standard Python type hints, designed to be asynchronous.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the libraries.

    pip install fastapi pymongo pydantic uvicorn

## How to start

1. Use the git to clone the repo:
    ```bash 
    git clone https://github.com/NirajPujari/fastapi_notes
    ```

2. Navigate to the project directory:
    ```bash 
    cd fastapi_notes
    ```

3. Run the FastAPI application:
    ```bash 
    uvicorn main:app --reload
    ```


## API Documentation

### Authentication Endpoints

- **POST** `/api/auth/signup`: Create a new user account.
- **POST** `/api/auth/login`: Log in to an existing user account and receive an access token.
- **DELETE** `/api/auth/login/{token}`: Log out the user with the given token.

### Note Endpoints

- **GET** `/api/notes`: Get a list of all notes for the authenticated user.
- **GET** `/api/notes/{id}`: Get a note by ID for the authenticated user.
- **POST** `/api/notes`: Create a new note for the authenticated user.
- **PUT** `/api/notes/{id}`: Update an existing note by ID for the authenticated user.
- **DELETE** `/api/notes/{id}`: Delete a note by ID for the authenticated user.
- **POST** `/api/notes/{id}/share`: Share a note with another user for the authenticated user.
- **GET** `/api/search?q=:query`: Search for notes based on keywords for the authenticated user.


#### -> For Authentication of the user we can use a api key and login tokens that can be random but for this we can use below api key 
- **Api Key**:
  ```
  key : ygyrlTfv7tqVznf
- **Login Token**:
  ```
  token : <random for all user>
## Database Information
### Database - MongoDB
- **Type**: NoSQL 

### Database Structure
- **db**:
    - **login**: Collection for storing login information.
    - **signup**: Collection for storing user signup details.
    - **notes**: Collection for storing notes.

### Reason for MongoDB

- **Schema-less Design**
- **Scalability**
- **Document-Oriented**
- **High Performance**
- **Community Support**
- **Adoption**

## Usage Examples(Postman)
### Authentication Endpoints

**Signup:**

**POST** `/api/auth/signup`
- **Body**:
  ```json
  {
      "userid": "example",
      "useremail": "example@example.com",
      "password": "password"
  }
- **Header**:
  ```
  key : ygyrlTfv7tqVznf
**Log-in:**

**POST** `/api/auth/login`
- **Body**:
  ```json
  {
      "userid": "example",
      "password": "password"
  }
- **Header**:
  ```
  key : ygyrlTfv7tqVznf
**Log-out:**

**DELETE** `/api/auth/login{token}`
- **Body**:
  ```json
  {}
- **Header**:
  ```
  key : ygyrlTfv7tqVznf
### Note Endpoints

**Create Note:**

**POST** `/api/notes`
- **Body**:
  ```json
  {
      "title": "Example Note",
      "content": "This is an example note."
  }
- **Header**:
  ```
  key : ygyrlTfv7tqVznf
  token: <logintoken>
**Fetch Notes:**

**GET** `/api/notes`
- **Body**:
  ```json
  {}
- **Header**:
  ```
  key : ygyrlTfv7tqVznf
  token: <logintoken>
**Fetch Notes by ID:**

**GET** `/api/notes/{id}`
- **Body**:
  ```json
  {}
- **Header**:
  ```
  key : ygyrlTfv7tqVznf
  token: <logintoken>
**Update Note by ID:**

**PUT** `/api/notes/{id}`
- **Body**:
  ```json
  {
      "title": "Update Note Title",
      "content": "Update note."
  }
- **Header**:
  ```
  key : ygyrlTfv7tqVznf
  token: <logintoken>
**Delete Note by ID:**

**DELETE** `/api/notes/{id}`
- **Body**:
  ```json
  {}
- **Header**:
  ```
  key : ygyrlTfv7tqVznf
  token: <logintoken>
**Share Note:**

**POST** `/api/notes/{id}/share`
- **Body**:
  ```json
  {
      "touser": "username of person receiving"
  }
- **Header**:
  ```
  key : ygyrlTfv7tqVznf
  token: <logintoken>
**Search Note:**

**POST** `/api/search?query=user=example,title=example`
- **Body**:
  ```json
  {}
- **Header**:
  ```
  key : ygyrlTfv7tqVznf
  token: <logintoken>
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Credits

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [PyMongo](https://pymongo.readthedocs.io/)
- [Uvicorn](https://www.uvicorn.org/)
- License([MIT License](LICENSE))