from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models.db import db, init_db
from services.api import fetch_rows, import_rows
from models.data import attractions, attraction, save_attraction, remove_attraction, reviews, review, save_review, remove_review, stats

app = Flask(__name__)
app.config.from_object(Config)

@app.context_processor
def common(): return {"site_name": "Atlántico Turístico"}

@app.get("/")
def home():
    try: return render_template("home.html", stats=stats(), latest=attractions(limit=6))
    except Exception as e: return render_template("error.html", error=str(e)), 500

@app.get("/atractivos")
def list_page():
    return render_template("attractions.html", rows=attractions(request.args.get("q",""), request.args.get("municipio",""), request.args.get("tipo","")), q=request.args.get("q",""))

@app.route("/atractivos/nuevo", methods=["GET","POST"])
@app.route("/atractivos/<int:rid>/editar", methods=["GET","POST"])
def attraction_form(rid=None):
    item = attraction(rid) if rid else None
    if request.method == "POST":
        try:
            save_attraction(request.form, rid)
            flash("Registro guardado correctamente.", "success")
            return redirect(url_for("list_page"))
        except Exception as e: flash(str(e), "error")
    return render_template("attraction_form.html", item=item)

@app.post("/atractivos/<int:rid>/eliminar")
def attraction_delete(rid):
    remove_attraction(rid); flash("Registro eliminado.", "success"); return redirect(url_for("list_page"))

@app.get("/resenas")
def review_page(): return render_template("reviews.html", rows=reviews())

@app.route("/resenas/nueva", methods=["GET","POST"])
@app.route("/resenas/<int:rid>/editar", methods=["GET","POST"])
def review_form(rid=None):
    item = review(rid) if rid else None
    if request.method == "POST":
        try:
            save_review(request.form, rid); flash("Reseña guardada.", "success")
            return redirect(url_for("review_page"))
        except Exception as e: flash(str(e), "error")
    return render_template("review_form.html", item=item)

@app.post("/resenas/<int:rid>/eliminar")
def review_delete(rid):
    remove_review(rid); flash("Reseña eliminada.", "success"); return redirect(url_for("review_page"))

@app.route("/importar", methods=["GET","POST"])
def import_page():
    result = None
    if request.method == "POST":
        try: result = import_rows(fetch_rows()); flash("Importación completada.", "success")
        except Exception as e: flash(f"Error al importar: {e}", "error")
    return render_template("import.html", result=result, api_url=app.config["API_URL"])

if __name__ == "__main__": app.run(debug=app.config["DEBUG"])
