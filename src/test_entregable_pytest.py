import pytest
from entregable_final import Paquete, Pedido, Vehiculo, Furgoneta, Conductor, Viaje, Cliente

# Prueba para la clase Paquete
def test_precio_paquete():
    paquete = Paquete("Fresa", 5)
    assert paquete.Precio() == 6  # 5 kg * 1.2 = 6€

def test_str_paquete():
    paquete = Paquete("Fresa", 5)
    assert str(paquete) == "Paquete Fresa de peso 5 kg"

# Prueba para la clase Pedido
def test_coste_pedido():
    paquete1 = Paquete("Fresa", 5)
    paquete2 = Paquete("Chocolate", 10)
    pedido = Pedido("C001", "TEL", "Domicilio", 20, "Madrid")
    pedido.AgregarPaquete(paquete1)  # 1 vez
    pedido.AgregarPaquete(paquete2)  # 1 vez
    assert pedido.Coste() == (6 + 12) + (20 * 3) + 5.5  # 6 + 12 + 60 + 5.5 = 78.5€


def test_peso_pedido():
    paquete1 = Paquete("Fresa", 5)
    paquete2 = Paquete("Chocolate", 10)
    pedido = Pedido("C001", "TEL", "Express", 20, "Madrid")
    pedido.AgregarPaquete(paquete1)
    pedido.AgregarPaquete(paquete2)
    assert pedido.Peso() == 15  # Peso total de los paquetes

# Prueba para la clase Vehiculo
def test_vehiculo_disponible():
    vehiculo = Furgoneta(3000, "Ford Transit")
    assert vehiculo.UbicacionActual() == "El vehiculo Ford Transit no esta en reparto"
    vehiculo.disponible = False
    vehiculo.ubicacion = 1  # Simula que está en reparto
    assert vehiculo.UbicacionActual() == "El vehiculo Ford Transit esta en reparto"


# Prueba para la clase Cliente
def test_facturacion_cliente():
    cliente = Cliente("C001")
    paquete1 = Paquete("Fresa", 5)
    paquete2 = Paquete("Chocolate", 10)
    paquete3 = Paquete('Zumo', 3)
    paquete4 = Paquete('Agua', 20)
    cliente.HacerPedido([paquete1, paquete2], canalEntrada="TEL", modalidadEnvio="Express", km=20, destino="Madrid")
    cliente.HacerPedido([paquete3, paquete4], canalEntrada="TEL", modalidadEnvio="Domicilio", km=2, destino="Madrid")
    assert cliente.FacturaciónMesual() == "117.1 €"  # Verifica el coste correcto
