# library
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
import sys

# Configs
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite']
FLATPAGES_EXTENSION_CONFIGS = {
    'codehilite': {'linenums': True}
}

app=Flask(__name__)
app.config.from_object(__name__)
pages=FlatPages(app)
freezer=Freezer(app)

# URL Routing
@app.route("/")
def index():
    latest=sorted(pages,reverse=True,key=lambda p:p.meta["published"])
    return render_template("index.html",posts=latest[:5])

@app.route("/about/")
def about():
	return render_template("about.html")

@app.route("/tag/<string:tag>/")
def tag(tag):
    tags=[p for p in pages if tag in p.meta.get("tags",[])]
    return render_template("tag.html",tag=tag,pages=tags)

@app.route("/posts/")
def posts():
    posts=[p for p in pages]
    return render_template("post.html",pages=posts)

@app.route("/posts/<path:path>/")
def page(path):
    page=pages.get_or_404(path)
    return render_template("page.html",page=page,pages=pages)

@app.route('/pygments.css')
def pygments():
    return pygments_style_defs(style='algol_nu'), 200, {'Content-Type':'text/css'}

# main
if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=='build':
        freezer.freeze()
    else:
        app.run(port=8000)