from enum import Enum
from typing import Dict
from typing import List
import threading
import time


class Paquete:
    def __init__(self, nombre, peso, destino):
        self.nombre = nombre
        self.peso = peso #En kilogramos
        self.destino = destino
    
    def Precio(self):
        precio = self.peso*1.2
        return precio
    
    def __str__(self):
        return f"Paquete de peso {self.peso} kg y destino {self.destino}"


class Pedido:
    def __init__(self, id, cliente, canalEntrada, modalidadEnvio, km):
        self.id = id
        self.cliente = cliente
        self.canalEntrada = canalEntrada
        self.modalidadEnvio = modalidadEnvio
        self.km = km
        self.viaje = None

        self.Paquetes: Dict[Paquete, int] = dict()
    
    def __str__(self):
        return f"Pedido {self.id} del cliente {self.cliente}, por {self.canalEntrada}, enviado"

    def AgregarPaquete(self, paquete):
        if paquete not in self.Paquetes:
            self.Paquetes[paquete] = 1
        else:
            self.Paquetes[paquete] += 1


    def Coste(self):
        costetotal = 0
        for paquete in self.Paquetes:
            costetotal += paquete.Precio()*self.Paquetes[paquete]
        
        return costetotal + self.km*3 #Cada km costaria 3 euros

    def PedidoEntregado(self):
        self.Paquetes.clear()
    
    def Peso(self):
        peso = 0
        for paquete in self.Paquetes:
            peso += paquete.peso
        return peso


class Vehiculo:
    def __init__(self, cargaMaxima, tipo):
        self.cargaMaxima = cargaMaxima
        self.tipo = tipo
        self.disponible = True #True si esta disponible, False si no
        self.ubicacion = -1

        Vehiculo.todos_los_vehiculos.append(self)

    @classmethod
    def VehiculosDisponibles(cls):
        return [vehiculo for vehiculo in cls.todos_los_vehiculos if vehiculo.disponible]
    

class Motorizado(Vehiculo):
  def __init__(self, cargaMaxima, tipo, combustible):
        super().__init__(cargaMaxima, tipo)
        self.combustible = combustible

class Ecologico(Vehiculo):
    def __init__(self, cargaMaxima, tipo):
        super().__init__(cargaMaxima, tipo)

# Vehículos específicos
class Furgoneta(Motorizado):
    def __init__(self, cargaMaxima):
        super().__init__(cargaMaxima, "Furgoneta", "Diesel")

class BicicletaElectrica(Motorizado, Ecologico):
    def __init__(self, cargaMaxima):
        Motorizado.__init__(self, cargaMaxima, "Bicicleta Eléctrica", "Batería")
        Ecologico.__init__(self, cargaMaxima, "Bicicleta Eléctrica")  


class Camion(Motorizado):
    def __init__(self, cargaMaxima):
        super().__init__(cargaMaxima, "Camion", "Gasolina")

class Bicicleta(Ecologico):
    def __init__(self, cargaMaxima):
        super().__init__(cargaMaxima, "Bicicleta")


class Viaje:
    def __init__(self, id, km):
        self.id = id
#        self.km = km
        self.vehiculo = None
        self.ParteViaje = None
        self.trabajadores: List[Trabajador] = list()
        self.pedidos: List[Pedido] = list()
        Viaje.todos_los_viajes.append(self)

    def UbicacionActual(self):
        if self.ubicacion == -1:
            return f'El vehiculo no esta en reparto'
        elif self.ubicacion == 0:
            return f'El vehiculo esta en reparto'
        else:
            return f'El vehiculo ha terminado el reparto'

    
    def AñadirPedido(self, pedido):
        peso = 0
        for pedido1 in self.pedidos:
            peso += pedido1.Peso()

        if peso + pedido.Peso() > 3500 :

            raise Exception(f"El viaje {self.id} esta completo, por favor busque otro viaje disponible")
            
        self.pedidos.append(pedido)
        pedido.viaje = self.id
        
    def SeleccionVehiculo(self):
        peso = 0
        for pedido in self.pedidos:
            peso += pedido.Peso()
        
        for vehiculo in Vehiculo.VehiculosDisponibles():
            if vehiculo.cargaMaxima >= peso:
                self.vehiculo = vehiculo
                vehiculo.disponible = False
                pass
    
    def SeleccionTrabajadores(self):
        for trabajador in Trabajador.TrabajadoresDisponibles():
            if len(self.trabajadores) == 0:
                self.trabajadores.append(trabajador)
                trabajador.disponible = False
            elif len(self.trabajadores) == 1:
                for contratado in self.trabajadores:
                    if isinstance(contratado, Mixto):
                        pass
                    elif isinstance(contratado, Ayudante) and (isinstance(trabajador, Mixto) or isinstance(trabajador, Conductor)):
                        self.trabajadores.append(trabajador)
                        trabajador.disponible = False
                    elif isinstance(contratado, Trabajador) and (isinstance(trabajador, Mixto) or isinstance(trabajador, Ayudante)):
                        self.trabajadores.append(trabajador)
                        trabajador.disponible = False
            else:
                pass

    def FinViaje(self):
        self.vehiculo.disponible = True
        self.vehiculo.ubicacion = 1

    def IniciarViaje(self):
        self.SeleccionVehiculo()
        self.SeleccionTrabajadores()
        self.vehiculo.disponible = False
        self.vehiculo.ubicacion = 0
    
        time.sleep(5)

        self.FinViaje()
        for pedido in self.pedidos:
            pedido.PedidoEntregado()
        self.ParteViaje.Cerrar()
    def MostrarParte(self):
        for i in self.ParteViaje:
            print(i)

class Cliente:
    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id
        self.listaPaquetes = []

    def HacerPedido(self, *paquetes, canalEntrada, modalidadEnvio, km):

        pedido = Pedido(self, len(self.listaPedidos), self.id, canalEntrada, modalidadEnvio, km)

        self.listaPedidos.append(pedido)

        for paquete in paquetes:
            pedido.AgregarPaquete(paquete)
        
        i = 0

        lista_viajes = Viaje.todos_los_viajes
        try:
            lista_viajes[i].AñadirPedido(pedido)
            viaje = lista_viajes[i]
        except Exception as e:
            i+=1
        
        viaje = lista_viajes[i]
        pedido.viaje = viaje

class canalEntrada(Enum):
    IMPRESOS = 1
    TELEFONO = 2
    FAX = 3



class Trabajador():
    def __init__(self, nombre, id, añosContrato):
        self.id = id
        self.nombre = nombre
        self.añosContrato = añosContrato
        self.disponible = True
    
        Trabajador.todos_los_trabajadores.append(self)

    def Disponibilidad(self):
        return self.disponible
    

    @classmethod
    def TrabajadoresDisponibles(cls):
        return [trabajador for trabajador in cls.todos_los_trabajadores if trabajador.disponible]


class Ayudante(Trabajador):
    def __init__(self, id, añosContrato):
        super().__init__(id, añosContrato)

    def IncidenciaViaje(self, viaje, incidencia_ocurrida, observacion):
        if viaje.ParteViaje == None:
            parte = ParteViaje()
            viaje.ParteViaje = parte

        viaje.ParteViaje.AgregarIncidencia(incidencia_ocurrida, observacion)


class Mixto(Trabajador):
    def __init__(self, id, añosContrato, listaPartes, añosConCarnet):
        super().__init__(id, añosContrato)
        self.añosConCarnet = añosConCarnet

    def IncidenciaViaje(self, viaje, incidencia_ocurrida, observacion):
        if viaje.ParteViaje == None:
            parte = ParteViaje()
            viaje.ParteViaje = parte

        viaje.ParteViaje.AgregarIncidencia(incidencia_ocurrida, observacion)


class Conductor(Trabajador):
    def __init__(self, id, añosContrato, añosConCarnet):
        super().__init__(id, añosContrato)
        self.añosConCarnet = añosConCarnet


class ParteViaje:
    def __init__(self, hora):
        self.viaje = None
        self.incidencias = dict()
        self.hora = hora
    
    def AgregarIncidencia(self, incidencia, observacion):
        self.incidencias[incidencia] = observacion
    
    def Cerrar(self):
        for contratado in self.viaje.trabajadores:
            if isinstance(contratado, Mixto) or isinstance(contratado, Ayudante):
                contratado.AñadirParte(self.incidencias)
        self.incidencias.clear()


if __name__ == "__main__":
    paquete1 = Paquete('latas', 20, 'Murcia')
    paquete2 = Paquete('Paco', 200, 'ibiza')
    paquetes = [paquete1,paquete2]
    cliente1 = Cliente('Jose', 123456789)
    cliente1.HacerPedido(paquetes, canalEntrada.FAX, 'domicilio', 24)