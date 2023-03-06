from flask import Flask, render_template, request, url_for,redirect, flash
import json
import random




app = Flask(__name__)
app.config['SECRET_KEY'] = "citation"

citations_list = []
    
id_counter = 1

@app.route("/")
def main():
    if len(citations_list) < 4:
        return redirect(url_for('add'))
    if len(citations_list) > 3:
        cits = []
        sources = []
        random_citations = random.sample(citations_list, min(len(citations_list), 3))
        for citation in random_citations:
            r = json.loads(citation)
            cits.append(r["citation"])
            sources.append(r["source"])
        return render_template("main.html", citations=cits, sources=sources)
    return render_template("main.html")



@app.route("/add", methods=["GET", "POST"])
def add():
    citations = {}
    global id_counter
    if request.method == "POST":
        citation = request.form["citation"]
        author = request.form["source"]
        if author:
            citations["source"] = author
        else:
            citations["source"] = "Unknown"
        citations["citation"] = citation
        citations["id"] = id_counter 
        json_object = json.dumps(citations)
        citations_list.append(json_object) 
        id_counter+=1
        return redirect(url_for("main"))
    return render_template("add.html")

@app.route("/daily")
def daily():
    random_citation = random.sample(citations_list, min(len(citations_list), 1))
    return render_template("daily.html", random_citation=random_citation)

if __name__ == "__main__":
    app.run(debug=True)