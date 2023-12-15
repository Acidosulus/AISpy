from flask import render_template, flash, redirect, url_for, request
from collections.abc import Iterable
from app import app, db, models,connection_fl
from click import echo, style
import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint

def Points_WithOut_Displays():
    return render_template("addresses.html", results=[])
    