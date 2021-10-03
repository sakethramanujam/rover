import click
import os
from rover.rover.tools import n_pages
from .rover.main import show_missions, show_downlink_status, show_stats, get_cameras, downloader


@click.group()
def cli():
    pass


@cli.command("missions", help="show list of active missions.")
def missions():
    show_missions()


@cli.group(help="show mission status.")
def status():
    pass


@status.command("current", help="info of current/latest downlink.")
@click.argument("mission")
def current(mission):
    show_downlink_status(mission_id=mission, timeline="current")


@status.command("past", help="info of past downlink(s).")
@click.argument("mission")
def past(mission):
    show_downlink_status(mission_id=mission, timeline="previous")


@status.command("future", help="info of upcoming downlinks.")
@click.argument("mission")
def upcoming(mission):
    show_downlink_status(mission_id=mission, timeline="upcoming")


@cli.command("stats", help="Show mission statistics.")
@click.argument("mission")
def stats(mission):
    show_stats(mission_id=mission)


@cli.group(help="show camera instrument info.")
def camera():
    pass


@camera.command("names", help="show camera instrument names.")
@click.argument("mission")
def camnames(mission):
    get_cameras(mission_id=mission, what="names")


@camera.command("ids", help="show camera instrment ids.")
@click.argument("mission")
def camids(mission):
    get_cameras(mission_id=mission, what="ids")


@cli.group(help="download mission raw images/metadata.")
def download():
    pass


@download.command("images", help="download images.")
@click.argument("mission")
@click.option('-r', '--resolution', type=str,
              default="full", show_default=True,
              help="resolution of the images to be download.\
                   Available options: small, medium, large, full")
@click.option('-p', '--path',
              default="./", show_default=True,
              help="path to store the downloaded images.")
@click.option('-pn', '--pagenum', type=int, show_default=True,
              help="value of the page to download images from.")
@click.option('-np', '--npages', type=int, show_default=True,
              help="number of pages to download the images from.")
def imgs(mission, resolution, path, pagenum, npages):
    downloader(mission_id=mission,
               what="images",
               path=path,
               resolution=resolution,
               pagenum=pagenum,
               npages=npages
               )

@download.command("metadata", help="download metadata.")
@click.argument("mission")
@click.option('-p', '--path',
              default="./", show_default=True,
              help="path to store the downloaded images.")
@click.option('-pn', '--pagenum', type=int, show_default=True,
              help="value of the page to download images from.")
@click.option('-np', '--npages', type=int, show_default=True,
              help="number of pages to download the images from.")
def meta(mission, path, pagenum, npages):
    downloader(mission_id=mission,
               what="metadata",
               path=path,
               pagenum=pagenum,
               npages=npages
               )
