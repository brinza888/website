from app import create_app


app = create_app()


if __name__ == '__main__':
    app.run(
        host=app.config["DEBUG_HOST"],
        port=app.config["DEBUG_PORT"]
    )
