import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# 🔹 Glavna stran
@app.route('/')
def hello_world():
    return render_template("main.html")


# 🔹 Testna stran
@app.route('/test/<username>')
def test(username):
   return render_template("test.html", username=username)


# 🔹 Obrazec za prijavo
@app.route('/form/')
def janez():
    return render_template("form.html")


# 🔹 Obdelava prijave
@app.route('/odaja/')
def odaja():
    name = request.args.get("name")
    geslo = request.args.get("geslo")
    print(name, geslo)

    if name == "admin" and geslo == "1234":
        return "Hvala za prijavo, " + name
    else:
        return render_template("form.html", infotext="Ni uspelo")



@app.route('/registracija/')
def form_test():
    return render_template("registracija.html", infotext="", odaja="Registriraj se")



@app.route('/registracija-submit/', methods=['POST', 'GET'])
def form_submit():
  
    uporabnisko_ime = request.values.get("name")
    geslo = request.values.get("geslo")


    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

  
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT
        )
    ''')

    cursor.execute(
        'INSERT INTO contacts (first_name, last_name) VALUES (?, ?)',
        (uporabnisko_ime, geslo)
    )

    conn.commit()
    conn.close()

    print("Shranjeno:", uporabnisko_ime, geslo)

    return f"Hvala za registracijo, {uporabnisko_ime}!"


@app.route('/prijava/')
def prijava():
    return render_template("prijava.html", napaka="")



@app.route('/prijava-submit/', methods=['POST'])
def prijava_submit():
    uporabnisko_ime = request.form.get("name")
    geslo = request.form.get("geslo")

    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM contacts WHERE first_name=? AND last_name=?",
        (uporabnisko_ime, geslo)
    )
    uporabnik = cursor.fetchone()
    conn.close()

   
    return render_template("prijava.html", napaka="uspešno.")


@app.route('/View_db/')
def View_db():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts;")
    podatki = cursor.fetchall()
    conn.close()

   
    html = "<h2>Podatki v bazi:</h2><table border=1><tr><th>ID</th><th>Ime</th><th>Geslo</th></tr>"
    for row in podatki:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    html += "</table>"
    return html



if __name__ == "__main__":
    app.run(debug=True)
