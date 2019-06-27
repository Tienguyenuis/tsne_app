from flask import(
    Flask, render_template, Blueprint, url_for, request, current_app, flash, redirect
)
import os
from tsne import tsne_visualize

bp = Blueprint(
'tsne', __name__, url_prefix='/', template_folder='templates')

@bp.route("/", methods=['GET', 'POST'])
def choose_file():
    embedding_files = os.listdir(os.getcwd() + '/embeddingfiles/')
    embedding_files.remove('formattedfiles')

    label_files = os.listdir(os.getcwd() + '/labelfiles/')
    label_files.remove('formattedfiles')

    if request.method == "POST":
        try:
            if request.form.get('confirmed') == 'confirmed':
                if not request.form.get('file') or not request.form.get('label') or not request.form.get('iterations'):
                    flash("Embedding file, label file, and iterations has to be checked", category='danger')
                    return redirect(url_for('choose_file'))
                else:
                    return redirect(url_for('tsne.tsne_started', 
                    file = request.form.get('file'), label = request.form.get('label'), iterations = request.form.get('iterations')))
            else:
                flash("You need to check the confirmation box", category='danger')
                return redirect(url_for('choose_file'))
        except:
            pass
    return(render_template("index.html", embeddings = embedding_files, labels = label_files))

@bp.route("started/<file>/<label>/<iterations>", methods=['GET', 'POST'])
def tsne_started(file, label, iterations):
    if request.method == "POST":
        tsne_visualize(file, label, iterations)
        flash("Visualization is finished", category='danger')
        return redirect(url_for('tsne.choose_file'))

    return render_template("confirm.html", file = file)


@bp.route("tsne_links", methods=['GET'])
def tsne_links():
    links = os.listdir(os.getcwd() + '/tsne_images/')
    return render_template("imagelist.html", links = links)

@bp.route("show_tsne/<plot>", methods=['GET'])
def show_tsne(plot):
    return render_template("image.html", plot = plot)
    
