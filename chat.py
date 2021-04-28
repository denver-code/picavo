from app import create_app, socketio
import sass

app = create_app(debug=True)
app.jinja_env.add_extension("pyjade.ext.jinja.PyJadeExtension")

if __name__ == "__main__":
    sass.compile(
        dirname=("app/static/sass", "app/static/css"), output_style="compressed"
    )
    socketio.run(
        app,
        host='0.0.0.0',
        port=80
    )
