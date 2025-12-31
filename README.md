# 🔐Full Secure API for Notes Storage

This project is a secure backend API for a notes storage application built with **FastAPI**, **MongoDB**, and **JWT-based** authentication. It provides complete user authentication and authorization, along with protected CRUD operations for managing personal notes.

The API implements a dual-layer security model:

- **JWT (Bearer Token)** for user identity and session validation
- **Per-user API Key** for client-level access control

## ✨Key Features

- User signup and login with hashed passwords
- JWT-based authentication with token verification
- Secure logout with token blacklisting
- Per-user API key generation and validation
- Create, update (bulk), search, and manage notes
- Notes scoped strictly to their owner
- Optional sharing support via user IDs
- MongoDB schema validation and indexing for performance
- UTC-based timestamp handling for consistency

## 🛡️Security Highlights

- Passwords stored using bcrypt hashing
- Stateless JWT authentication
- API key validation on every protected endpoint
- Token revocation support via blacklist
- Ownership checks on all note operations

## ⚙️Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the libraries

```bash
  pip install -r requirements.txt
```

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
   uvicorn main:app --host 127.0.0.1 --port %PORT% --reload --log-level debug
   ```
   or
   ```bash
   ./run
   ```

## 📘API Documentation

### 🔐Authentication Endpoints

- **POST** `/signup`: Create a new user account and receive an API key
- **POST** `/login`: Log in and receive a JWT access token
- **DELETE** `/logout`: Log out the user using the provided token and key

### 👤 User Endpoints

- **GET** `/users`: Fetch authenticated user profile
- **PUT** `/users`: Update user data
- **DELETE** `/users`: Soft delete user (its intentional)

### 📝Note Endpoints

- **GET** `/notes`: Get all notes for the authenticated user
- **GET** `/notes/{id}`: Get a note by ID
- **POST** `/notes`: Create a new note
- **POST** `/notes/bulk`: Create multiple notes
- **PUT** `/notes/{id}`: Update a note by ID
- **PUT** `/notes/bulk?ids={id}...`: Update multiple notes by IDs
- **DELETE** `/notes/{id}`: Delete a note
- **POST** `/notes/share/{id}/{share_with_user_id}`: Share a note with another user
- **POST** `/notes/unshare/{id}/{share_with_user_id}`: Remove access to a shared note
- **GET** `/search?q=:query`: Search notes by title and content

### 🔑Authentication Headers

For authentication, both an API key and a session token are required and are unique per user.

- **Api Key in the header**:
  ```
  x-api-key : <given when sign in>
  ```
- **Login Token**:
  ```
  Authorization : Bearer <given when login>
  ```

**Note:**

- JWT access tokens are valid for **60 minutes**. Logging out or allowing a token to expire will revoke the token. Once revoked or expired, the token cannot be reused, and a new login is required to issue a fresh token.
- The API key is permanent and does not change across logins.

## 🧰Tech Stack

- **FastAPI** – REST API framework
- **MongoDB** – Data storage with schema validation
- **PyMongo** – Database driver
- **JWT (python-jose)** – Authentication
- **Passlib (bcrypt)** – Password hashing

## 🗄️Database (MongoDB)

### Collection

- **blacklisted_tokens**: Collection for all storing blacklisted tokens which is removed with a index later.
- **users**: Collection for storing user data.
- **notes**: Collection for storing user`s notes.

## 📄License

MIT

## 👤Authors

- [@Niraj Pujari](https://github.com/NirajPujari)
