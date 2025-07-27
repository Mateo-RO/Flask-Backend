from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

# =============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# =============================================================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Matreo1901",
    database="Listas_3"
)
cursor = db.cursor(dictionary=True)

# =============================================================================
# CONFIGURACIÓN DEL FLASK Y CORS
# =============================================================================

app = Flask(__name__)

CORS(app, 
     origins=["http://localhost:3000"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Accept"],
     supports_credentials=True
)

# =============================================================================
# INICIO
# =============================================================================

@app.route('/', methods=['GET'])
def home():
    return jsonify({"mensaje": "Bienvenido a la API de Mateo"})

# =============================================================================
# ENDPOINTS PARA USUARIOS
# =============================================================================

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        user_id = request.args.get('id')
        if user_id:
            cursor.execute("SELECT * FROM Usuarios WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                return jsonify(user)
            return jsonify({"error": "Usuario no encontrado"}), 404
        else:
            cursor.execute("SELECT * FROM Usuarios")
            resultados = cursor.fetchall()
            return jsonify(resultados)
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['nombre', 'email', 'contraseña']):
            return jsonify({"error": "Faltan campos requeridos: nombre, email, contraseña"}), 400
        
        cursor.execute(
            "INSERT INTO Usuarios (nombre, email, contraseña) VALUES (%s, %s, %s)",
            (data['nombre'], data['email'], data['contraseña'])
        )
        db.commit()
        
        new_user_id = cursor.lastrowid
        return jsonify({
            "mensaje": "Usuario creado exitosamente",
            "id": new_user_id
        }), 201
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['nombre', 'email', 'contraseña']):
            return jsonify({"error": "Faltan campos requeridos: nombre, email, contraseña"}), 400
        
        cursor.execute(
            "UPDATE Usuarios SET nombre = %s, email = %s, contraseña = %s WHERE id = %s",
            (data['nombre'], data['email'], data['contraseña'], id)
        )
        db.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404
            
        return jsonify({"mensaje": f"Usuario con ID {id} actualizado exitosamente"})
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        cursor.execute("DELETE FROM Usuarios WHERE id = %s", (id,))
        db.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404
            
        return jsonify({"mensaje": f"Usuario con ID {id} eliminado exitosamente"})
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

# =============================================================================
# ENDPOINTS PARA PROYECTOS
# =============================================================================

@app.route('/proyectos', methods=['GET'])
def obtener_proyectos():
    try:
        proyecto_id = request.args.get('id')
        if proyecto_id:
            cursor.execute("SELECT * FROM Proyectos WHERE id = %s", (proyecto_id,))
            proyecto = cursor.fetchone()
            if proyecto:
                return jsonify(proyecto)
            return jsonify({"error": "Proyecto no encontrado"}), 404
        else:
            cursor.execute("SELECT * FROM Proyectos")
            resultados = cursor.fetchall()
            return jsonify(resultados)
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/proyectos', methods=['POST'])
def crear_proyecto():
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['user_id', 'nombre', 'descripcion']):
            return jsonify({"error": "Faltan campos requeridos: user_id, nombre, descripcion"}), 400
        
        cursor.execute(
            "INSERT INTO Proyectos (user_id, nombre, descripcion) VALUES (%s, %s, %s)",
            (data['user_id'], data['nombre'], data['descripcion'])
        )
        db.commit()
        
        new_project_id = cursor.lastrowid
        return jsonify({
            "mensaje": "Proyecto creado exitosamente",
            "id": new_project_id
        }), 201
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/proyectos/<int:id>', methods=['PUT'])
def actualizar_proyecto(id):
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['user_id', 'nombre', 'descripcion']):
            return jsonify({"error": "Faltan campos requeridos: user_id, nombre, descripcion"}), 400
        
        cursor.execute(
            "UPDATE Proyectos SET user_id = %s, nombre = %s, descripcion = %s WHERE id = %s",
            (data['user_id'], data['nombre'], data['descripcion'], id)
        )
        db.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Proyecto no encontrado"}), 404
            
        return jsonify({"mensaje": f"Proyecto con ID {id} actualizado exitosamente"})
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/proyectos/<int:id>', methods=['DELETE'])
def eliminar_proyecto(id):
    try:
        cursor.execute("DELETE FROM Proyectos WHERE id = %s", (id,))
        db.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Proyecto no encontrado"}), 404
            
        return jsonify({"mensaje": f"Proyecto con ID {id} eliminado exitosamente"})
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

# =============================================================================
# ENDPOINTS PARA LISTAS
# =============================================================================

@app.route('/listas', methods=['GET'])
def obtener_listas():
    try:
        lista_id = request.args.get('id')
        if lista_id:
            cursor.execute("SELECT * FROM Listas WHERE id = %s", (lista_id,))
            lista = cursor.fetchone()
            if lista:
                return jsonify(lista)
            return jsonify({"error": "Lista no encontrada"}), 404
        else:
            cursor.execute("SELECT * FROM Listas")
            resultados = cursor.fetchall()
            return jsonify(resultados)
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/listas', methods=['POST'])
def crear_lista():
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['proyectos_id', 'nombre']):
            return jsonify({"error": "Faltan campos requeridos: proyectos_id, nombre"}), 400
        
        cursor.execute(
            "INSERT INTO Listas (proyectos_id, nombre) VALUES (%s, %s)",
            (data['proyectos_id'], data['nombre'])
        )
        db.commit()
        
        new_list_id = cursor.lastrowid
        return jsonify({
            "mensaje": "Lista creada exitosamente",
            "id": new_list_id
        }), 201
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/listas/<int:id>', methods=['PUT'])
def actualizar_lista(id):
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['proyectos_id', 'nombre']):
            return jsonify({"error": "Faltan campos requeridos: proyectos_id, nombre"}), 400
        
        cursor.execute(
            "UPDATE Listas SET proyectos_id = %s, nombre = %s WHERE id = %s",
            (data['proyectos_id'], data['nombre'], id)
        )
        db.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Lista no encontrada"}), 404
            
        return jsonify({"mensaje": f"Lista con ID {id} actualizada exitosamente"})
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/listas/<int:id>', methods=['DELETE'])
def eliminar_lista(id):
    try:
        cursor.execute("DELETE FROM Listas WHERE id = %s", (id,))
        db.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Lista no encontrada"}), 404
            
        return jsonify({"mensaje": f"Lista con ID {id} eliminada exitosamente"})
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/listas/<int:lista_id>/tareas', methods=['GET'])
def obtener_tareas_por_lista(lista_id):
    try:
        cursor.execute("SELECT * FROM Tareas WHERE lista_id = %s", (lista_id,))
        tareas = cursor.fetchall()
        return jsonify(tareas)
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

# =============================================================================
# ENDPOINTS PARA TAREAS
# =============================================================================

@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    try:
        tarea_id = request.args.get('id')
        if tarea_id:
            cursor.execute("SELECT * FROM Tareas WHERE id = %s", (tarea_id,))
            tarea = cursor.fetchone()
            if tarea:
                return jsonify(tarea)
            return jsonify({"error": "Tarea no encontrada"}), 404
        else:
            cursor.execute("SELECT * FROM Tareas")
            resultados = cursor.fetchall()
            return jsonify(resultados)
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/tareas', methods=['POST'])
def crear_tarea():
    try:
        data = request.get_json()
        
        
        if not data or 'lista_id' not in data or 'nombre' not in data:
            return jsonify({"error": "Faltan campos requeridos: lista_id, nombre"}), 400
        
        lista_id = data['lista_id']
        nombre = data['nombre']
        descripcion = data.get('descripción', None)  
        completada = data.get('completada', False)   
        vencimiento = data.get('vencimiento', None)  
        
        cursor.execute(
            "INSERT INTO Tareas (lista_id, nombre, descripción, completada, vencimiento) VALUES (%s, %s, %s, %s, %s)",
            (lista_id, nombre, descripcion, completada, vencimiento)
        )
        db.commit()
        
        new_task_id = cursor.lastrowid
        return jsonify({
            "mensaje": "Tarea creada exitosamente",
            "id": new_task_id
        }), 201
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        campos = []
        valores = []
        
        if 'lista_id' in data:
            campos.append("lista_id = %s")
            valores.append(data['lista_id'])
        if 'nombre' in data:
            campos.append("nombre = %s")
            valores.append(data['nombre'])
        if 'descripción' in data:
            campos.append("descripción = %s")
            valores.append(data['descripción'])
        if 'completada' in data:
            campos.append("completada = %s")
            valores.append(data['completada'])
        if 'vencimiento' in data:
            campos.append("vencimiento = %s")
            valores.append(data['vencimiento'])
        
        if not campos:
            return jsonify({"error": "No se proporcionaron campos para actualizar"}), 400
        
        valores.append(id)  
        
        query = f"UPDATE Tareas SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(query, valores)
        db.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Tarea no encontrada"}), 404
            
        return jsonify({"mensaje": f"Tarea con ID {id} actualizada exitosamente"})
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@app.route('/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    try:
        cursor.execute("DELETE FROM Tareas WHERE id = %s", (id,))
        db.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Tarea no encontrada"}), 404
            
        return jsonify({"mensaje": f"Tarea con ID {id} eliminada exitosamente"})
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

# =============================================================================
# INICIALIZACIÓN DEL SERVIDOR
# =============================================================================

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')