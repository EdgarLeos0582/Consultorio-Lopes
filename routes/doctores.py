from flask import Blueprint, render_template, request, redirect, url_for
from database import db

doctores_bp = Blueprint('doctores_bp', __name__)
col = db['doctores']

@doctores_bp.route("/")
def ver_doctores():
    lista = list(col.find())
    return render_template('doctores.html', doctores=lista)

@doctores_bp.route("/nuevo")
def formulario():
    return render_template('formulariodoctores.html', d=None)

@doctores_bp.route("/guardar", methods=["POST"])
def guardar():
    id_existente = request.form.get("id_doctor")

    datos_doctor = {
        "especialidad":     request.form.get("especialidad"),
        "nombre":           request.form.get("nombre"),
        "apellido_paterno": request.form.get("apellido_paterno"),
        "apellido_materno": request.form.get("apellido_materno"),
        "cedula":           request.form.get("cedula"),
        "rfc":              request.form.get("rfc"),
        "horario":          request.form.get("horario"),
        "consultorio":      request.form.get("consultorio"),
        "sueldo":           request.form.get("sueldo"),
    }

    if id_existente:
        col.update_one({"id_doctor": int(id_existente)}, {"$set": datos_doctor})
    else:
        ultimo = col.find_one(sort=[("id_doctor", -1)])
        nuevo_id = (ultimo["id_doctor"] + 1) if ultimo else 1
        datos_doctor["id_doctor"] = nuevo_id
        col.insert_one(datos_doctor)

    return redirect(url_for('doctores_bp.ver_doctores'))

@doctores_bp.route("/eliminar/<id_doctor>", methods=["POST"])
def eliminar(id_doctor):
    id = int(id_doctor)
    col.delete_one({"id_doctor": id})
    return redirect(url_for('doctores_bp.ver_doctores'))

@doctores_bp.route("/editar/<id_doctor>")
def editar(id_doctor):
    id_entero = int(id_doctor)
    doctor = col.find_one({"id_doctor": id_entero})
    return render_template('formulariodoctores.html', d=doctor)