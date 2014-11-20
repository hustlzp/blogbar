# coding: utf-8
from flask import render_template, Blueprint, flash, redirect, url_for, abort, request
from ..models import db, Blog, Post
from ..utils.permissions import AdminPermission

bp = Blueprint('admin', __name__)


@bp.route('/approve')
@AdminPermission()
def approve():
    return "yes"