from enum import Enum
from typing import Dict
from typing import List
import threading
import time


class Paquete:
     
    def __init__(self, nombre, peso):
        self.peso = peso #En kilogramos
        self.nombre = nombre
    
    def Precio(self): # Calcula el precio respecto del peso, usando un indice de 1,2 euros por kilo usado
        precio = int(self.peso)*1.2
        return precio
    
    def __str__(self):
        return f"Paquete {self.nombre} de peso {self.peso} kg"


class Pedido:
    def __init__(self, cliente, canalEntrada, modalidadEnvio, km, destino):
        self.cliente = cliente
        self.canalEntrada = canalEntrada
        self.modalidadEnvio = modalidadEnvio
        self.km = km
        self.destino = destino
        self.viaje = None

        self.Paquetes: Dict[Paquete, int] = dict()
    
    def __str__(self):

        return f"Pedido de cliente {self.cliente}, con canal de entrada {self.canalEntrada}, por {self.modalidadEnvio}, a {self.destino} a {self.km} km añadidos al viaje {self.viaje}\n"

    def AgregarPaquete(self, paquete): #Añade al diccionario Paquetes la clave paquete 
        if paquete not in self.Paquetes: #Si el paquete no se ha añadido todavía le crea un valor 1
            self.Paquetes[paquete] = 1
        else: #Si el paquete ya esta añadido se le añade uno al valor
            self.Paquetes[paquete] += 1


    def Coste(self):
        costetotal = 0
        for paquete in self.Paquetes.keys(): #Suma el precio de todos los paquetes con la cantidad de veces q esta ese paquete

            costetotal += paquete.Precio()*self.Paquetes[paquete] 
        
        if self.modalidadEnvio ==  "Domicilio": # Si la modalidad de envio es domicilio se le añaden 5.5 euros
            costetotal += 5.5
        
        return costetotal + self.km*3 #Cada km costaria 3 euros
    
    def Peso(self):
        peso = 0
        for paquete in self.Paquetes.keys(): #Añade el peso de cada paquete por la cantidad de veces que esta ese paquete
            peso += paquete.peso * self.Paquetes[paquete]
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
        if self.ubicacion == 0: #Si la ubicación es 0 (predeterminada) el viaje no estará moviendose
            return f"El vehiculo {self.modelo} no esta en reparto"
        else: #El caso contrario significa que estará en reparto
            return f"El vehiculo {self.modelo} esta en reparto"

    def __str__(self):
        return f"Vehiculo: {self.modelo} con cargaMaxima {self.cargaMaxima} kg"

    @classmethod
    def VehiculosDisponibles(cls): #Añade cada objeto vehiculo que esta disponible
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

    def __str__(self):
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
        return "Camion: " + super().__str__()

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
        
        txt3 = "** Parte de viaje ** \n"
        if self.ParteViaje != None:
    
            for i in self.ParteViaje.incidencias:
                txt3 += (f'Incidente : {i}, Observacion:{self.ParteViaje.incidencias[i]}' ) + "\n"
        
        return f"Viaje {self.id} en el vehiculo {self.vehiculo} \n" + txt1 + txt2 + txt3
    
    def AñadirPedido(self, pedido):
        peso = 0
        for pedido1 in self.pedidos: #Suma todos los pedidos
            peso += pedido1.Peso()

        if peso + pedido.Peso() > 3500 : #Ponemos como limite 3.500 kilos y si al añadir este viaje supera esa cantidad se añade un error

            raise Exception(f"El viaje {self.id} esta completo, por favor busque otro viaje disponible")
            
        self.pedidos.append(pedido)
        pedido.viaje = self.id
        
    def SeleccionVehiculo(self):
        peso = 0
        for pedido in self.pedidos:
            peso += pedido.Peso()
        
        for vehiculo in Vehiculo.VehiculosDisponibles(): #Revisa todos los vehiculos
            if vehiculo.cargaMaxima >= peso: #Si el vehiculo soporta el peso del viaje se añade este vehiculo y se quita de disponibles
                self.vehiculo = vehiculo
                self.vehiculo.disponible = False
                break
        return Exception(f"No hay vehiculos para seleccionar")
    
    def SeleccionTrabajadores(self):
        if len(Mixto.MixtosDisponibles()) > 0: #Si tenemos la opción de añadir un mixto nada mas como trabajador lo hacemos
            contratado = Mixto.MixtosDisponibles()[0] 
            self.trabajadores.append(contratado)
            contratado.viaje = self
            contratado.disponible = False
        elif len(Conductor.conductoresDisponibles()) > 0 and len(Ayudante.AyudantesDisponibles()) > 0: #Añadimos un ayudante y un conductor
            self.trabajadores.append(Conductor.conductoresDisponibles()[0])
            Conductor.conductoresDisponibles()[0].viaje = self
            Conductor.conductoresDisponibles()[0].disponible = False
            self.trabajadores.append(Ayudante.AyudantesDisponibles()[0])
            Ayudante.AyudantesDisponibles()[0].viaje = self
            Ayudante.AyudantesDisponibles()[0].disponible = False
        else:
            raise Exception(f"No hay suficientes trabajadores para hacer un viaje")
    
    def FinViaje(self):
        if self.vehiculo.UbicacionActual() == 0: #si el viaje no ha iniciado no podra finalizar
            raise Exception(f"El viaje {self.id} no ha salido todavia")
        self.vehiculo.disponible = True #SE vuelve a poner el vehiculo disponible
        for trabajador in self.trabajadores: #Hacemos disponibles los trabajadores
            trabajador.disponible = True 
        self.vehiculo.ubicacion = 0

    def IniciarViaje(self):
        if len(self.pedidos) == 0: #Si no hay pedidos no se puede iniciar el viaje
            raise Exception(f"El viaje {self.id} no saldrá por que no tiene pedidos asignados")
        self.SeleccionVehiculo()
        self.SeleccionTrabajadores()
        self.vehiculo.disponible = False
        self.vehiculo.ubicacion = 1

    def VerParte(self):
        if self.ParteViaje == None: #si no hay parte de viaje no se puede ver
            raise Exception(f"No hay parte del viaje {self.id}")
        for i in self.ParteViaje.incidencias:
            print(f'Incidente : {i}, Observacion:{self.ParteViaje.incidencias[i]}')



class Cliente:
    def __init__(self, id):
        self.id = id
        self.listaPedidos: List[Pedido] = list()
        self.paquetes = []
    
    def __str__(self):
        return f"Cliente {self.id} "
    def AñadirPaquetes(self,paquete):
        self.paquetes.append(paquete)
    def HacerPedido(self, paquetes, canalEntrada, modalidadEnvio, km, destino):

        pedido = Pedido(len(self.listaPedidos),  canalEntrada, modalidadEnvio, km, destino) #Creamos un Pedido()
        self.listaPedidos.append(pedido)

        for paquete in paquetes:
            self.AñadirPaquetes(paquete) #Añadimos los pedidos 
            pedido.AgregarPaquete(paquete)

        lista_viajes = Viaje.todos_los_viajes
        for viaje1 in lista_viajes: #Buscamos viaje para poder añadir el pedido
            try:
                viaje1.AñadirPedido(pedido)
                pedido.viaje = viaje1.id
                break
            except Exception:
                continue
    
    def FacturaciónMesual(self):#Usamos directamente todos los pedidos hechos y calculamos el gasto total
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
    def TrabajadoresDisponibles(cls): #Seleccionamos todos los trabajadores disponibles
        return [trabajador for trabajador in cls.todos_los_trabajadores if trabajador.disponible]


class Ayudante(Trabajador):
    todos_los_ayudantes = list()
    def __init__(self, id, añosContrato):
        super().__init__(id, añosContrato)

        Ayudante.todos_los_ayudantes.append(self)

    def __str__(self):
        return "Ayudante: " + super().__str__() 
    
    @classmethod
    def AyudantesDisponibles(cls): #Seleccionamos todos los ayudantes disponibles
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
    def MixtosDisponibles(cls): #Seleccionamos todos los mixtos disponibles
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
    def conductoresDisponibles(cls): #Seleccionamos todos los conductores disponibles
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
        self.incidencias[incidencia] = observacion

if __name__ == "__main__":
    print("=== Creando Paquetes ===")
    paquete1 = Paquete("Fresa",205)    # 5 kg
    paquete2 = Paquete("Chocolate", 1110)   # 10 kg
    paquete3 = Paquete("Agua", 2000)    # 2 kg
    paquete4 = Paquete("Papel", 500)   # 50 kg

    print(f"Paquete 1: {paquete1}, Precio: {paquete1.Precio()}€")
    print(f"Paquete 2: {paquete2}, Precio: {paquete2.Precio()}€")

    print("\n=== Creando Clientes ===")
    cliente1 = Cliente("C001")
    cliente2 = Cliente("C002")
   

    print("\n=== Creando Vehículos ===")
    furgoneta = Furgoneta(3000, "Ford Transit")
    camion = Camion(5000, "Volvo FH16")
    bici_electrica = BicicletaElectrica(20, "E-Bike Pro")
    bicicleta = Bicicleta(10, "Classic Bike")
  
    print("\n=== Creando Trabajadores ===")
    conductor = Conductor("T001", 5, 10)
    ayudante = Ayudante("T002", 2)
    mixto = Mixto("T003", 3, 7)

    viaje1 = Viaje(1)
    viaje2 = Viaje(2)
    

    print("\n=== Cliente 1 Hace Pedidos ===")
    cliente1.HacerPedido((paquete1, paquete2), canalEntrada=canalEntrada.TELEFONO, modalidadEnvio="Sucursal", km=20, destino="Madrid")
    cliente1.HacerPedido((paquete3, paquete1), canalEntrada=canalEntrada.IMPRESOS, modalidadEnvio="Domicilio", km=10, destino="Barcelona")
  
    print("\n=== Cliente 2 Hace un Pedido Grande ===")
    cliente2.HacerPedido((paquete4, paquete4), canalEntrada=canalEntrada.FAX, modalidadEnvio="Sucursal", km=50, destino="Sevilla")
    
    print("\n=== Mostrando Costes de Pedidos ===")
    print(f'El coste total de los pedidos del primer cliente es {cliente1.FacturaciónMesual()}')
    print(f'El coste total de los pedidos del segundo cliente es {cliente2.FacturaciónMesual()}')

    viaje1.IniciarViaje()
    viaje2.IniciarViaje()

    print(camion.UbicacionActual())
    print(furgoneta.UbicacionActual())
    
    viaje1.FinViaje()
    print("\n Detalles del viaje 1")
    print(viaje1)
 
    ayudante.IncidenciaViaje("Retraso", "Accidente en la carretera")
    ayudante.IncidenciaViaje("Paquete dañado", "Caja aplastada")

    print(camion.UbicacionActual())
    print(furgoneta.UbicacionActual())
    viaje2.FinViaje()
    print("\n Detalles del viaje 2")
    print(viaje2)

 
    print("\n=== Verificando Vehículos Disponibles ===")
    print("Vehículos disponibles:", [str(v) for v in Vehiculo.VehiculosDisponibles()])

    print("\n=== Verificando Trabajadores Disponibles ===")
    print("Trabajadores disponibles:", [str(m) for m in Mixto.MixtosDisponibles()] + [str(a) for a in Ayudante.AyudantesDisponibles()] + [str(c) for c in Conductor.conductoresDisponibles()])