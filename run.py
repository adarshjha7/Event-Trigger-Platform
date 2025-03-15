from app import create_app

app = create_app()
@app.route('/test')
def test():
    return {"message": "Flask is working!"}, 200

if __name__ == '__main__':
    app.run(debug=True)