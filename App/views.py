from logging import logThreads
from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, logout_user, login_required
from .models import Gallery, Image
from . import db, UPLOAD_FOLDER
from werkzeug.utils import secure_filename

import os
import mimetypes
import base64

views = Blueprint("views", __name__)


# The dashboard
# @views.route("/dashboard")
# @login_required
# def dashboard():
#     return render_template("dashboard.html", user=current_user)


# The dashboard
@views.route("/dashboard")
@login_required
def dashboard():
    galleries_data = []
    for gallery in current_user.galleries:
        gallery_data = {}
        gallery_data["gallery"] = gallery
        if gallery.images:
            image = gallery.images[0]
            image_data = base64.b64encode(image.data).decode("ascii")
            image_mime_type = image.mime_type
            gallery_data["image_data"] = image_data
            gallery_data["mime_type"] = image_mime_type
        galleries_data.append(gallery_data)
    return render_template(
        "dashboard.html", user=current_user, galleries_data=galleries_data
    )


# Log the user out
@views.route("/logout")
# @login_required
def logout():
    logout_user()
    flash("Logout successful", category="success")
    return redirect(url_for("auth.login"))


# page for creating an album
@views.route("/new_album", methods=["GET", "POST"])
# @login_required
def new_album():
    if request.method == "POST":
        album_name = request.form.get("album-name")
        existing_album = Gallery.query.filter_by(gallery_name=album_name).first()

        # Check if there is an existing album name
        if existing_album:
            flash("This album name already exists, try another name", category="error")
            return redirect(request.url)

        # Check if the album name is empty
        if album_name == "":
            flash("The album name must not be empty", category="error")
            return redirect(request.url)

        # Create a new album
        album_to_create = Gallery(gallery_name=album_name, user_id=current_user.id)
        db.session.add(album_to_create)
        db.session.commit()
        return redirect(url_for("views.dashboard"))

    return render_template("new_album.html")


# For deleting an album
@views.route("/delete_album/<int:id>")
# @login_required
def delete_album(id):
    try:
        gallery_to_delete = Gallery.query.get(id)

        if gallery_to_delete.user_id == current_user.id:
            db.session.delete(gallery_to_delete)
            db.session.commit()
    except:
        flash("Oops, something went wrong...")
        return redirect(url_for("views.dashboard"))

    return redirect(url_for("views.dashboard"))


# For viewing and adding pictures
# @views.route("/view_album/<int:id>")
# @login_required
# def view_album(id):
#     gallery_to_view = Gallery.query.get(id)
#     return render_template("album_view.html", gallery=gallery_to_view)


# For viewing and adding pictures
@views.route("/view_album/<int:id>")
# @login_required
def view_album(id):
    gallery_to_view = Gallery.query.get(id)

    # List to store image data and mime types
    images_data = []

    # Iterate through images and encode image data
    for image in gallery_to_view.images:
        image_data = base64.b64encode(image.data).decode("ascii")
        image_mime_type = image.mime_type
        image_id = image.id
        images_data.append(
            {"data": image_data, "mime_type": image_mime_type, "id": image_id}
        )

    return render_template(
        "album_view.html", gallery=gallery_to_view, images_data=images_data
    )


# For adding an image
@views.route("/add_image/<int:id>", methods=["GET", "POST"])
# @login_required
def add_image(id):
    if request.method == "POST":
        if "file" not in request.files:
            flash("There is no file part", category="error")
            return redirect(request.url)

        file = request.files["file"]
        gallery = Gallery.query.get(id)

        if file.filename == "":
            flash("There is no file", category="error")
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file_mime_type = mimetypes.guess_type(filename)[0]
            file_content = file.read()
            image_to_add = Image(
                filename=filename,
                data=file_content,
                mime_type=file_mime_type,
                gallery_id=gallery.id,
            )
            db.session.add(image_to_add)
            db.session.commit()
            flash(
                f"Successfully added image to {gallery.gallery_name}",
                category="success",
            )
            return redirect(url_for("views.view_album", id=gallery.id))

    return render_template("upload_image.html")


# For viewing an image
@views.route("/view_image/<int:id>")
#@login_required
def view_image(id):
    image_to_view = Image.query.get(id)

    if image_to_view is None:
        flash("No image found with the provided ID.", category="error")
        return redirect(url_for("views.dashboard"))  # or some other appropriate view

    image_data = base64.b64encode(image_to_view.data).decode("ascii")
    image_mime_type = image_to_view.mime_type

    return render_template(
        "image_view.html",
        image_data=image_data,
        mime_type=image_mime_type,
        image=image_to_view,
    )


# For deleting images
@views.route("/delete_image/<int:id>")
#@login_required
def delete_image(id):
    try:
        image_to_delete = Image.query.get(id)
        gallery_id = image_to_delete.gallery_id
        db.session.delete(image_to_delete)
        db.session.commit()

        flash("Image successfully deleted from the album.", category="success")
        return redirect(url_for("views.view_album", id=gallery_id))
    except:
        return "<h1> Oops, this page could not be reached</h1>"
