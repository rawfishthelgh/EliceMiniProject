from flask import Blueprint
from flask import Flask, render_template, redirect, url_for

bp = Blueprint('main', __name__, url_prefix='/main')


@bp.route('/')
def main():
    return 'This is main page'