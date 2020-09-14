from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy

uygulama = Flask(__name__)
uygulama.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Ahmet Emre/Desktop/Udemy Python Dersleri/ToDo Uygulaması/todo_veritabani.db'
db = SQLAlchemy(uygulama)
uygulama.secret_key = "todo"
@uygulama.route("/")
def index():
    yapilacaklar_liste = ToDo.query.all() 
    return render_template("index.html",todos = yapilacaklar_liste)
@uygulama.route("/ekle", methods = ["POST"])
def ekle():
    baslik = request.form.get("title")
    deger = ToDo(title = baslik, complete = False)
    db.session.add(deger)
    db.session.commit()
    return redirect(url_for("index"))
@uygulama.route("/complete/<string:id>")
def complete(id):
    yapilacak = ToDo.query.filter_by(id = id).first()
    yapilacak.complete = not yapilacak.complete
    db.session.commit()
    return redirect(url_for("index"))
@uygulama.route("/delete/<string:id>")
def delete(id):
    silinecek = ToDo.query.filter_by(id = id).first()
    db.session.delete(silinecek)
    db.session.commit()
    return redirect(url_for("index"))

class ToDo(db.Model):
    #SQL Tablosundaki Alanlarımızı Class içine oluşturuyoruz...
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    db.create_all() #belirttiğimiz alanlar dahilinde veritabanımızı oluşturuyoruz. 
    uygulama.run(debug = True)

