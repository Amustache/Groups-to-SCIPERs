import os
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
import random
from bs4 import BeautifulSoup
import re
from secrets import DEFAULT_SCIPERS, DEFAULT_SCIPERS_NAMES

PERSON_REGEX = "\/viewtype\?type\=person\&id\=\d+"


def extract_sciper_from_link(content):
    results = re.findall(PERSON_REGEX, content)
    if results:
        return int(results[0].split("id=")[1])


def extract_scipers_from_page(content):
    return set([int(result.split("id=")[1]) for result in re.findall(PERSON_REGEX, content)])


def extract_scipers_from_string(content):
    return set([int(result) for result in re.findall("\d{6,6}", content) if len(result) == 6])


UPLOAD_FOLDER = "."
ALLOWED_EXTENSIONS = {"html", "htm"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "d456s456qsdf3456qsf3456qsf3456"


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("HTML file not found.", "danger")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("HTML file not selected.", "danger")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            with open(filename, "r") as webpage:
                content = webpage.read()

            _, useful = content.split("<table>")
            useful, _ = useful.split("</table>")

            soup = BeautifulSoup(useful, "html.parser")

            scipers_admins = set()
            scipers_members = set()
            for th in soup.find_all("th"):
                text = th.get_text().replace("\n", " ").strip()
                if "Admin" in text:
                    td = th.find_next("td")
                    for a in td.find_all("a"):
                        sciper = extract_sciper_from_link(a.get("href"))
                        if sciper:
                            scipers_admins.add(sciper)
                if "Memb" in text:
                    members = th.find_next("td")
                    if th.find_next("div").get("id") == "tree":
                        members = members.find_next("span")
                        for member in members:
                            if member.name == "div":
                                sciper = extract_sciper_from_link(member.find_next("a").get("href"))
                                if sciper:
                                    scipers_members.add(sciper)
                    else:
                        scipers_members = set([extract_sciper_from_link(a.get("href")) for a in members.find_all("a")])

            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            scipers_to_remove = extract_scipers_from_string(request.form["filters"])
            remove_admins = request.form.get("remove_admins")
            result = scipers_members - scipers_to_remove
            result -= scipers_admins if remove_admins else set()

            result = list(result)

            if request.form["sorting"] == "ascending":
                result = sorted(result)
            elif request.form["sorting"] == "descending":
                result = sorted(result, reverse=True)
            else:
                random.shuffle(result)

            flash(", ".join([str(sciper) for sciper in result]) + "<hr/>Total: {}".format(len(result)), "success")
            return redirect(request.url)
        else:
            flash("Not a correct file.", "danger")
            return redirect(request.url)
    return render_template("index.html", default_scipers=DEFAULT_SCIPERS, default_scipers_names=DEFAULT_SCIPERS_NAMES)


if __name__ == "__main__":
    app.run()
