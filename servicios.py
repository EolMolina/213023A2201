from abc import ABC, abstractmethod


# ===== EXCEPCIÓN PERSONALIZADA PARA SERVICIOS =====
class ErrorServicio(Exception):
    """
    Excepción personalizada para controlar errores relacionados
    con los servicios ofrecidos por Software FJ.
    """
    pass


# ===== CLASE ABSTRACTA SERVICIO =====
class Servicio(ABC):
    """
    Clase abstracta que representa un servicio general dentro del sistema.

    Esta clase funciona como una plantilla para todos los servicios concretos
    ofrecidos por Software FJ. No se debe crear un objeto directamente desde
    esta clase, porque su función principal es definir la estructura común que
    deben respetar los servicios especializados.

    Los servicios concretos deben implementar obligatoriamente los métodos:
    calcular_costo, descripcion y validar_parametros.
    """

    def __init__(self, codigo, nombre, precio_base, disponible=True):
        self.__codigo = None
        self.__nombre = None
        self.__precio_base = None
        self.__disponible = None

        self.codigo = codigo
        self.nombre = nombre
        self.precio_base = precio_base
        self.disponible = disponible

    # ===== ENCAPSULAMIENTO Y VALIDACIONES GENERALES =====

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
            raise ErrorServicio("El precio base debe ser un valor numerico")
        if valor <= 0:
            raise ErrorServicio("El precio base debe ser mayor que cero")
        self.__precio_base = float(valor)

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ErrorServicio("La disponibilidad debe ser un valor booleano")
        self.__disponible = valor

    def validar_disponibilidad(self):
        """
        Verifica si el servicio se encuentra disponible para ser reservado.
        """
        if not self.disponible:
            raise ErrorServicio(f"El servicio '{self.nombre}' no se encuentra disponible")
        return True

    # ===== MÉTODOS ABSTRACTOS =====

    @abstractmethod
    def calcular_costo(self, duracion=1):
        """
        Método abstracto que debe ser implementado por cada servicio concreto.
        """
        pass

    @abstractmethod
    def descripcion(self):
        """
        Método abstracto que debe devolver la descripción del servicio.
        """
        pass

    @abstractmethod
    def validar_parametros(self):
        """
        Método abstracto para validar las reglas propias de cada servicio.
        """
        pass

    # ===== MÉTODOS CON PARÁMETROS OPCIONALES =====
    # En Python no existe sobrecarga tradicional como en Java o C++;
    # por eso se simula mediante parámetros opcionales.

    def calcular_costo_con_impuesto(self, duracion=1, impuesto=0.19):
        """
        Calcula el costo del servicio aplicando un impuesto.

        Parámetros:
        duracion: tiempo de uso del servicio.
        impuesto: porcentaje de impuesto expresado en decimal.
        Ejemplo: 0.19 representa el 19%.
        """
        try:
            if not isinstance(impuesto, (int, float)):
                raise ErrorServicio("El impuesto debe ser numérico")

            if impuesto < 0:
                raise ErrorServicio("El impuesto no puede ser negativo")

            costo = self.calcular_costo(duracion)
            return costo + (costo * impuesto)

        except ErrorServicio as error:
            raise ErrorServicio("No fue posible calcular el costo con impuesto") from error

    def calcular_costo_con_descuento(self, duracion=1, descuento=0.0):
        """
        Calcula el costo del servicio aplicando un descuento.

        Parámetros:
        duracion: tiempo de uso del servicio.
        descuento: porcentaje de descuento expresado en decimal.
        Ejemplo: 0.10 representa el 10%.
        """
        try:
            if not isinstance(descuento, (int, float)):
                raise ErrorServicio("El descuento debe ser numérico")

            if descuento < 0 or descuento > 1:
                raise ErrorServicio("El descuento debe estar entre 0 y 1")

            costo = self.calcular_costo(duracion)
            return costo - (costo * descuento)

        except ErrorServicio as error:
            raise ErrorServicio("No fue posible calcular el costo con descuento") from error

    def __str__(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"{self.codigo} - {self.nombre} | Precio base: {self.precio_base} | Estado: {estado}"


# ===== SERVICIO ESPECIALIZADO 1: RESERVA DE SALA =====
class ServicioSala(Servicio):
    """
    Servicio especializado para la reserva de salas.

    Esta clase hereda de Servicio e implementa sus propios métodos para calcular
    costos, describir el servicio y validar parámetros. Con esto se aplica
    polimorfismo, porque sobrescribe los métodos definidos en la clase abstracta.
    """

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
            raise ErrorServicio("La capacidad de la sala debe ser un número entero")

        if valor <= 0:
            raise ErrorServicio("La capacidad de la sala debe ser mayor que cero")

        self.__capacidad = valor

    @property
    def incluye_audiovisuales(self):
        return self.__incluye_audiovisuales

    @incluye_audiovisuales.setter
    def incluye_audiovisuales(self, valor):
        if not isinstance(valor, bool):
            raise ErrorServicio("El campo de audiovisuales debe ser verdadero o falso")

        self.__incluye_audiovisuales = valor

    def validar_parametros(self):
        """
        Valida las condiciones específicas de una sala.
        """
        if self.capacidad > 100:
            raise ErrorServicio("La sala no puede superar una capacidad de 100 personas")

        return True

    def calcular_costo(self, duracion=1):
        """
        Calcula el costo de la reserva de una sala.

        El costo depende de la duración de la reserva, la capacidad de la sala
        y si se incluyen recursos audiovisuales.
        """
        self.validar_disponibilidad()

        if not isinstance(duracion, (int, float)):
            raise ErrorServicio("La duración de la reserva debe ser numérica")

        if duracion <= 0:
            raise ErrorServicio("La duración de la reserva debe ser mayor que cero")

        costo = self.precio_base * duracion

        if self.capacidad > 50:
            costo += 50

        if self.incluye_audiovisuales:
            costo += 30

        return costo

    def descripcion(self):
        if self.incluye_audiovisuales:
            audiovisuales = "incluye recursos audiovisuales"
        else:
            audiovisuales = "no incluye recursos audiovisuales"

        return (
            f"Reserva de sala: {self.nombre}. "
            f"Capacidad: {self.capacidad} personas; {audiovisuales}. "
            f"El costo se calcula según la duración, la capacidad y los recursos adicionales."
        )


# ===== SERVICIO ESPECIALIZADO 2: ALQUILER DE EQUIPO =====
class ServicioEquipo(Servicio):
    """
    Servicio especializado para el alquiler de equipos.

    Esta clase permite representar el alquiler de computadores, proyectores,
    equipos de sonido, impresoras o tabletas.
    """

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
            raise ErrorServicio("La cantidad de equipos debe ser un número entero")

        if valor <= 0:
            raise ErrorServicio("La cantidad de equipos debe ser mayor que cero")

        self.__cantidad = valor

    def validar_parametros(self):
        """
        Valida las condiciones específicas del alquiler de equipos.
        """
        if self.tipo_equipo not in self.TIPOS_VALIDOS:
            raise ErrorServicio(
                f"Tipo de equipo inválido. Tipos permitidos: {', '.join(self.TIPOS_VALIDOS)}"
            )

        if self.cantidad > 20:
            raise ErrorServicio("No se pueden alquilar más de 20 equipos en una sola reserva")

        return True

    def calcular_costo(self, duracion=1):
        """
        Calcula el costo del alquiler de equipos.

        El costo depende de la duración, la cantidad de equipos y el tipo de
        equipo seleccionado.
        """
        self.validar_disponibilidad()

        if not isinstance(duracion, (int, float)):
            raise ErrorServicio("La duración del alquiler debe ser numérica")

        if duracion <= 0:
            raise ErrorServicio("La duración del alquiler debe ser mayor que cero")

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
            f"Tipo de equipo: {self.tipo_equipo}; cantidad solicitada: {self.cantidad}. "
            f"El costo se calcula de acuerdo con la duración, la cantidad y el tipo de equipo."
        )


# ===== SERVICIO ESPECIALIZADO 3: ASESORÍA ESPECIALIZADA =====
class ServicioAsesoria(Servicio):
    """
    Servicio especializado para asesorías profesionales.

    Esta clase representa asesorías en distintas áreas, como software, redes,
    seguridad, datos e inteligencia artificial.
    """

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
        """
        Valida las condiciones específicas de una asesoría especializada.
        """
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
        """
        Calcula el costo de una asesoría especializada.

        El costo depende de la duración, el área de asesoría y el nivel de
        especialización solicitado.
        """
        self.validar_disponibilidad()

        if not isinstance(duracion, (int, float)):
            raise ErrorServicio("La duración de la asesoría debe ser numérica")

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
            f"Área: {self.area}; nivel: {self.nivel}. "
            f"El costo se calcula según la duración, el área profesional y el nivel de especialización."
        )

