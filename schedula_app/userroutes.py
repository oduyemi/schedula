import os
from flask import render_template, redirect
from schedula_app import starter, db



from schedula_app import starter

@starter.route('/', strict_slashes = False)
def home():
    return render_template('user/index.html')