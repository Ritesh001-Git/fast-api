# FastAPI

FastAPI is a modern, high-performance Python web framework used for building RESTful APIs. It is designed to be fast to code, easy to learn, and production-ready, with performance levels comparable to NodeJS and Go.

## WHY IS FASTAPI POPULAR? (BENEFITS)
### Super Fast Performance
FastAPI is one of the fastest Python frameworks available, comparable to frameworks like Node.js and Go - thanks to its asynchronous capabilities.
### Easy to Learn & Use
Even beginners can start building APIs quickly because FastAPI uses clean, readable code and Python's standard features.
### Automatic API Documentation
FastAPI automatically generates interactive API documentation (Swagger UI and ReDoc) from your code. It shows all available endpoints with descriptions and allows testing API routes without writing extra documentation yourself.
### Type-Hint-Based Validation
FastAPI uses Python type hints for data validation - this means your API checks incoming data automatically, preventing many bugs early on.
### Async Support
Built-in support for Python's async/await allows handling many requests at the same time.

## WHAT IS ROUTING IN FASTAPI?
Routing means connecting a URL (web address) with a Python function.
In FastAPI, routes are defined using decorators like:
- @app.get() - handles GET requests
- @app.post() — handles POST requests
- @app.put() - handles updates
- @app.delete() - handles deletes
These HTTP methods decide how users will interact with your API. For example, GET is usually for fetching data, and POST is usually for sending (creating) new data.

### PATH PARAMETERS: DYNAMIC URLS

- Part of the actual URL path. They are required to find the specific resource (like a specific user ID).

### QUERY PARAMETERS: OPTIONAL EXTRA INFO

- Added to the end of the URL after a ?. They are typically optional and used to sort, filter, or page through results.


## DATABASE INTEGRATION IN FASTAPI
SQLAlchemy ORM-a powerful Python library that lets you work with databases using Python
classes instead of writing raw SQL queries. FastAPI doesn't force you to use any one database,
but SQLAlchemy is one of the most common and flexible choices.

### Why Use a Database With FastAPI?
Databases let your API persist data - - so the data stays even after your app
restarts.
#### With a database, you can:
- ✓ Save users
- ✓ Store application data
- ✓ Run queries and filters
- ✓ Build real-world applications

We will use SQLAlchemy ORM (Object Relational Mapper) so we can treat
database tables as Python classes and rows as objects.

## WHAT IS AUTHENTICATION VS AUTHORIZATION?

### Authentication
This is the process of verifying who a user is - usually through a login system (like email + password). Only authenticated users should access certain parts of your API.

### Authorization
After authentication, authorization determines what the authenticated user is allowed to do - e.g., regular user vs admin.

### Simple Example:
- **Authentication** = User proves they are user123
- **Authorization** = User123 can view their own data but not delete another user's data

## WHAT & WHY USE JWT (JSON WEB TOKENS)?
-  JWT stands for JSON Web Token a compact token sent by clients to prove they are authenticated.
Tokens are signed with a secret key, so the server can verify they haven't been tampered with.
-  No server-side session storage is needed - everything needed to verify is inside the token.

How JWT Works:
- User logs in with credentials
- Server verifies login and generates a JWT token
- Client includes this token in the Authorization header for future requests
- Server checks token validity before responding
- This pattern makes scalable and stateless authentication possible.
