from sys import argv

argc = len(argv)

if __name__ == '__main__':
    keys = set(argv)

    if "--generate-gps" in keys or "-ggps" in keys:
        from server.utils.json.generate_gps import generate

        generate()

    if "--create-data-base" in keys or "-cdb" in keys:
        from server.utils.create_db import create

        create()

    if argc == 1 or "--start" in keys or "-s" in keys:
        from server.server import app

        app.run()
