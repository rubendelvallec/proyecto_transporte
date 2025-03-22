from enum import Enum
from typing import Dict
from typing import List
import threading
import time


class Paquete:
    def __init__(self, nombre, peso):
        self.peso = peso #En kilogramos
        self.nombre = nombre
    
    def Precio(self):
        precio = int(self.peso)*1.2
        return precio
    
    def __str__(self):
        return f"Paquete {self.nombre} de peso {self.peso} kg"


class Pedido:
    def __init__(self, id, paquetes, canalEntrada, modalidadEnvio, km, destino):
        self.id = id
        self.paquetes = paquetes
        self.canalEntrada = canalEntrada
        self.modalidadEnvio = modalidadEnvio
        self.km = km
        self.destino = destino
        self.viaje = None

    
    def __str__(self):

        return f"Pedido {self.id} de cliente {self.paquetes}, con canal de entrada {self.canalEntrada}, por {self.modalidadEnvio}, a {self.destino} a {self.km} km añadidos al viaje {self.viaje}\n"


    def Coste(self):
        costetotal = 0
        for paquete in self.paquetes:

            costetotal += paquete.Precio()
        
        if self.modalidadEnvio ==  "Domicilio":
            costetotal += 5.5
        
        return costetotal + self.km*3 #Cada km costaria 3 euros
    
    def Peso(self):
        peso = 0
        for paquete in self.paquetes:
            peso += paquete.peso
        return peso


class Vehiculo:
    todos_los_vehiculos = []

    def __init__(self, cargaMaxima, modelo):
        self.cargaMaxima = cargaMaxima
        self.modelo = modelo
        self.disponible = True #True si esta disponible, False si no
        self.ubicacion = 0

        Vehiculo.todos_los_vehiculos.append(self)

    def UbicacionActual(self):
        if self.ubicacion == 0:
            return f"El vehiculo {self.modelo} no esta en reparto"
        else:
            return f"El vehiculo {self.modelo} esta en reparto"

    def __str__(self):
        return f"Vehiculo: {self.modelo} con cargaMaxima {self.cargaMaxima} kg"

    @classmethod
    def VehiculosDisponibles(cls):
        return [vehiculo for vehiculo in cls.todos_los_vehiculos if vehiculo.disponible]

class Ecologico(Vehiculo):
    def __init__(self, cargaMaxima, modelo):
        super().__init__(cargaMaxima, modelo)
    
    def __str__(self):
        return "Ecologico: " + super().__str__()

class Motorizado(Vehiculo):
    def __init__(self, cargaMaxima, modelo):
        super().__init__(cargaMaxima, modelo)

    def __str__(self):
        return "Motorizado: " + super().__str__()

class Furgoneta(Motorizado):
    def __init__(self, cargaMaxima, modelo):
        super().__init__(cargaMaxima, modelo)

    def _str_(self):
        return "Furgoneta: " + super().__str__()

class BicicletaElectrica(Motorizado, Ecologico):
    def __init__(self, cargaMaxima, modelo):
        super().__init__(cargaMaxima, modelo)

    def __str__(self):
        return "Bicicleta Electrica: " + super().__str__()

class Camion(Motorizado):
    def __init__(self, cargaMaxima, modelo):
        super().__init__(cargaMaxima, modelo)

    def __str__(self):
        return "Camion: " + super()._str_()

class Bicicleta(Ecologico):
    def __init__(self, cargaMaxima, modelo):
        super().__init__(cargaMaxima, modelo)

    def __str__(self):
        return "Bicicleta: " + super().__str__()
class Viaje:
    todos_los_viajes = []
    def __init__(self, id):
        self.id = id
        self.vehiculo = None
        self.ParteViaje = None
        
        self.trabajadores: List[Trabajador] = list()
        self.pedidos: List[Pedido] = list()
        Viaje.todos_los_viajes.append(self)

    def __str__(self):
        txt1 = "** Pedidos Añadidos **\n"
        for v in self.pedidos:
            txt1 += str(v) + "\n"

        txt2 = "** Trabajadores Añadidos **\n"
        for v in self.trabajadores:
            txt2 += str(v) + "\n"
        
        return f"Viaje {self.id} en el vehiculo {self.vehiculo} \n" + txt1 + txt2
    
    def AñadirPedido(self, pedido):
    
        peso_total = sum([p.Peso() for p in self.pedidos]) + pedido.Peso()
        if peso_total > 3500:  # Por ejemplo, no puede superar los 3500 kg
            raise Exception(f"El viaje {self.id} está completo, no puede añadir más pedidos.")
        self.pedidos.append(pedido)
        pedido.viaje = self.id
        
    def SeleccionVehiculo(self):
        peso = 0
        for pedido in self.pedidos:
            peso += pedido.Peso()
        
        for vehiculo in Vehiculo.VehiculosDisponibles():
            if vehiculo.cargaMaxima >= peso:
                self.vehiculo = vehiculo
                self.vehiculo.disponible = False
                break
    
    def SeleccionTrabajadores(self):
        if len(Mixto.MixtosDisponibles()) > 0:
            contratado = Mixto.MixtosDisponibles()[0] 
            self.trabajadores.append(contratado)
            contratado.viaje = self
            contratado.disponible = False
        else:
            self.trabajadores.append(Conductor.conductoresDisponibles()[0])
            Conductor.conductoresDisponibles()[0].viaje = self
            Conductor.conductoresDisponibles()[0].disponible = False
            self.trabajadores.append(Ayudante.AyudantesDisponibles()[0])
            Ayudante.AyudantesDisponibles()[0].viaje = self
            Ayudante.AyudantesDisponibles()[0].disponible = False

    def FinViaje(self):
        self.vehiculo.disponible = True
        for trabajador in self.trabajadores:
            trabajador.disponible = True
        self.vehiculo.ubicacion = 0

    def IniciarViaje(self):
        self.SeleccionVehiculo()
        self.SeleccionTrabajadores()
        self.vehiculo.disponible = False
        self.vehiculo.ubicacion = 1

    def VerParte(self):
        for i in self.ParteViaje.incidencias:
            print(f'Incidente : {i}, Observacion:{self.ParteViaje.incidencias[i]}')



class Cliente:
    def __init__(self, nombre, id):
        self.id = id
        self.nombre = nombre
        self.listaPedidos: List[Pedido] = list()
        self.paquetes = []
    
    def __str__(self):
        return f"Cliente {self.nombre} con dni {self.id} "

    def AñadirPaquetes(self, paquete):
        self.paquetes.append(paquete)

    def HacerPedido(self, pedido):
        # Crear un nuevo pedido
        self.listaPedidos.append(pedido)
        viaje_asignado = False
        for viaje in Viaje.todos_los_viajes:
            try:
                viaje.AñadirPedido(pedido)  # Añadir el pedido al viaje
                pedido.viaje = viaje.id  # Asociar el pedido con el viaje
                viaje_asignado = True
                break  # Salir del ciclo si el pedido fue agregado
            except Exception:
                continue  # Si el viaje está completo, probar con el siguiente viaje

        # Si no se asignó el pedido a ningún viaje, lanzar excepción
        if not viaje_asignado:
            print("No se pudo asignar el pedido a ningún viaje disponible.")
    
    def FacturaciónMesual(self):
        coste_total = 0
        for pedido in self.listaPedidos:
            coste_total += pedido.Coste()
        
        return str(coste_total) + " €"


class canalEntrada(Enum):
    IMPRESOS = 1
    TELEFONO = 2
    FAX = 3


class Trabajador():
    todos_los_trabajadores = []
    def __init__(self, id, añosContrato):
        self.id = id
        self.añosContrato = añosContrato
        self.disponible = True
        self.viaje = None
    
        Trabajador.todos_los_trabajadores.append(self)
    
    def __str__(self):
        return f"Trabajador {self.id} con {self.añosContrato} años contratado"

    def Disponibilidad(self):
        return self.disponible  

    @classmethod
    def TrabajadoresDisponibles(cls):
        return [trabajador for trabajador in cls.todos_los_trabajadores if trabajador.disponible]


class Ayudante(Trabajador):
    todos_los_ayudantes = list()
    def __init__(self, id, añosContrato):
        super().__init__(id, añosContrato)

        Ayudante.todos_los_ayudantes.append(self)

    def __str__(self):
        return "Ayudante: " + super().__str__() 
    
    @classmethod
    def AyudantesDisponibles(cls):
        return [ayudante for ayudante in cls.todos_los_ayudantes if ayudante.disponible]


    def IncidenciaViaje(self, incidencia_ocurrida, observacion):
        viaje = self.viaje
        if viaje.ParteViaje is None:  # Asegúrate de que ParteViaje no sea None
            parte = ParteViaje()
            viaje.ParteViaje = parte
            parte.viaje = viaje

        viaje.ParteViaje.AgregarIncidencia(incidencia_ocurrida, observacion)




class Mixto(Trabajador):
    todos_los_mixtos = list()
    def __init__(self, id, añosContrato, añosConCarnet):
        super().__init__(id, añosContrato)
        self.añosConCarnet = añosConCarnet

        Mixto.todos_los_mixtos.append(self)

    def __str__(self):
        return "Mixto:  "+ str(self.añosConCarnet) + super().__str__()

    def AñadirParte(self, parte):
        self.listaPartes.append(parte)
    
    @classmethod
    def MixtosDisponibles(cls):
        return [mixto for mixto in cls.todos_los_mixtos if mixto.disponible]
    
    def IncidenciaViaje(self, incidencia_ocurrida, observacion):
        viaje = self.viaje
        if viaje.ParteViaje is None:  # Asegúrate de que ParteViaje no sea None
            parte = ParteViaje()
            viaje.ParteViaje = parte
            parte.viaje = viaje

        viaje.ParteViaje.AgregarIncidencia(incidencia_ocurrida, observacion)



class Conductor(Trabajador):
    todos_los_conductores = list()
    def __init__(self, id, añosContrato, añosConCarnet):
        super().__init__(id, añosContrato)
        self.añosConCarnet = añosConCarnet

        Conductor.todos_los_conductores.append(self)

    def __str__(self):        
        return "Conductor: "+ f"con {str(self.añosConCarnet)} años con carnet " + super().__str__()

    @classmethod
    def conductoresDisponibles(cls):
        return [conductor for conductor in cls.todos_los_conductores if conductor.disponible]

class ParteViaje():
    def __init__(self):
        self.viaje = None
        self.incidencias = dict()
    
    def __str__(self):
        txt = "** Incidencias **\n"
        for v in self.incidencias.keys():
            txt += str(v) + " --> " + str(self.incidencias[v]) + "\n"

        return f"Parte de Viaja {self.viaje}" + txt
    
    def AgregarIncidencia(self, incidencia, observacion):
        self.incidencias[incidencia]=observacion

if __name__ == "__main__":
   # Crear algunos paquetes
    p1 = Paquete("Camisetas", 25)
    p2 = Paquete("Zapatos", 3)

# Crear un cliente
    cliente = Cliente("Carlos", 1)

# Añadir paquetes al cliente
    cliente.AñadirPaquetes(p1)
    cliente.AñadirPaquetes(p2)

    conductor = Conductor('520', 3, 20)
    ayudante = Ayudante('2920', 20)
    pedido = Pedido(cliente.id, cliente.paquetes, canalEntrada.FAX, 'domicilio', 20, 'Madrid')
# Hacer un pedido con el cliente
    cliente.HacerPedido(pedido)
# Crear vehículos
    v1 = Bicicleta(20, "Bici Verde")
    v2 = Camion(4000, "Camión Rojo")

# Crear un viaje
    viaje1 = Viaje(100)

# Iniciar el viaje
    viaje1.IniciarViaje()

# Mostrar información del viaje y los paquetes
    print("Viaje Iniciado")
    print(viaje1)
    print("Pedidos del viaje:")
    for pedido in viaje1.pedidos:
       print(pedido)

# Ver facturación mensual del cliente
    print("\nFacturación mensual del cliente:", cliente.FacturaciónMesual())

# Marcar incidencia en el viaje
    ayudante.IncidenciaViaje("Robo", "Faltan paquetes en destino")

    print(v1.UbicacionActual())

# Ver el parte del viaje
    print("\nParte del viaje:")
    viaje1.FinViaje()
    viaje1.VerParte()
