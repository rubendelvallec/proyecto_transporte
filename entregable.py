from enum import Enum
from typing import Dict
from typing import List
import threading
import time


class Paquete:
    def __init__(self, peso, destino):
        self.peso = peso #En kilogramos
        self.destino = destino
    
    def Precio(self):
        precio = self.peso*1,2
        return precio

class Pedido:
    def __init__(self, id, cliente, canalEntrada, modalidadEnvio, fechaPedido, viaje):
        self.id = id
        self.cliente = cliente
        self.canalEntrada = canalEntrada
        self.modalidadEnvio = modalidadEnvio
        self.fechaPedido = fechaPedido
        self.viaje = viaje

        self.Paquetes: Dict[Paquete, int] = dict()


    def AgregarPaquete(self, paquete):
        if paquete not in self.Paquetes:
            self.Paquetes[paquete] = 1
        else:
            self.Paquetes[paquete] += 1


    def Coste(self):
        costetotal = 0
        for paquete in self.Paquetes:
            costetotal += paquete.Precio()*self.Paquetes[paquete]

        return costetotal

    def PagarPedido(self):
        self.Paquetes.clear()
    
    def Peso(self):
        peso = 0
        for paquete in self.Paquetes:
            peso += paquete.peso
        return peso

class Vehiculo:
    def __init__(self, cargaMaxima, tipo, disponible):
        self.cargaMaxima = cargaMaxima
        self.tipo = tipo
        self.disponible = disponible #True si esta disponible, False si no

        self.vehiculosDisponibles: List[Vehiculo] = list()
    
    def añadirVehiculoDisp(self, vehiculo):
        if vehiculo.disponible:
            self.vehiculo

    




class Viaje:
    def __init__(self, id, km, vehiculo):
        self.id = id
        self.km = km
        
        self.listaPedidos: List[Pedido] = list()
    
    def IniciarViaje(self):

        self.vehiculo.disponible = False
    
    def FinViaje(self):



class Cliente:
    def __init__(self, id, km, Servicios):
        self.id = id
        self.km = km
        self.Servicios = Servicios
    
    def FacturacionMensual(self):


