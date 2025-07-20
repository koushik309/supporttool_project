import ssl
from fastapi import FastAPI
import uvicorn
from cert_utils import generate_self_signed_cert

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "SupportTool API running"}

@app.get("/swagger")
def swagger_ui_placeholder():
    return """
    <html>
    <head><title>Swagger UI</title></head>
    <body><h1>Swagger UI</h1></body>
    </html>
    """

if __name__ == "__main__":
    cert_file, key_file = generate_self_signed_cert("certs")

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    uvicorn.run("mock_supporttool:app",
                host="0.0.0.0",
                port=60000,
                ssl_certfile=cert_file,
                ssl_keyfile=key_file)


