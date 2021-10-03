import click
from .rover.main import show_missions, show_downlink_status, show_stats, get_cameras


@click.group()
def cli():
    pass


@cli.command("missions", help="Show list of active missions ")
def missions():
    show_missions()


@cli.group(help="Show mission status")
def status():
    pass


@status.command("current", help="info of current/latest downlink")
@click.argument("mission")
def current(mission):
    show_downlink_status(mission_id=mission, timeline="current")


@status.command("past", help="info of past downlink(s)")
@click.argument("mission")
def past(mission):
    show_downlink_status(mission_id=mission, timeline="previous")


@status.command("future", help="info of upcoming downlinks")
@click.argument("mission")
def upcoming(mission):
    show_downlink_status(mission_id=mission, timeline="upcoming")


@cli.command("stats", help="Show mission statistics")
@click.argument("mission")
def stats(mission):
    show_stats(mission_id=mission)


@cli.group(help="Show camera info")
def camera():
    pass


@camera.command("names", help="Show camera names")
@click.argument("mission")
def camnames(mission):
    get_cameras(mission_id=mission, what="names")


@camera.command("ids", help="Show camera ids")
@click.argument("mission")
def camids(mission):
    get_cameras(mission_id=mission, what="ids")


@cli.group(help="Download mission raw images/metadata")
def download():
    pass


@download.command("images", help="Download Images")
@click.argument("mission")
@click.option('-r', '--resolution', help="")
@click.option('-p', '--path', help="Path to store the downloaded images")
def download_images(mission, r):
    pass
