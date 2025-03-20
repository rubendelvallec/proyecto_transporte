from enum import Enum
from typing import Dict
from typing import List
import threading
import time


class Paquete:
    def __init__(self, peso, destino, precio):
        self.peso = peso
        self.destino = destino
        self.precio = precio

    
class Pedido:
    def __init__(self, id, cliente,canalEntrada, modalidadEnvio, km):
        self.id = id
        self.cliente = cliente
        self.canalEntrada = canalEntrada
        self.modalidadEnvio = modalidadEnvio
        self.paquetes = []
        self.km = km

    def AgregarPaquete(self, paquete):
        self.paquetes.append(paquete)

    def Distancia(self, paquete):
        distancia = 0
        for paquete in self.Paquetes:
            distancia += paquete.destino
        return distancia


    def Coste(self):
        costetotal = 0
        for paquete in self.Paquetes:
            costetotal += paquete.precio
        
        return costetotal
    
    def Peso(self):
        peso = 0
        for paquete in self.Paquetes:
            peso += paquete.peso
        return peso
    

class Vehiculo:
    def __init__(self, cargaMaxima):
        self.cargaMaxima = cargaMaxima
        self.disponibilidad = True
    
    def Usar(self):
        self.disponibilidad= False
    

class Motorizado(Vehiculo):
    def __init__(self, cargaMaxima, combustible):
        super().__init__(cargaMaxima)
        self.combustible = combustible

class Ecologico(Vehiculo):
    def __init__(self, cargaMaxima):
        super().__init__(cargaMaxima)

    

class Viaje:
    def __init__(self, id):
        self.id = id
        self.vehiculos = False
        self.ParteViaje = None
        self.pedidos = []
        self.trabajadores = []

    def AñadirVehiculos(self, vehiculo):
        if vehiculo.disponibilidad == False:
            raise ValueError(f'Este vehiculo no esta disponible para el viaje')
        else:
            self.vehiculos = vehiculo

    def AñadirPedidos(self, pedido):
        self.pedidos.append(pedido)  

    def SeleccionVehiculo(self):
        peso = 0
        for pedido in self.pedidos:
            peso += pedido.Peso()
        
        for vehiculo in self.vehiculos:  
            if vehiculo.cargaMaxima >= peso and vehiculo.disponibilidad:
                vehiculo.Usar()  
                self.vehiculo = vehiculo
                break  

    def FinViaje(self):
        self.vehiculo.disponibilidad == True  

    def IniciarViaje(self):
        self.SeleccionVehiculo()
        time.sleep(5)
        self.FinViaje()

    def Coste(self, pedido):
        preciototal= 0
        for i in self.pedidos:
            if pedido.modalidadEnvio == 'domicilio':
                preciototal += pedido.Coste() + 5.3
            else:
                preciototal += pedido.Coste()
            preciototal += pedido.Distancia()*0.2
        return preciototal
    
    def AgregarParte(self, parteviaje):
        self.ParteViaje = parteviaje

    def MostrarParte(self):
        if self.ParteViaje:
            for incidencia in self.ParteViaje.incidencias:
                print(incidencia)
        

class Cliente:
    def __init__(self, dni, Servicios):
        self.dni = dni
        self.Servicios = Servicios
        self.listaPaquetes = []
        self.listaPedidos = []
    
    def AgregarPaquetes(self, peso, destino, precio):
        paquete = Paquete(peso, destino, precio)
        self.listaPaquetes.append(paquete)

    def HacerPedido(self, dni,  paquetes, canalEntrada, modalidadEnvio, km):

        pedido = Pedido(dni,  paquetes, canalEntrada, modalidadEnvio, km)

        self.listaPedidos.append(pedido)

        for paquete in paquetes:
            pedido.AgregarPaquete(paquete)
        
class Trabajador:
    def __init__(self, id, añosContrato):
        self.id = id
        self.añosContrato = añosContrato
        self.disponibilidad = True


    def Disponibilidad(self):
        self.disponibilidad = False

class Ayudante(Trabajador):
    def __init__(self, id, añosContrato):
        super().__init__(id, añosContrato)


    def AgregarIncidencias(self, viaje,contenido, fecha):
        parte = ParteViaje(self,fecha)
        parte.incidencias.append(contenido)
        viaje.AgregarParte(parte)
    
class Conductor(Trabajador):
    def __init__(self, id, añosContrato, añosCarnet):
        super().__init__(id, añosContrato)
        self.añosCarnet = añosCarnet


class Mixto(Trabajador):
    def __init__(self, id, añosContrato,  añosCarnet):
        super().__init__(id, añosContrato)
        self.añosCarnet = añosCarnet

    def AgregarIncidencias(self,viaje,contenido, fecha):
        parte = ParteViaje(self,fecha)
        parte.incidencias.append(contenido)
        viaje.AgregarParte(parte)


class ParteViaje:
    def __init__(self, fecha):
        self.fecha = fecha
        self.incidencias = []
    def AgregarIncidencias(self,contenido):
        self.incidencias.append(contenido)
            
class canalEntrada(Enum):
    IMPRESOS = 1
    TELEFONO = 2
    FAX = 3


class tipoVehiculo(Enum):
    CAMION = 1
    FURGONETA = 2
    BICICLETAE = 3
    BICICLETAM = 4

