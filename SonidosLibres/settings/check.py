def show_settings():
    from SonidosLibres.settings import common
    for name in dir(common):
        print(name, getattr(common, name))

show_settings()