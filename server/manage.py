import os
import click
from api import app
from bottle import run
from dotenv import load_dotenv


load_dotenv('../.env')


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def main():
    pass

@main.command()
@click.option(
    '--ip', '-ip', default=os.getenv('SERVER_IP', '0.0.0.0'), type=str,
    help='Set application server ip'
)
@click.option(
    '--port', '-p', default=os.getenv('SERVER_PORT', 8000), type=int,
    help='Set application server port'
)
@click.option(
    '--debug', '-d', default=os.getenv('START_DEBUG', False), type=int,
    help='Set application server debug. 0 -> False. 1 -> True'
)
def start_server(port, ip, debug):
    click.echo(f'Start server at: {ip}:{port}')
    run(app=app, host=ip, port=port, debug=bool(debug), reloader=bool(debug))


@main.command()
def test():
    import unittest
    loader = unittest.TestLoader()
    tests = loader.discover('tests')
    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(tests)


if __name__ == "__main__":
    main()
