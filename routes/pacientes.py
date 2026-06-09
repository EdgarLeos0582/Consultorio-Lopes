from flask import Blueprint, render_template, request, redirect, url_for
from database import db 

pacientes_bp= Blueprint('pacientes', __name__)
col= db['pacientes']

@pacientes_bp.route("/")
def ver_pacientes():
    lista = list(col.find({}, {'_id': 0}))
    return render_template('pacientes.html', pacientes=lista)

@pacientes_bp.route("/nuevo")
def formulario(): 
    return render_template('formulariopacientes.html', p=None)

@pacientes_bp.route("/guardar", methods=["POST"])
def guardar():
    id_existente = request.form.get("id_paciente")

    datos_paciente = {
        "edad":             request.form.get("edad"),
        "nombre":           request.form.get("nombre"),
        "apellido_paterno": request.form.get("apellido_paterno"),
        "apellido_materno": request.form.get("apellido_materno"),
        "tipo_sangre":      request.form.get("tipo_sangre"),
        "alergias":         request.form.get("alergias"),
        "genero":           request.form.get("genero"),
        "telefono":         request.form.get("telefono"),
    }

    if id_existente:
        col.update_one({"id_paciente": int(id_existente)}, {"$set": datos_paciente})
    else:
        ultimo = col.find_one({"id_paciente": {"$type": "int"}}, sort=[("id_paciente", -1)])
        nuevo_id = (ultimo["id_paciente"] + 1) if ultimo else 1
        datos_paciente["id_paciente"] = nuevo_id
        col.insert_one(datos_paciente)

    return redirect(url_for('pacientes.ver_pacientes'))

@pacientes_bp.route("/editar/<id_paciente>")
def editar(id_paciente):
    id_entero = int(id_paciente)
    paciente = col.find_one({"id_paciente": id_entero})
    return render_template('formulariopacientes.html', p=paciente)

@pacientes_bp.route("/eliminar/<id_paciente>", methods=["POST"])
def eliminar(id_paciente):
    id_entero = int(id_paciente)
    col.delete_one({"id_paciente": id_entero})
    return redirect(url_for('pacientes.ver_pacientes'))