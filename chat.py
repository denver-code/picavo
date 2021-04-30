from app import create_app, socketio
from os import path, walk
import sass

app = create_app(debug=True)
app.jinja_env.add_extension("pyjade.ext.jinja.PyJadeExtension")


extra_dirs = ['app/static', 'app/templates']
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)

if __name__ == "__main__":
    sass.compile(
        dirname=("app/static/sass", "app/static/css"), output_style="compressed"
    )
    socketio.run(
        app,
        extra_files=extra_files
    )
