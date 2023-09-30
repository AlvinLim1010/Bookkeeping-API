from src.apis import create_app


global app
app = create_app()

@app.get('/')
def get():
    return {None, 200}

@app.get('/test')
def get():
    return {'test', 200}
    