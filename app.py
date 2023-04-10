#Primera flag de la app aparentemente corregida
from flask import Flask 
from flask import render_template,request,redirect,url_for, flash, jsonify
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os
import time
import json


app = Flask(__name__)
app.secret_key="Jorge"

mysql = MySQL()

#Declaramos el uso de mysql pasando los parámetros de
#nuestra base de datos
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='fabrica'

#Creamos la conección con esos datos
mysql.init_app(app)


CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

lista_id_ing_perten_receta_obt=[]
lista_cant_ing_nec_pert_id_obt=[]
lista_cant_ing_nec_almacen_id_obt=[]
lista_cant_ing_nec_mult_cantobt=[]
lista_cant_ing_finales_almacen =[]
lista_nom_ing_nec_pert_id_obt=[]


@app.route('/uploads/<nombreImagen>')
def uploads(nombreImagen):
    return send_from_directory(app.config['CARPETA'],nombreImagen)

#Hasta esta parte nos sirve para varias

@app.route('/')
def index():
    
    sql ="SELECT * FROM `almacen`;"
    conn = mysql.connect()
    #Lugar donde almacenamos todo lo que vamos a ejecutar
    cursor=conn.cursor()
    cursor.execute(sql)
    
    #Selecicona todos los registros y muéstrame esos registros
    ingredientes=cursor.fetchall()
    print(ingredientes)
    
    #La instrucción se terminó
    conn.commit()
    
    
    
    sql2 ="SELECT * FROM `formulas`;"
    conn2 = mysql.connect()
    #Lugar donde almacenamos todo lo que vamos a ejecutar
    cursor2=conn2.cursor()
    cursor2.execute(sql2)
    
    #Selecicona todos los registros y muéstrame esos registros
    formulas=cursor2.fetchall()
    print(formulas)
    
    #La instrucción se terminó
    conn2.commit()


    sql3 ="SELECT * FROM `formula_ing`;"
    conn3 = mysql.connect()
    #Lugar donde almacenamos todo lo que vamos a ejecutar
    cursor3=conn3.cursor()
    cursor3.execute(sql3)
    
    #Selecicona todos los registros y muéstrame esos registros
    relaciones=cursor3.fetchall()
    print(relaciones)
    
    #La instrucción se terminó
    conn3.commit()
    
    
    
    return render_template('fabrica/index.html', ingredientes=ingredientes, formulas=formulas, relaciones=relaciones)

@app.route('/obtenerid')
def obtenerid(_recetaob):
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT nombre_form FROM formulas WHERE id_form=%s", _recetaob)
    recetasobt=cursor.fetchall()
    conn.commit()
    print(recetasobt)





@app.route('/destroy/<int:id_ing>')
def destroy(id_ing):
    conn = mysql.connect()
    cursor=conn.cursor()
    
    cursor.execute("SELECT imagen_ing FROM almacen WHERE id_ing=%s", id_ing)
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
    
    cursor.execute("DELETE FROM almacen WHERE id_ing=%s",(id_ing))
    conn.commit()
    return redirect('/')

@app.route('/destroy2/<int:id_form>')
def destroy2(id_form):
    conn2 = mysql.connect()
    cursor2=conn2.cursor()
    
    cursor2.execute("SELECT imagen_form FROM formulas WHERE id_form=%s", id_form)
    fila2=cursor2.fetchall()
    os.remove(os.path.join(app.config['CARPETA'],fila2[0][0]))
    
    cursor2.execute("DELETE FROM formulas WHERE id_form=%s",(id_form))
    conn2.commit()
    return redirect('/')

@app.route('/destroy3/<int:id_rel>')
def destroy3(id_rel):
    conn3 = mysql.connect()
    cursor3=conn3.cursor()
    
    cursor3.execute("DELETE FROM formula_ing WHERE id_rel=%s",(id_rel))
    conn3.commit()
    return redirect('/')





@app.route('/edit/<int:id_ing>')
def edit(id_ing):
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM almacen WHERE id_ing=%s", (id_ing))
    ingredientes=cursor.fetchall()
    conn.commit()
    
    return render_template('fabrica/edit.html',ingredientes=ingredientes)

#Aquí se tendría que crear un edit 2

@app.route('/edit2/<int:id_form>')
def edit2(id_form):
    conn2 = mysql.connect()
    cursor2=conn2.cursor()
    cursor2.execute("SELECT * FROM formulas WHERE id_form=%s", (id_form))
    formulas=cursor2.fetchall()
    conn2.commit()
    
    return render_template('fabrica/edit2.html',formulas=formulas)

@app.route('/edit3/<int:id_rel>')
def edit3(id_rel):
    conn3 = mysql.connect()
    cursor3=conn3.cursor()
    cursor3.execute("SELECT * FROM formula_ing WHERE id_rel=%s", (id_rel))
    relaciones=cursor3.fetchall()
    conn3.commit()
    
    return render_template('fabrica/edit3.html',relaciones=relaciones)
    
    
    
@app.route('/update', methods=['POST'])
def update():
    _nombre_ing=request.form['txtNombre']
    _cantidad_ing=request.form['txtCantidad']
    _imagen_ing=request.files['txtImagen']
    id_ing=request.form['txtID']
    
    sql ="UPDATE almacen SET nombre_ing=%s, cantidad_ing=%s WHERE id_ing=%s;"
    
    datos=(_nombre_ing,_cantidad_ing,id_ing)
    
    
    conn = mysql.connect()
    cursor=conn.cursor()

    #Para el formato de foto
    now = datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    
    if _imagen_ing.filename!='':
        
        nuevoNombreImagen=tiempo+_imagen_ing.filename
        _imagen_ing.save("uploads/"+nuevoNombreImagen)
        
        cursor.execute("SELECT imagen_ing FROM almacen WHERE id_ing=%s", id_ing)
        fila=cursor.fetchall()
        
        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE almacen SET imagen_ing=%s WHERE id_ing=%s",(nuevoNombreImagen,id_ing))
        conn.commit()
    
    
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')


@app.route('/update2', methods=['POST'])
def update2():
    _nombre_form=request.form['txtNombreForm']
    _cantidad_ing_form=request.form['txtCantidadForm']
    _imagen_form=request.files['txtImagenForm']
    id_form=request.form['txtIDForm']
    
    sql2 ="UPDATE formulas SET nombre_form=%s, cantidad_ing=%s WHERE id_form=%s;"
    
    datos2=(_nombre_form,_cantidad_ing_form,id_form)
    
    
    conn2 = mysql.connect()
    cursor2=conn2.cursor()

    #Para el formato de foto
    now2 = datetime.now()
    tiempo2=now2.strftime("%Y%H%M%S")
    
    if _imagen_form.filename!='':
        
        nuevoNombreImagen2=tiempo2+_imagen_form.filename
        _imagen_form.save("uploads/"+nuevoNombreImagen2)
        
        cursor2.execute("SELECT imagen_form FROM formulas WHERE id_form=%s", id_form)
        fila2=cursor2.fetchall()
        
        os.remove(os.path.join(app.config['CARPETA'],fila2[0][0]))
        cursor2.execute("UPDATE formulas SET imagen_form=%s WHERE id_form=%s",(nuevoNombreImagen2,id_form))
        conn2.commit()
    
    
    cursor2.execute(sql2,datos2)
    conn2.commit()
    return redirect('/')

@app.route('/update3', methods=['POST'])
def update3():
    _id_form_rel=request.form['txtIdFormRel']
    _id_ing_rel=request.form['txtIdIngRel']
    _cantidad_ing_rel=request.form['txtCantIngRel']
    
    id_rel=request.form['txtIDRel']
    
    sql3 ="UPDATE formula_ing SET id_form_rel=%s, id_ing_rel=%s, cantidad_ing_rel=%s WHERE id_rel=%s;"
    
    datos3=(_id_form_rel, _id_ing_rel,_cantidad_ing_rel,id_rel)
    
    
    conn3 = mysql.connect()
    cursor3=conn3.cursor()


    
    cursor3.execute(sql3,datos3)
    conn3.commit()
    return redirect('/')




@app.route('/form1', methods=['POST'])
def form1():
    global _recetaob
    global _cantob
    _recetaob=request.form['txtCreaReceta']
    _recetaob=_recetaob
    _cantob=request.form['txtCantGaFab']
    _cantob=int(_cantob)
    
    
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT id_form FROM formulas WHERE nombre_form=%s", _recetaob)
    id_receta_obt=cursor.fetchall()
    print("ID DE LA RECETA OBTENIDA:")
    print(id_receta_obt[0][0])
    conn.commit()
    
    conn2 = mysql.connect()
    cursor2=conn2.cursor()
    cursor2.execute("SELECT id_ing_rel FROM formula_ing WHERE id_form_rel=%s", id_receta_obt[0][0])
    id_ing_perten_receta_obt=cursor2.fetchall()
    print("ID DE LOS INGREDIENTES PERTENECIENTES A LA RECETA OBTENIDA EN UNA TUPLA:")
    print(id_ing_perten_receta_obt)
    conn2.commit()
    
    global lista_id_ing_perten_receta_obt
    lista_id_ing_perten_receta_obt.clear()
    
    for dato in id_ing_perten_receta_obt:
        lista_id_ing_perten_receta_obt.append(dato[0])
     
    print("ID DE LOS INGREDIENTES PERTENECIENTES A LA RECETA OBTENIDA EN UNA LISTA")   
    print(lista_id_ing_perten_receta_obt)


    conn3 = mysql.connect()
    cursor3=conn3.cursor()
    
    global lista_cant_ing_nec_pert_id_obt
    lista_cant_ing_nec_pert_id_obt.clear()
    
    a=0
    for i in lista_id_ing_perten_receta_obt:
        cursor3.execute("SELECT cantidad_ing_rel FROM formula_ing WHERE id_ing_rel=%s", lista_id_ing_perten_receta_obt[a])
        cant_ing_nec_pert_id_obt=cursor3.fetchall()
        lista_cant_ing_nec_pert_id_obt.append(cant_ing_nec_pert_id_obt[0][0])
        a=a+1
    
    print("CANTIDAD DE INGREDIENTES NECESARIOS PERTENECIENTES A LOS ID OBTENIDOS:")
    print(lista_cant_ing_nec_pert_id_obt)
    
    global lista_cant_ing_nec_mult_cantobt
    lista_cant_ing_nec_mult_cantobt.clear()
    lista_cant_ing_nec_mult_cantobt = [x * _cantob for x in lista_cant_ing_nec_pert_id_obt]
    
    print("CANTIDAD DE INGREDIENTES NECESARIOS (MULTIPLICADO POR LA CANTIDAD DE GALLETAS OBTENIDAS POR EL FORMS)")
    print(lista_cant_ing_nec_mult_cantobt)
    conn3.commit()
    
    
    conn4 = mysql.connect()
    cursor4=conn4.cursor()
    
    global lista_nom_ing_nec_pert_id_obt
    lista_nom_ing_nec_pert_id_obt.clear()
    
    
    b=0
    for i in lista_id_ing_perten_receta_obt:
        cursor4.execute("SELECT nombre_ing FROM almacen WHERE id_ing=%s", lista_id_ing_perten_receta_obt[b])
        nom_ing_nec_pert_id_obt=cursor4.fetchall()
        lista_nom_ing_nec_pert_id_obt.append(nom_ing_nec_pert_id_obt[0][0])
        b=b+1
    
    
    print("NOMBRE DE LOS INGREDIENTES DISPONIBLES EN ALMACEN PERTENECIENTES A LOS ID OBTENIDOS:")
    print(lista_nom_ing_nec_pert_id_obt)
        
    conn4.commit()
    
    
    
    conn5 = mysql.connect()
    cursor5=conn5.cursor()
    
    global lista_cant_ing_nec_almacen_id_obt
    lista_cant_ing_nec_almacen_id_obt.clear()
    
    
    
    b=0
    for i in lista_id_ing_perten_receta_obt:
        cursor5.execute("SELECT cantidad_ing FROM almacen WHERE id_ing=%s", lista_id_ing_perten_receta_obt[b])
        cant_ing_nec_almacen_id_obt=cursor5.fetchall()
        lista_cant_ing_nec_almacen_id_obt.append(cant_ing_nec_almacen_id_obt[0][0])
        b=b+1
    
    
    print("CANTIDAD DE INGREDIENTES DISPONIBLES EN ALMACEN PERTENECIENTES A LOS ID OBTENIDOS:")
    print(lista_cant_ing_nec_almacen_id_obt)
        
    conn5.commit()
    
    
    conn6 = mysql.connect()
    cursor6=conn6.cursor()
    
    global lista_cant_ing_finales_almacen
    lista_cant_ing_finales_almacen.clear()
    
    for i in range(len(lista_cant_ing_nec_almacen_id_obt)):
        resta = lista_cant_ing_nec_almacen_id_obt[i] - lista_cant_ing_nec_mult_cantobt[i]
        lista_cant_ing_finales_almacen.append(resta)
        
    print("CANTIDAD DE INGREDIENTES RESULTANTES EN ALMACEN LUEGO DE PREPARAR GALLETAS:")
    print(lista_cant_ing_finales_almacen)
    
    hay_negativos = any(numero < 0 for numero in lista_cant_ing_finales_almacen)
    if hay_negativos:
        print("NO HAY SUFICIENTES INGREDIENTES PARA PREPARAR LAS GALLETAS")
        return redirect('/ingredientes_insuficientes')

        
    else:
        a=0
        for i in lista_id_ing_perten_receta_obt:
            cursor6.execute(f"UPDATE almacen SET cantidad_ing={lista_cant_ing_finales_almacen[a]} WHERE id_ing={lista_id_ing_perten_receta_obt[a]}")
            a=a+1

        
        conn6.commit()
    
    
        return redirect('/ing_listos_amasado')
    
    
    
    




@app.route('/create')
def create():
    return render_template('fabrica/create.html')

#Aquí se tendría que crear un create2
@app.route('/create2')
def create2():
    return render_template('fabrica/create2.html')

@app.route('/create3')
def create3():
    return render_template('fabrica/create3.html')
    
    
@app.route('/store', methods=['POST'])
def storage():
    _nombre_ing=request.form['txtNombre']
    _cantidad_ing=request.form['txtCantidad']
    _imagen_ing=request.files['txtImagen']
    
    if _nombre_ing=='' or _cantidad_ing=='' or _imagen_ing=='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('create'))
    
    
    #Para el formato de foto
    now = datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    
    if _imagen_ing.filename!='':
        nuevoNombreImagen=tiempo+_imagen_ing.filename
        _imagen_ing.save("uploads/"+nuevoNombreImagen)
        
        
    sql ="INSERT INTO `almacen` (`id_ing`, `nombre_ing`, `cantidad_ing`, `imagen_ing`) VALUES (NULL,%s,%s,%s);"
    
    datos=(_nombre_ing,_cantidad_ing,nuevoNombreImagen)
    
    
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('/')


@app.route('/store2', methods=['POST'])
def storage2():
    _nombre_form=request.form['txtNombreForm']
    _cantidad_ing_form=request.form['txtCantidadForm']
    _imagen_form=request.files['txtImagenForm']
    
    if _nombre_form=='' or _cantidad_ing_form=='' or _imagen_form=='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('create2'))
    
    
    #Para el formato de foto
    now2 = datetime.now()
    tiempo2=now2.strftime("%Y%H%M%S")
    
    if _imagen_form.filename!='':
        nuevoNombreImagen2=tiempo2+_imagen_form.filename
        _imagen_form.save("uploads/"+nuevoNombreImagen2)
        
        
    sql2 ="INSERT INTO `formulas` (`id_form`, `nombre_form`, `cantidad_ing`, `imagen_form`) VALUES (NULL,%s,%s,%s);"
    
    datos2=(_nombre_form,_cantidad_ing_form,nuevoNombreImagen2)
    
    
    conn2 = mysql.connect()
    cursor2=conn2.cursor()
    cursor2.execute(sql2,datos2)
    conn2.commit()
    
    return redirect('/')


@app.route('/store3', methods=['POST'])
def storage3():
    _idformrel=request.form['txtIdFormRel']
    _idingrel=request.form['txtIdIngRel']
    _cantrel=request.form['txtCantRel']
    
    if _idformrel=='' or _idingrel=='' or _cantrel=='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('create3'))
    
        
    sql3 ="INSERT INTO `formula_ing` (`id_rel`, `id_form_rel`, `id_ing_rel`, `cantidad_ing_rel`) VALUES (NULL,%s,%s,%s);"
    
    datos3=(_idformrel,_idingrel,_cantrel)
    
    
    conn3 = mysql.connect()
    cursor3=conn3.cursor()
    cursor3.execute(sql3,datos3)
    conn3.commit()
    
    return redirect('/')

@app.route('/fabricacion_front')
def fabricacion_front():
    return render_template('fabrica/fabricacion_front.html')


@app.route('/ing_listos_amasado')
def ing_listos_amasado():
    global _recetaob
    global _cantob
    return render_template('fabrica/ing_listos_amasado.html',_recetaob=_recetaob,_cantob=_cantob)


@app.route('/horneando_galletas')
def horneando_galletas():
    return render_template('fabrica/horneando_galletas.html')

@app.route('/moldeando_transportando')
def moldeando_transportando():
    return render_template('fabrica/moldeando_transportando.html')

@app.route('/recibiendo_galletas')
def recibiendo_galletas():
    return render_template('fabrica/recibiendo_galletas.html')

@app.route('/galletas_listas_final')
def galletas_listas_final():
    global lista_id_ing_perten_receta_obt
    global lista_cant_ing_nec_mult_cantobt
    global lista_cant_ing_nec_almacen_id_obt
    global lista_nom_ing_nec_pert_id_obt
    global lista_cant_ing_finales_almacen
    global _recetaob
    global _cantob
    print(_recetaob)
    print(_cantob)
    return render_template('fabrica/galletas_listas_final.html',lista_id_ing_perten_receta_obt=lista_id_ing_perten_receta_obt, lista_cant_ing_nec_mult_cantobt=lista_cant_ing_nec_mult_cantobt,lista_cant_ing_nec_almacen_id_obt=lista_cant_ing_nec_almacen_id_obt,lista_nom_ing_nec_pert_id_obt=lista_nom_ing_nec_pert_id_obt,_recetaob=_recetaob,_cantob=_cantob,lista_cant_ing_finales_almacen=lista_cant_ing_finales_almacen)

@app.route('/ingredientes_insuficientes')
def ingredientes_insuficientes():
    global lista_id_ing_perten_receta_obt
    global lista_cant_ing_nec_mult_cantobt
    global lista_cant_ing_nec_almacen_id_obt
    global lista_nom_ing_nec_pert_id_obt
    
    return render_template('fabrica/ingredientes_insuficientes.html', lista_id_ing_perten_receta_obt=lista_id_ing_perten_receta_obt, lista_cant_ing_nec_mult_cantobt=lista_cant_ing_nec_mult_cantobt,lista_cant_ing_nec_almacen_id_obt=lista_cant_ing_nec_almacen_id_obt,lista_nom_ing_nec_pert_id_obt=lista_nom_ing_nec_pert_id_obt,)


if __name__=='__main__':
    app.run(debug=True)