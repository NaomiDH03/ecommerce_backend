from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#Mi clase Prodcuto con todos sus atributod
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True) #Entero
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.titulo,
            'precio': self.autor,
            'stock': self.editorial,
            'categoria': self.edicion
        }
    

#Mi clase orden con todos sus atributos
class Orden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(100), nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    total_productos = db.Column(db.Integer, nullable=False)
    items = db.relationship('OrdenProducto', backref='orden')
    tienda_id = db.Column(db.Integer, db.ForeignKey('tienda.id')) #Me faltava el id de la tienda por eso no jalaba

    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.titulo,
            'cliente': self.autor,
            'total_productos': self.editorial,
            'items': [item.to_dict() for item in self.items]
        }
    

#Mi clase orden producto que esta como para que tu puedas checar esa orden (o por lo menos asi lo pienso yo)
class OrdenProducto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('orden.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    producto = db.relationship('Producto')

    def to_dict(self):
        return {
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'producto': self.producto.to_dict()
        }
    

class Tienda(db.Model):
    id = db.Column(db.Integer, primary_key=True) #Entero
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.Float, nullable=False)
    items = db.relationship('Orden', backref='tienda') #Y aqui eata relacionado directamente con orden, no con orden producto 
    #Nota: estaba mal el bacred ya que teneia "orden" en lugar de "tienda" 

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'ubicacion': self.ubicacion,
            'items': [item.to_dict() for item in self.items]
        }