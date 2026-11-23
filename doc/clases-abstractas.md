# Clases abstractas, herencia y polimorfismo

Una clase permite agrupar datos y operaciones relacionadas. La **herencia**
permite crear una clase especializada a partir de otra. Las **clases
abstractas** ayudan a definir un modelo común que las clases especializadas
deben completar. El **polimorfismo** permite tratar objetos diferentes a través
de una misma interfaz.

Estas herramientas son útiles cuando varias clases representan variaciones de
una misma idea. Por ejemplo, una aplicación puede tener empleados fijos,
autónomos y becarios que comparten datos como el nombre, pero tienen formas
diferentes de calcular su salario.

## Herencia

La herencia crea una relación «es un tipo de». Una clase hija hereda los
atributos y métodos de una clase padre.

```python
class Empleado:
    def __init__(self, nombre):
        self.nombre = nombre

    def presentarse(self):
        return f"Soy {self.nombre}"


class EmpleadoFijo(Empleado):
    def __init__(self, nombre, salario_mensual):
        super().__init__(nombre)
        self.salario_mensual = salario_mensual
```

`EmpleadoFijo` hereda `nombre` y `presentarse()` de `Empleado`. Dentro de la
clase hija, `super()` permite llamar a la implementación de la clase padre.

```python
empleado = EmpleadoFijo("Ana", 2200)

print(empleado.nombre)
print(empleado.presentarse())
```

Salida:

```text
Ana
Soy Ana
```

Cuando conviene modificar un método heredado, se puede sobrescribir:

```python
class EmpleadoFijo(Empleado):
    def __init__(self, nombre, salario_mensual):
        super().__init__(nombre)
        self.salario_mensual = salario_mensual

    def presentarse(self):
        return f"Soy {self.nombre}, empleado fijo"
```

Es preferible invocar primero `super().__init__()` para inicializar todo lo
común a las clases padre.

## Clase abstracta

Una clase abstracta describe una plantilla para otras clases. Puede contener
comportamiento compartido, pero obliga a las clases hijas a implementar ciertos
métodos.

En Python se utilizan el módulo `abc` y dos elementos:

- `ABC`, que convierte una clase en una posible clase abstracta.
- `@abstractmethod`, que marca un método como obligatorio.

```python
from abc import ABC, abstractmethod


class Empleado(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def calcular_salario(self):
        pass

    def presentarse(self):
        return f"Soy {self.nombre}"
```

`Empleado` no se puede instanciar directamente:

```python
empleado = Empleado("Ana")
# TypeError: Can't instantiate abstract class Empleado
# with abstract method calcular_salario
```

Una clase hija debe implementar el método abstracto:

```python
class EmpleadoFijo(Empleado):
    def __init__(self, nombre, salario_mensual):
        super().__init__(nombre)
        self.salario_mensual = salario_mensual

    def calcular_salario(self):
        return self.salario_mensual
```

Ahora sí se puede crear una instancia:

```python
empleado = EmpleadoFijo("Ana", 2200)
print(empleado.calcular_salario())
# 2200
```

Si una clase hija no implementa `calcular_salario()`, seguirá siendo abstracta y
Python no permitirá crearla.

## Implementaciones concretas

Se puede ampliar la plantilla con distintas formas de calcular el salario:

```python
class EmpleadoPorHoras(Empleado):
    def __init__(self, nombre, horas, precio_hora):
        super().__init__(nombre)
        self.horas = horas
        self.precio_hora = precio_hora

    def calcular_salario(self):
        return self.horas * self.precio_hora


class Becario(Empleado):
    def __init__(self, nombre, ayuda_mensual):
        super().__init__(nombre)
        self.ayuda_mensual = ayuda_mensual

    def calcular_salario(self):
        return self.ayuda_mensual
```

Las tres clases siguen una misma interfaz: todas tienen `nombre`,
`presentarse()` y `calcular_salario()`. Sin embargo, cada clase puede aplicar su
propia fórmula.

## Polimorfismo

El polimorfismo permite ejecutar el mismo método sobre objetos de distintas
clases y obtener un comportamiento apropiado para cada objeto.

```python
empleados = [
    EmpleadoFijo("Ana", 2200),
    EmpleadoPorHoras("Luis", 80, 18),
    Becario("Marina", 600),
]

for empleado in empleados:
    print(empleado.presentarse())
    print(f"Salario: {empleado.calcular_salario()} euros")
```

Salida aproximada:

```text
Soy Ana
Salario: 2200 euros
Soy Luis
Salario: 1440 euros
Soy Marina
Salario: 600 euros
```

El bucle no necesita saber qué clase concreta contiene `empleado`. Solo necesita
que el objeto sea compatible con la interfaz de `Empleado`: debe tener
`calcular_salario()`.

## Método abstracto con lógica común

Una clase abstracta no tiene que limitarse a declarar métodos vacíos. También
puede implementar parte del comportamiento y reutilizarlo:

```python
class Empleado(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def calcular_salario(self):
        pass

    def mostrar_resumen(self):
        salario = self.calcular_salario()
        return f"{self.presentarse()}: {salario} euros"

    def presentarse(self):
        return f"Soy {self.nombre}"
```

`mostrar_resumen()` está disponible en todas las clases hijas. Cuando se ejecuta,
llama a la implementación de `calcular_salario()` correspondiente al objeto
concreto.

## Clase abstracta o clase normal

Usar una clase abstracta es apropiado cuando las clases hijas deben garantizar
ciertos métodos.

- Usa una **clase normal** si la clase padre puede usarse por sí sola y no
  necesita métodos obligatorios.
- Usa una **clase abstracta** si la clase representa una categoría general y
  varias clases hijas deben implementar operaciones propias.
- Usa una **interfaz conceptual** si solo importa que distintos objetos
  compartan métodos. Python permite esto mediante [duck typing](#duck-typing),
  aunque las clases abstractas hacen el contrato más explícito.

## Duck typing

Python no exige declarar que una clase hereda de otra para que sus objetos
puedan usarse de la misma forma:

```python
class Factura:
    def calcular_total(self):
        return 120


def mostrar_total(cobro):
    print(cobro.calcular_total())


mostrar_total(Factura())
```

En este ejemplo no existe herencia. La función funciona porque el objeto acepta
la operación que necesita: tiene `calcular_total()`. Este comportamiento se
llama **duck typing**: si el objeto sabe realizar la operación esperada, puede
utilizarse.

Las clases abstractas son útiles cuando conviene declarar y comprobar
explícitamente ese conjunto mínimo de operaciones.

## Evitar decisiones comunes

### No hacer que la clase padre sea demasiado específica

Una clase `Vehiculo` puede tener `marca`, `modelo` y `acelerar()`. No conviene
añadir a la clase padre propiedades exclusivas de coches, como el número de
puertas, si solo algunos tipos de vehículo las poseen.

### No duplicar comportamiento compartido

Si varias clases repiten el mismo método, conviene trasladarlo a la clase
padre.

### No abusar de la herencia

Una relación de herencia debe representar una relación «es un». Una
`CuentaBancaria` no debería heredar de `Cliente`, aunque ambos estén presentes
en la misma aplicación.

## Ejemplo completo

```python
from abc import ABC, abstractmethod


class Figura(ABC):
    @abstractmethod
    def calcular_area(self):
        pass

    def describir(self):
        return f"{type(self).__name__}: {self.calcular_area()}"


class Rectangulo(Figura):
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

    def calcular_area(self):
        return self.ancho * self.alto


class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio

    def calcular_area(self):
        import math
        return math.pi * self.radio ** 2


figuras = [
    Rectangulo(4, 3),
    Circulo(2),
]

for figura in figuras:
    print(figura.describir())
```

Aunque `Figura` no puede instanciarse, se utiliza como plantilla común:
garantiza que `Rectangulo` y `Circulo` implementen `calcular_area()`. El código
cliente no necesita escribir una instrucción `if` para decidir qué operación
realizar en cada clase.

## Ejercicio

1. Crea una clase abstracta `Notificacion` con un método abstracto
   `enviar(mensaje)`.
2. Añade las clases `NotificacionEmail` y `NotificacionSMS`.
3. Cada clase debe imprimir un mensaje distinto al llamar a `enviar()`.
4. Guarda varias notificaciones en una lista.
5. Recorre la lista y llama a `enviar("Tarea completada")` en cada elemento.
6. Comprueba que ocurre si intentas crear directamente una instancia de
   `Notificacion`.

Al terminar, se habrá aplicado una única interfaz a objetos diferentes:
`Notificacion` define qué operaciones son necesarias, las clases hijas deciden
cómo realizarlas y el bucle utiliza el polimorfismo sin conocer todos los tipos
concretos.
