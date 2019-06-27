import os
from flask import Flask

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True, static_url_path = "/tsne_images", static_folder = "tsne_images")
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        DEBUG=True,
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello/')
    def hello():
        return f"Hello, World!"

    import bp_tsne
    app.register_blueprint(bp_tsne.bp)

    return app