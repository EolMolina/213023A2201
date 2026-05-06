from abc import ABC, abstractmethod


# ===== LOGS =====
def registrar_log(mensaje):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(mensaje + "\n")


# ===== EXCEPCIONES PERSONALIZADAS =====
class ErrorReserva(Exception):
    pass


class ErrorServicio(Exception):
    pass


# ===== CLIENTE =====
class Cliente:
    def __init__(self, nombre, identificacion):
        self.__nombre = None
        self.__id = None

        self.set_nombre(nombre)
        self.set_identificacion(identificacion)

    # GETTERS
    def get_nombre(self):
        return self.__nombre

    def get_identificacion(self):
        return self.__id

    # SETTERS (VALIDACIONES)
    def set_nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        self.__nombre = nombre.strip()

    def set_identificacion(self, identificacion):
        if not identificacion or not str(identificacion).isdigit():
            raise ValueError("La identificación debe ser numérica")
        self.__id = identificacion

    # OPCIONAL (BONUS)
    def mostrar_info(self):
        return f"Cliente: {self.__nombre} - ID: {self.__id}"


# ===== SERVICIO ABSTRACTO =====
class Servicio(ABC):
    def __init__(self, codigo, nombre, precio_base, disponible=True):
        self.__codigo = None
        self.__nombre = None
        self.__precio_base = None
        self.__disponible = None

        self.codigo = codigo
        self.nombre = nombre
        self.precio_base = precio_base
        self.disponible = disponible

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ErrorServicio("El código del servicio no puede estar vacio")
        self.__codigo = valor.strip().upper()

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ErrorServicio("El nombre del servicio no puede estar vacio")
        self.__nombre = valor.strip()

    @property
    def precio_base(self):
        return self.__precio_base

    @precio_base.setter
    def precio_base(self, valor):
        if not isinstance(valor, (int, float)):
            raise ErrorServicio("El precio base debe ser numerico")
        if valor <= 0:
            raise ErrorServicio("El precio base debe ser mayor que cero")
        self.__precio_base = float(valor)

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ErrorServicio("La disponibilidad debe ser verdadera o falsa")
        self.__disponible = valor

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ErrorServicio(f"El servicio '{self.nombre}' no se encuentra disponible")
        return True

    @abstractmethod
    def calcular_costo(self, duracion=1):
        pass

    @abstractmethod
    def descripcion(self):
        pass

    @abstractmethod
    def validar_parametros(self):
        pass

    def calcular_costo_con_impuesto(self, duracion=1, impuesto=0.19):
        try:
            if not isinstance(impuesto, (int, float)):
                raise ErrorServicio("El impuesto debe ser numerico")
            if impuesto < 0:
                raise ErrorServicio("El impuesto no puede ser negativo")

            costo = self.calcular_costo(duracion)
            return costo + (costo * impuesto)

        except ErrorServicio as e:
            raise ErrorServicio("No fue posible calcular el costo con impuesto") from e

    def calcular_costo_con_descuento(self, duracion=1, descuento=0.0):
        try:
            if not isinstance(descuento, (int, float)):
                raise ErrorServicio("El descuento debe ser numérico")
            if descuento < 0 or descuento > 1:
                raise ErrorServicio("El descuento debe estar entre 0 y 1")

            costo = self.calcular_costo(duracion)
            return costo - (costo * descuento)

        except ErrorServicio as e:
            raise ErrorServicio("No fue posible calcular el costo con descuento") from e


# ===== SERVICIO 1: RESERVA DE SALA =====
class ServicioSala(Servicio):
    def __init__(
        self,
        codigo="S001",
        nombre="Reserva de sala",
        precio_base=100,
        capacidad=10,
        incluye_audiovisuales=False,
        disponible=True
    ):
        super().__init__(codigo, nombre, precio_base, disponible)
        self.capacidad = capacidad
        self.incluye_audiovisuales = incluye_audiovisuales
        self.validar_parametros()

    @property
    def capacidad(self):
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, valor):
        if not isinstance(valor, int):
            raise ErrorServicio("La capacidad de la sala debe ser un numero entero")
        if valor <= 0:
            raise ErrorServicio("La capacidad de la sala debe ser mayor que cero")
        self.__capacidad = valor

    @property
    def incluye_audiovisuales(self):
        return self.__incluye_audiovisuales

    @incluye_audiovisuales.setter
    def incluye_audiovisuales(self, valor):
        if not isinstance(valor, bool):
            raise ErrorServicio("El campo audiovisuales debe ser verdadero o falso")
        self.__incluye_audiovisuales = valor

    def validar_parametros(self):
        if self.capacidad > 100:
            raise ErrorServicio("La sala no puede superar una capacidad de 100 personas")
        return True

    def calcular_costo(self, duracion=1):
        self.validar_disponibilidad()

        if not isinstance(duracion, (int, float)):
            raise ErrorServicio("La duración de la reserva debe ser numerica")
        if duracion <= 0:
            raise ErrorServicio("La duración de la reserva debe ser mayor que cero")

        costo = self.precio_base * duracion

        if self.capacidad > 50:
            costo += 50

        if self.incluye_audiovisuales:
            costo += 30

        return costo

    def descripcion(self):
        audiovisuales = "incluye recursos audiovisuales" if self.incluye_audiovisuales else "no incluye recursos audiovisuales"

        return (
            f"Reserva de sala: {self.nombre}. "
            f"Capacidad: {self.capacidad} personas; {audiovisuales}."
        )


# ===== SERVICIO 2: ALQUILER DE EQUIPO =====
class ServicioEquipo(Servicio):
    TIPOS_VALIDOS = ["computador", "proyector", "sonido", "impresora", "tablet"]

    def __init__(
        self,
        codigo="E001",
        nombre="Alquiler de equipo",
        precio_base=200,
        tipo_equipo="computador",
        cantidad=1,
        disponible=True
    ):
        super().__init__(codigo, nombre, precio_base, disponible)
        self.tipo_equipo = tipo_equipo
        self.cantidad = cantidad
        self.validar_parametros()

    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ErrorServicio("El tipo de equipo no puede estar vacio")
        self.__tipo_equipo = valor.strip().lower()

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if not isinstance(valor, int):
            raise ErrorServicio("La cantidad de equipos debe ser un numero entero")
        if valor <= 0:
            raise ErrorServicio("La cantidad de equipos debe ser mayor que cero")
        self.__cantidad = valor

    def validar_parametros(self):
        if self.tipo_equipo not in self.TIPOS_VALIDOS:
            raise ErrorServicio(
                f"Tipo de equipo inválido. Tipos permitidos: {', '.join(self.TIPOS_VALIDOS)}"
            )

        if self.cantidad > 20:
            raise ErrorServicio("No se pueden alquilar mas de 20 equipos en una sola reserva")

        return True

    def calcular_costo(self, duracion=1):
        self.validar_disponibilidad()

        if not isinstance(duracion, (int, float)):
            raise ErrorServicio("La duracion del alquiler debe ser numérica")
        if duracion <= 0:
            raise ErrorServicio("La duracion del alquiler debe ser mayor que cero")

        costo = self.precio_base * self.cantidad * duracion

        if self.tipo_equipo == "computador":
            costo += 20 * self.cantidad
        elif self.tipo_equipo == "proyector":
            costo += 15 * self.cantidad
        elif self.tipo_equipo == "sonido":
            costo += 25 * self.cantidad

        return costo

    def descripcion(self):
        return (
            f"Alquiler de equipo: {self.nombre}. "
            f"Tipo de equipo: {self.tipo_equipo}; cantidad solicitada: {self.cantidad}."
        )


# ===== SERVICIO 3: ASESORÍA ESPECIALIZADA =====
class ServicioAsesoria(Servicio):
    AREAS_VALIDAS = ["software", "redes", "seguridad", "datos", "inteligencia artificial"]
    NIVELES_VALIDOS = ["basico", "intermedio", "avanzado"]

    def __init__(
        self,
        codigo="A001",
        nombre="Asesoría especializada",
        precio_base=300,
        area="software",
        nivel="basico",
        disponible=True
    ):
        super().__init__(codigo, nombre, precio_base, disponible)
        self.area = area
        self.nivel = nivel
        self.validar_parametros()

    @property
    def area(self):
        return self.__area

    @area.setter
    def area(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ErrorServicio("El área de asesoría no puede estar vacia")
        self.__area = valor.strip().lower()

    @property
    def nivel(self):
        return self.__nivel

    @nivel.setter
    def nivel(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ErrorServicio("El nivel de asesoría no puede estar vacio")
        self.__nivel = valor.strip().lower()

    def validar_parametros(self):
        if self.area not in self.AREAS_VALIDAS:
            raise ErrorServicio(
                f"Área de asesoría inválida. Áreas permitidas: {', '.join(self.AREAS_VALIDAS)}"
            )

        if self.nivel not in self.NIVELES_VALIDOS:
            raise ErrorServicio(
                f"Nivel de asesoría inválido. Niveles permitidos: {', '.join(self.NIVELES_VALIDOS)}"
            )

        return True

    def calcular_costo(self, duracion=1):
        self.validar_disponibilidad()

        if not isinstance(duracion, (int, float)):
            raise ErrorServicio("La duración de la asesoría debe ser numerica")
        if duracion <= 0:
            raise ErrorServicio("La duración de la asesoría debe ser mayor que cero")

        costo = self.precio_base * duracion

        if self.nivel == "intermedio":
            costo *= 1.25
        elif self.nivel == "avanzado":
            costo *= 1.50

        if self.area == "seguridad":
            costo += 60
        elif self.area == "inteligencia artificial":
            costo += 80

        return costo

    def descripcion(self):
        return (
            f"Asesoría especializada: {self.nombre}. "
            f"Área: {self.area}; nivel: {self.nivel}."
        )


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
            print(f"Intentando confirmar reserva para {self.cliente.get_nombre()}...")

            costo = self.servicio.calcular_costo()
            self.estado = "Confirmada"

        except Exception as e:
            self.estado = "Error"
            registrar_log(f"[ERROR] Reserva fallida: {str(e)}")
            print("Error al confirmar reserva")

        else:
            registrar_log(f"[INFO] Reserva confirmada para {self.cliente.get_nombre()} - Costo: {costo}")
            print(f"Reserva confirmada para {self.cliente.get_nombre()} - Costo: {costo}")

        finally:
            print("Proceso de confirmación finalizado\n")

    def cancelar(self):
        self.estado = "Cancelada"
        print("Reserva cancelada")


# ===== SIMULACIÓN =====
def main():
    try:
        cliente1 = Cliente("Wendy", "123")

        servicio1 = ServicioSala(
            codigo="S001",
            nombre="Sala ejecutiva",
            precio_base=100,
            capacidad=40,
            incluye_audiovisuales=True
        )

        reserva1 = Reserva(cliente1, servicio1)
        reserva1.confirmar()

        print(servicio1.descripcion())
        print("Costo normal:", servicio1.calcular_costo(2))
        print("Costo con impuesto:", servicio1.calcular_costo_con_impuesto(2))
        print("Costo con descuento:", servicio1.calcular_costo_con_descuento(2, 0.10))
        print("-" * 60)

        servicio2 = ServicioEquipo(
            codigo="E001",
            nombre="Alquiler de computadores",
            precio_base=200,
            tipo_equipo="computador",
            cantidad=3
        )

        reserva2 = Reserva(cliente1, servicio2)
        reserva2.confirmar()

        print(servicio2.descripcion())
        print("Costo equipo:", servicio2.calcular_costo(2))
        print("-" * 60)

        servicio3 = ServicioAsesoria(
            codigo="A001",
            nombre="Asesoría en seguridad informática",
            precio_base=300,
            area="seguridad",
            nivel="avanzado"
        )

        reserva3 = Reserva(cliente1, servicio3)
        reserva3.confirmar()

        print(servicio3.descripcion())
        print("Costo asesoría:", servicio3.calcular_costo(2))
        print("-" * 60)

        # Prueba de error intencional
        servicio_invalido = ServicioEquipo(
            codigo="E002",
            nombre="Equipo inválido",
            precio_base=200,
            tipo_equipo="drone",
            cantidad=2
        )

    except Exception as e:
        print("Error detectado:", e)
        registrar_log(str(e))

    finally:
        print("Proceso finalizado")


if __name__ == "__main__":
    main()
