import click


@click.group()
def entry():
    pass


@entry.group()
def location():
    pass


@location.command()
def view():
    pass


@location.command()
def open():
    pass


@location.command()
def change():
    pass
