from flask import Flask

app = Flask("Ecommerce")


def main():
    app.run(port=5000)


if __name__ == "__main__":
    main()
