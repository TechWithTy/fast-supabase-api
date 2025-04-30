Endpoints

Consider a FastAPI app with three endpoints:

    /call-other-service
    /factorize
    /health

These are backed by three methods

# non-blocking IO
def call_other_service():

# blocking/CPU heavy
def factorize()

# trivial - immedaite return
def health()

Ok — so do I use async on any/all of these? Unless your app is just a toy/very low complexity, or depends on library that don’t support await I recommend just using async from the jump.

def async call_other_service()
def async factorize()
def async health() 

Sure — the health check is trivial and could drop the async, but things can get hairy when mixing and matching
/call_other_service

This endpoint represents a non-blocking IO operation so we should use await. What the hell is that? It’s anything that calls something else and waits around. Example of this include:

    Making an HTTP request
    Async Database queries

The CPU is not being utilized while the process waits for these to return, so we want to use await to take advantage — in this case, let’s use the httpx library:

import httpx
from fastapi import FastAPI

app = FastAPI()

# The inner async function that fetches data from an external service
async def _fetch():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/todos/1")
        return response.json()  # Non-blocking request

# The FastAPI endpoint that calls the inner function
@app.get("/call_other_service")
async def call_other_service():
    data = await _fetch()  # Call the async inner function
    return data

It’s similar to database queries, but we have to use an async driver to take advantage of non-blocking IO:

import asyncpg
from fastapi import FastAPI

app = FastAPI()

# Async function that fetches data from a database
async def _fetch_db_data():
    conn = await asyncpg.connect(user='user', password='password', database='dbname', host='localhost')
    rows = await conn.fetch("SELECT * FROM your_table WHERE some_column = 'some_value'")  # Non-blocking query
    await conn.close()
    return rows

# FastAPI endpoint that calls the inner function for database query
@app.get("/call_other_service")
async def call_other_service():
    data = await _fetch_db_data()  # Call the async inner function for DB query
    return {"data": data}

/factorize

In contrast to a non-blocking IO operations, where the CPU just sits idle, we have CPU-heavy operations, or blocking operations, these include things like:

    factorize
    using the subprocess library
    printing hello world a trillion times

Ok — so naively you may think simply make blocking tasks synchronous, for example:

@app.get("/factorize")
def factorize():
   ...  

This blocks the worker process entirely while its running. Here are some issues:

    The worker thread is entirely blocked — so for example calls to /health will time out.
    Most blocking tasks aren’t completely CPU-bound like factorize, so there are times that the process spends not burning cycles that are being wasted in a synchronous execution.

Instead we can take advantage of asyncio loops

import asyncio

# Synchronous function for CPU-intensive computation
def _factorize():
    # CPU-intensive computation
    ...

@app.get("/factorize")
async def factorize():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, _factorize)
    return result

Ok so what is going on

    Within each Uvicorn Worker in your FastAPI app, there is an event loop running.
    By offloading factorize into loop.run_in_exectuor it runs in a new thread. These are managed by a ThreadPool, so won’t grow indefinitely.
    TLDR; the factorize endpoint will no-longer block an incoming /health call, as the synchronous version would.

The /health endpoint remains responsive because these requests are handled in the main event loop while the heavy tasks occur in separate threads.
Why do I blog when ChatGPT is way better at everything?

If many requests to /factorize arrive simultaneously, they will get slower and slower as your OS contexts switches between all these threads, but the main event loop will stay responsive for /health and other endpoints.
/health

ChatGPT recommends trivial endpoints still use async for no other reason than code consistency…

    Even for simple endpoints like /health, it's recommended to define them as asynchronous (async def). Keeping all endpoints asynchronous ensures consistency in your codebase, which simplifies maintenance and reduces the risk of errors that can arise from mixing synchronous and asynchronous code. Additionally, if you decide to add asynchronous operations to your health check in the future—such as checking the status of a database connection or an external service—you won't need to refactor the endpoint. Using async throughout your application promotes scalability and keeps your options open for enhancements.

TLDR;

    Use async in all of your endpoint definitions (or at least all non-trivial ones).
    Use await for non-blocking operations like HTTP requests and DB queries — make sure to use asynchronous-compliant libraries like httpx and asyncpg
    Use run_in_executor for blocking/CPU-bound tasks so they don’t make the worker thread unresponsive (ie. fail healthchecks).
    For /health and other non-trivial endpoints that exectute quickly, don’t use await nor run_in_exector.

Complete Example

import asyncio
import asyncpg
from fastapi import FastAPI

app = FastAPI()

# Async function that fetches data from a database
async def _fetch_db_data():
    conn = await asyncpg.connect(
        user='user',
        password='password',
        database='dbname',
        host='localhost'
    )
    rows = await conn.fetch("SELECT * FROM your_table WHERE some_column = 'some_value'")
    await conn.close()
    return rows

# FastAPI endpoint that calls the inner function for database query
@app.get("/call_other_service")
async def call_other_service():
    data = await _fetch_db_data()
    return {"data": data}

# Synchronous function for CPU-intensive computation
def _factorize():
    # CPU-intensive computation
    ...

@app.get("/factorize")
async def factorize():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, _factorize)
    return result

@app.get("/health")
async def health_check():
    return {"status": "healthy"}