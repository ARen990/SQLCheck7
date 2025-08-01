import flask
import models
import forms


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://coe:CoEpasswd@localhost:5432/coedb"

models.init_app(app)


@app.route("/")
def index():
    db = models.db
    notes = db.session.execute(
        db.select(models.Note).order_by(models.Note.title)
    ).scalars()
    return flask.render_template(
        "index.html",
        notes=notes,
    )


@app.route("/notes/create", methods=["GET", "POST"])
def notes_create():
    form = forms.NoteForm()
    if not form.validate_on_submit():
        print("error", form.errors)
        return flask.render_template(
            "notes-create.html",
            form=form,
        )
    note = models.Note()
    form.populate_obj(note)
    note.tags = []

    db = models.db
    for tag_name in form.tags.data:
        tag = (
            db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
            .scalars()
            .first()
        )

        if not tag:
            tag = models.Tag(name=tag_name)
            db.session.add(tag)

        note.tags.append(tag)

    db.session.add(note)
    db.session.commit()

    return flask.redirect(flask.url_for("index"))


@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
def notes_edit(note_id):
    db = models.db
    note = db.session.execute(db.select(models.Note).where(models.Note.id == note_id)).scalars().first()

    if not note:
        flask.abort(404)

    form = forms.NoteForm(obj=note)

    if flask.request.method == "GET":
        # When first loading the form, pre-populate the tags field with comma-separated names
        form.tags.data = [tag.name for tag in note.tags]
    else: # This is a POST request (form submission)
        if not form.validate_on_submit():
            print("error", form.errors)
            return flask.render_template(
                "notes-edit.html",
                form=form,
                note_id=note_id,
            )

        # Manually populate title and description, as populate_obj would cause issues with 'tags'
        note.title = form.title.data
        note.description = form.description.data

        # Clear existing tags before re-adding based on form input
        note.tags = [] 

        # Handle tags: find existing or create new ones
        for tag_name in form.tags.data:
            tag = (
                db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
                .scalars()
                .first()
            )
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
            note.tags.append(tag) # Append the actual Tag object

        db.session.commit()
        return flask.redirect(flask.url_for("index"))

    return flask.render_template(
        "notes-edit.html",
        form=form,
        note_id=note_id,
    )


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def notes_delete(note_id):
    db = models.db
    note = db.session.execute(db.select(models.Note).where(models.Note.id == note_id)).scalars().first()

    if not note:
        flask.abort(404)

    db.session.delete(note)
    db.session.commit()
    return flask.redirect(flask.url_for("index"))


@app.route("/tags/<tag_name>")
def tags_view(tag_name):
    db = models.db
    tag = (
        db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
        .scalars()
        .first()
    )
    if not tag:
        flask.abort(404)

    notes = db.session.execute(
        db.select(models.Note).where(models.Note.tags.any(id=tag.id))
    ).scalars()

    return flask.render_template(
        "tags-view.html",
        tag_name=tag_name,
        notes=notes,
        tag_id=tag.id # Pass tag_id for potential edit/delete links
    )


@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def tags_edit(tag_id):
    db = models.db
    tag = db.session.execute(db.select(models.Tag).where(models.Tag.id == tag_id)).scalars().first()

    if not tag:
        flask.abort(404)

    form = forms.TagForm(obj=tag) # Assuming you have a TagForm in forms.py
    if not form.validate_on_submit():
        print("error", form.errors)
        return flask.render_template(
            "tags-edit.html",
            form=form,
            tag_id=tag_id,
        )

    form.populate_obj(tag)
    db.session.commit()
    return flask.redirect(flask.url_for("tags_view", tag_name=tag.name))


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def tags_delete(tag_id):
    db = models.db
    tag = db.session.execute(db.select(models.Tag).where(models.Tag.id == tag_id)).scalars().first()

    if not tag:
        flask.abort(404)

    # Before deleting the tag, consider how to handle notes that are only associated with this tag.
    # For this example, we'll just delete the tag. If a note becomes tagless, it will still exist.
    db.session.delete(tag)
    db.session.commit()
    return flask.redirect(flask.url_for("index")) # Redirect to home or a tag list page


if __name__ == "__main__":
    app.run(debug=True)