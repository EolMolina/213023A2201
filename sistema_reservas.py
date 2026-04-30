from abc import ABC, abstractmethod

# ===== LOGS =====
def registrar_log(mensaje):
    with open("log.txt", "a") as f:
        f.write(mensaje + "\n")


# ===== EXCEPCIÓN PERSONALIZADA =====
class ErrorReserva(Exception):
    pass


# ===== CLIENTE =====
class Cliente:
    def __init__(self, nombre, identificacion):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        if not identificacion:
            raise ValueError("Identificación inválida")

        self.__nombre = nombre
        self.__id = identificacion

    def get_nombre(self):
        return self.__nombre


# ===== SERVICIO (ABSTRACTO) =====
class Servicio(ABC):
    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# ===== SERVICIOS CONCRETOS =====
class ServicioSala(Servicio):
    def calcular_costo(self):
        return 100

    def descripcion(self):
        return "Reserva de sala"


class ServicioEquipo(Servicio):
    def calcular_costo(self):
        return 200

    def descripcion(self):
        return "Alquiler de equipo"


class ServicioAsesoria(Servicio):
    def calcular_costo(self):
        return 300

    def descripcion(self):
        return "Asesoría especializada"


# ===== RESERVA =====
class Reserva:
    def __init__(self, cliente, servicio):
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Cliente inválido")

        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Servicio inválido")

        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"

    def confirmar(self):
        try:
            costo = self.servicio.calcular_costo()
            self.estado = "Confirmada"
            print(f"Reserva confirmada para {self.cliente.get_nombre()} - Costo: {costo}")
        except Exception as e:
            registrar_log(str(e))
            print("Error al confirmar reserva")

    def cancelar(self):
        self.estado = "Cancelada"
        print("Reserva cancelada")


# ===== SIMULACIÓN =====
def main():
    try:
        cliente1 = Cliente("Wendy", "123")
        servicio1 = ServicioSala()

        reserva1 = Reserva(cliente1, servicio1)
        reserva1.confirmar()

        # ERROR intencional
        cliente2 = Cliente("", "456")

    except Exception as e:
        print("Error detectado:", e)
        registrar_log(str(e))

    finally:
        print("Proceso finalizado")


if __name__ == "__main__":
    main()