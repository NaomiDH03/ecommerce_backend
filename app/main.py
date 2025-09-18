from flask import Flask, jsonify, request
from models import Producto, Tienda, Orden, OrdenProducto, db #seed_productos


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    #seed_productos()

@app.route('/')
def hello():
    return 'Tienda de productos'


@app.get("/productos")
def get_productos():
    nombre = request.args.get("nombre")
    categoria = request.args.get("categoria")
    query = Producto.query

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = query.order_by(Producto.id).paginate(page=page, per_page=per_page)


    if nombre:
        query = query.filter(Producto.nombre.ilike(f"%{nombre}%"))
    if categoria:
        query = query.filter(Producto.categoria.ilike(f"%{categoria}%"))

    productos = [{
        "id": p.id,
        "nombre": p.nombre,
        "precio": p.precio,
        "stock": p.stock,
        "categoria": p.categoria
    } for p in pagination.items]

    return jsonify(productos)


#Trae un producto con id especifico
@app.get("/productos/<int:id>")
def get_libro(id):
    producto = Producto.query.get(id)
    if producto is None:
        return jsonify({"Error :("}), 404
    return jsonify({
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "stock": producto.stock,
        "categoria": producto.categoria
    }), 200

#Agrega producto
@app.post("/productos")
def add_producto():
    data = request.json
    if not data:
        return jsonify({"error": "Datos faltantes"}), 400
    nuevo = Producto(
        nombre=data.get('nombre'),
        precio=data.get('precio'),
        stock=data.get('stock'),
        categoria=data.get('categoria')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({
        "id": nuevo.id,
        "nombre": nuevo.nombre,
        "precio": nuevo.precio,
        "stock": nuevo.stock,
        "categoria": nuevo.categoria
    }), 201

#Para actualizar el producto
@app.put("/productos/<int:id>")
def update_producto(id):
    data = request.json
    producto = Producto.query.get(id)  
    if not producto:
        return jsonify({"Error :("}), 404
    producto.nombre = data.get("nombre", producto.nombre)
    producto.precio = data.get("precio", producto.precio)
    producto.stock = data.get("stock", producto.stock)
    producto.categoria = data.get("categoria", producto.categoria)
    db.session.commit()  #Actualizamos BD
    return jsonify({"mensaje": "Producto actualizado :)"}), 200

@app.delete("/productos/<int:id>")
def delete_producto(id):
    producto = Producto.query.get(id) 
    if producto is None:
        return jsonify({'error': f'Libro con id {id} no encontrado'}), 404
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"mensaje": "Producto eliminado :)"}), 200

#Para obtener la orden
@app.get("/ordenesproducto")
def get_ordenesproducto():
    ordenes_producto = OrdenProducto.query.all()
    resultado = [op.to_dict() for op in ordenes_producto]
    return jsonify(resultado), 200

@app.post("/orden")
def add_orden():
    data = request.json
    if not data:
        return jsonify({"error": "Datos faltantes"}), 400
    nuevo = Orden(
        fecha=data.get("fecha"),
        cliente=data.get("cliente"),
        total_productos=data.get("total_productos"),
        tienda_id=data.get("tienda_id")
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({
        "id": nuevo.id,
        "fecha": nuevo.fecha,
        "cliente": nuevo.cliente,
        "total_productos": nuevo.total_productos,
        "tienda_id": nuevo.tienda_id
    }), 201

if __name__ == '__main__':
    app.run(debug=True)