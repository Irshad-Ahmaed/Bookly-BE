from fastapi import FastAPI, Header, status

app = FastAPI()


@app.get('/')
async def Home() -> dict:
    return {"message": "Welcome, Home"}

@app.get('/get_headers', status_code=status.HTTP_200_OK)
async def get_headers(
    accept:str = Header(None),
    content_type:str = Header(None),
    host:str = Header(None),
    user_agent:str = Header(None)
) -> dict:
    request_headers = {}

    request_headers['Accept'] = accept
    request_headers['Content-Type'] = content_type
    request_headers['Host'] = host
    request_headers['User_Agent'] = user_agent

    return request_headers