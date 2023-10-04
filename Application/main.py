# Creating our app from the website directory

from Website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
