from settings import app

def register_blueprints(app):
    from Controllers.controller import posts_controller
    app.register_blueprint(posts_controller)

register_blueprints(app)

if __name__ == "__main__":
    app.run(debug=True)
