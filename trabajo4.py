import logging
from datetime import datetime
from abc import ABC, abstractmethod

# ===== LOGS =====
def registrar_log(mensaje, tipo="INFO"):
    try:
        with open("log.txt", "a", encoding="utf-8") as f:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{fecha}] [{tipo}] {mensaje}\n")
    except Exception as e:
        print("Error crítico al escribir log:", e)


# ===== EXCEPCIONES PERSONALIZADAS =====
class ErrorSoftwareFJ(Exception):
    """Clase base para excepciones del sistema"""
    pass

class ErrorReserva(Exception):
    pass


class ErrorServicio(Exception):
    pass


# ===== CLIENTE =====
class Cliente:
    def __init__(self, nombre, identificacion):
        if not nombre:
            raise ValueError("El nombre no puede estar vacio")
        if not identificacion:
            raise ValueError("Identificación inválida")

        self.__nombre = nombre
        self.__id = identificacion

    def get_nombre(self):
        return self.__nombre


# ===== SERVICIO ABSTRACTO =====
class Servicio(ABC):
    def __init__(self, codigo, nombre, precio_base, disponible=True):
        self.codigo = codigo
        self.nombre = nombre
        self.precio_base = precio_base
        self.disponible = disponible

    @property
    def precio_base(self): return self.__precio_base
    
    @precio_base.setter
    def precio_base(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ErrorServicio("Precio base inconsistente: debe ser positivo.")
        self.__precio_base = float(valor)

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ErrorServicio(f"Servicio '{self.nombre}' NO disponible.")
        return True

    @abstractmethod
    def calcular_costo(self, duracion=1, impuesto=0.19): 
        """Método para polimorfismo y sobrecarga"""
        pass

    @abstractmethod
    def descripcion(self): pass

    @abstractmethod
    def validar_parametros(self): pass

# ===== 5. SERVICIOS ESPECIALIZADOS (Polimorfismo y Sobrescritura) =====

class ServicioSala(Servicio):
    def __init__(self, codigo="S01", nombre="Sala Pro", precio=100, capacidad=10, audiovisuales=False):
        self.capacidad = capacidad
        self.audiovisuales = audiovisuales
        super().__init__(codigo, nombre, precio)
        self.validar_parametros()

    def validar_parametros(self):
        if not (0 < self.capacidad <= 100):
            raise ErrorServicio("Capacidad de sala fuera de rango (1-100).")

    def calcular_costo(self, duracion=1, impuesto=0.19):
        self.validar_disponibilidad()
        costo = self.precio_base * duracion
        if self.capacidad > 50: costo += 50
        if self.audiovisuales: costo += 30
        return costo * (1 + impuesto) # Simulación de sobrecarga con parámetros opcionales

    def descripcion(self):
        return f"Sala para {self.capacidad} personas (AV: {self.audiovisuales})."

class ServicioEquipo(Servicio):
    TIPOS_VALIDOS = ["computador", "proyector", "sonido"]

    def __init__(self, codigo="E01", nombre="Alquiler Equipo", precio=200, tipo="computador", cantidad=1):
        self.tipo_equipo = tipo.lower()
        self.cantidad = cantidad
        super().__init__(codigo, nombre, precio)
        self.validar_parametros()

    def validar_parametros(self):
        if self.tipo_equipo not in self.TIPOS_VALIDOS:
            raise ErrorServicio(f"Tipo de equipo '{self.tipo_equipo}' no permitido.")
        if not (0 < self.cantidad <= 20):
            raise ErrorServicio("Cantidad de equipos inválida (1-20).")

    def calcular_costo(self, duracion=1, impuesto=0.19):
        self.validar_disponibilidad()
        costo = (self.precio_base * self.cantidad) * duracion
        return costo * (1 + impuesto)

    def descripcion(self):
        return f"Alquiler de {self.cantidad} {self.tipo_equipo}(s)."

class ServicioAsesoria(Servicio):
    NIVELES = {"basico": 1.0, "avanzado": 1.5}

    def __init__(self, codigo="A01", nombre="Asesoría", precio=300, area="software", nivel="basico"):
        self.area = area.lower()
        self.nivel = nivel.lower()
        super().__init__(codigo, nombre, precio)
        self.validar_parametros()

    def validar_parametros(self):
        if self.nivel not in self.NIVELES:
            raise ErrorServicio("Nivel de asesoría inexistente.")

    def calcular_costo(self, duracion=1, impuesto=0.19):
        self.validar_disponibilidad()
        costo = (self.precio_base * duracion) * self.NIVELES[self.nivel]
        return costo * (1 + impuesto)

    def descripcion(self):
        return f"Asesoría en {self.area} ({self.nivel})."
    
# ===== RESERVA =====
class Reserva:
    def __init__(self, cliente, servicio, duracion=1):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def procesar(self):
        print(f"Iniciando proceso de reserva para cliente: {self.cliente.get_nombre()} - Servicio: {self.servicio.descripcion()} - Duración: {self.duracion} horas")
        try:
            if not isinstance(self.duracion, int) or self.duracion <= 0:
                raise ErrorReserva("Duración debe ser un número entero positivo.")
            
            total = self.servicio.calcular_costo(self.duracion)
            self.estado = "Confirmada"
            
        except ErrorSoftwareFJ as e:
            # Encadenamiento de excepciones
            self.estado = "Fallida"
            logging.error(f"Error en Reserva [{self.cliente.nombre}]: {e}")
            print(f"[ERROR DE NEGOCIO] {e}")
            raise ErrorReserva("No se pudo completar la operación.") from e
            
        except Exception as e:
            self.estado = "Error Técnico"
            logging.critical(f"CRITICAL: Error inesperado: {e}")
            print(f"[ERROR TÉCNICO] Contacte a soporte.")
            
        else: # Se ejecuta solo si NO hubo errores
            logging.info(f"ÉXITO: {self.cliente.get_nombre()} reservó {self.servicio.nombre}")
            print(f"Factura Generada: ${total:.2f} | Estado: {self.estado}")
            
        finally: # Se ejecuta SIEMPRE
            print(f"Finalizando transacción para: {self.cliente.get_nombre()}.")

# ===== SIMULACIÓN =====
def ejecutar_simulacion():
    print("=== INICIANDO SIMULACIÓN SOFTWARE FJ (10 OPERACIONES) ===")
    
    # Lista interna para gestionar objetos
    operaciones = []
    
    # 1. Cliente Válido
    try:
        c1 = Cliente("Wendy Ramos", "WEN123")
        s1 = ServicioSala(capacidad=20)
        operaciones.append(Reserva(c1, s1, 3))
    except Exception as e: print(e)

    # 2. Cliente Inválido (Nombre corto)
    try: Cliente("Jo", "ID01")
    except Exception as e: 
        logging.error(f"Simulación 2: {e}")
        print(f"Op 2: Error esperado en cliente: {e}")

    # 3. Servicio Incorrecto (Capacidad excedida)
    try: ServicioSala(capacidad=500)
    except Exception as e:
        logging.error(f"Simulación 3: {e}")
        print(f"Op 3: Error esperado en sala: {e}")

    # 4. Servicio No Disponible
    try:
        s_off = ServicioEquipo(tipo="proyector")
        s_off.disponible = False
        operaciones.append(Reserva(c1, s_off, 2))
    except Exception as e: print(e)

    # 5. Reserva Correcta (Equipo)
    try:
        c2 = Cliente("Juan Perez", "JP007")
        s2 = ServicioEquipo(tipo="sonido", cantidad=2)
        operaciones.append(Reserva(c2, s2, 5))
    except Exception as e: print(e)

    # 6. Parámetro Faltante/Inválido (Duración negativa)
    try:
        operaciones.append(Reserva(c1, s1, -10))
    except Exception as e: print(e)

    # 7. Asesoría Exitosa (Avanzada)
    try:
        s3 = ServicioAsesoria(area="Seguridad", nivel="avanzado")
        operaciones.append(Reserva(c2, s3, 10))
    except Exception as e: print(e)

    # 8. ID de cliente inválido (No alfanumérico)
    try: Cliente("Marco Polo", "!!!???")
    except Exception as e:
        print(f"Op 8: Error esperado en ID: {e}")

    # 9. Tipo de equipo inexistente
    try: ServicioEquipo(tipo="Dron")
    except Exception as e:
        print(f"Op 9: Error esperado en equipo: {e}")

    # 10. Precio base negativo
    try: ServicioSala(precio=-50)
    except Exception as e:
        print(f"Op 10: Error esperado en precio: {e}")

    # PROCESAR TODAS LAS RESERVAS CREADAS
    print("\n--- EJECUTANDO PROCESAMIENTO DE RESERVAS REGISTRADAS ---")
    for res in operaciones:
        try:
            res.procesar()
        except ErrorReserva:
            pass # La aplicación continúa funcionando aunque una reserva falle

if __name__ == "__main__":
    ejecutar_simulacion()
    print("\n=== SIMULACIÓN FINALIZADA. APP ESTABLE. CONSULTE log_servicios.txt ===")


