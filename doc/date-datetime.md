# Date y datetime: trabajar con fechas y horas

Python incluye en el módulo `datetime` las clases que permiten representar
fechas, horas y combinaciones de ambas. Son objetos, no simples textos, por
lo que permiten comparar fechas, calcular diferencias y modificar partes de
una fecha.

En este proyecto el modelo `Usuario` utiliza `date` para almacenar las fechas
de vacaciones.

```python
from datetime import date
```

Las clases principales son:

- `date`: representa un día del calendario, pero no una hora.
- `datetime`: representa una fecha y una hora.
- `time`: representa una hora sin fecha.
- `timedelta`: representa una duración o diferencia de tiempo.
- `timezone`: representa una zona horaria.

## Fecha con `date`

Un objeto `date` contiene año, mes y día:

```python
from datetime import date

vacacion = date(2027, 7, 1)

print(vacacion)
print(vacacion.year)
print(vacacion.month)
print(vacacion.day)
```

Salida:

```text
2027-07-01
2027
7
1
```

En el ejemplo anterior, los números se pasan en el orden `año, mes, día`.

## Obtener la fecha actual

`date.today()` devuelve la fecha local actual:

```python
from datetime import date

hoy = date.today()
print(hoy)
```

No incluye la hora actual.

## Fecha y hora con `datetime`

Un objeto `datetime` contiene fecha y hora:

```python
from datetime import datetime

reunion = datetime(2027, 7, 1, 10, 30)

print(reunion)
print(reunion.year)
print(reunion.hour)
print(reunion.minute)
```

La hora se expresa con el formato de 24 horas. Por tanto, las 6 de la tarde se
representan como `18`.

También se pueden añadir segundos y microsegundos:

```python
desde = datetime(2027, 7, 1, 10, 30, 45)
print(desde)
```

## Obtener fecha y hora actuales

`datetime.now()` devuelve la fecha y hora locales:

```python
from datetime import datetime

ahora = datetime.now()
print(ahora)
```

`datetime.today()` realiza una operación equivalente en la mayoría de los
casos.

Si solo se necesita la hora UTC actual:

```python
from datetime import datetime, timezone

ahora_utc = datetime.now(timezone.utc)
print(ahora_utc)
```

## Diferencia entre `date` y `datetime`

La principal diferencia es el nivel de información:

```python
from datetime import date, datetime

solo_fecha = date(2027, 7, 1)
fecha_y_hora = datetime(2027, 7, 1, 10, 30)
```

- `solo_fecha` representa todo el día 1 de julio de 2027.
- `fecha_y_hora` representa las 10:30 de ese día.

No conviene mezclar ambos tipos como si fueran equivalentes en operaciones
complejas. Cuando solo interesa un día, utiliza `date`; cuando importa la hora,
utiliza `datetime`.

## Convertir `datetime` a `date`

El método `date()` obtiene únicamente la fecha de un `datetime`:

```python
from datetime import datetime

ahora = datetime.now()
hoy = ahora.date()

print(ahora)
print(hoy)
```

Al combinarlo con Pydantic se puede pasar una fecha a un campo de tipo `date`:

```python
from datetime import datetime

fecha = datetime(2027, 7, 1, 10, 30).date()
```

## Comparar fechas

Los objetos de fecha se pueden comparar con los operadores habituales:

```python
from datetime import date

inicio = date(2027, 7, 1)
fin = date(2027, 7, 10)

print(inicio < fin)
print(inicio == fin)
print(inicio > fin)
```

Salida:

```text
True
False
False
```

Python puede comparar objetos `datetime` entre sí siguiendo el mismo criterio:
primero la fecha y, después, la hora.

## Calcular diferencias

Restar dos fechas produce un objeto `timedelta`:

```python
from datetime import date

inicio = date(2027, 7, 1)
fin = date(2027, 7, 10)

diferencia = fin - inicio

print(diferencia)
print(diferencia.days)
```

Salida:

```text
9 days, 0:00:00
9
```

Con `datetime` también se puede calcular una duración:

```python
from datetime import datetime

inicio = datetime(2027, 7, 1, 9, 0)
fin = datetime(2027, 7, 1, 12, 30)

diferencia = fin - inicio

print(diferencia.total_seconds())
print(diferencia.total_seconds() / 3600)
```

La segunda operación convierte el resultado de segundos a horas.

## Añadir o quitar tiempo

`timedelta` representa una duración. Puede utilizarse para desplazar una fecha
o una fecha y hora:

```python
from datetime import date, timedelta

hoy = date(2027, 7, 1)
dos_dias_despues = hoy + timedelta(days=2)
una_semana_antes = hoy - timedelta(weeks=1)

print(dos_dias_despues)
print(una_semana_antes)
```

También admite horas, minutos y segundos:

```python
from datetime import datetime, timedelta

ahora = datetime(2027, 7, 1, 10, 30)
mas_treinta_minutos = ahora + timedelta(minutes=30)

print(mas_treinta_minutos)
```

Las operaciones `+` y `-` crean un nuevo objeto. No modifican el objeto
original.

## Crear fechas desde texto

Un texto como `"2027-07-01"` no es una fecha hasta que se convierte a `date`.
Para el formato ISO, el método `fromisoformat()` es directo:

```python
from datetime import date, datetime

vacacion = date.fromisoformat("2027-07-01")
reunion = datetime.fromisoformat("2027-07-01T10:30:00")

print(vacacion)
print(reunion)
```

`datetime.fromisoformat()` también acepta una combinación separada por un
espacio:

```python
reunion = datetime.fromisoformat("2027-07-01 10:30:00")
```

### Formatos personalizados

Si la fecha tiene otro formato, `strptime()` permite describir su estructura:

```python
from datetime import datetime

texto = "01/07/2027 10:30"
reunion = datetime.strptime(texto, "%d/%m/%Y %H:%M")

print(reunion)
```

Los códigos de formato más comunes son:

| Código | Significado |
| --- | --- |
| `%Y` | Año con cuatro dígitos |
| `%m` | Mes |
| `%d` | Día |
| `%H` | Hora en formato de 24 horas |
| `%M` | Minutos |
| `%S` | Segundos |

Es importante que el patrón coincida exactamente con el texto recibido.

## Convertir fechas a texto

El método `isoformat()` produce texto con formatos estándar:

```python
from datetime import date, datetime

vacacion = date(2027, 7, 1)
reunion = datetime(2027, 7, 1, 10, 30)

print(vacacion.isoformat())
print(reunion.isoformat())
```

Salida:

```text
2027-07-01
2027-07-01T10:30:00
```

Para un formato personalizado se utiliza `strftime()`:

```python
texto = reunion.strftime("%d/%m/%Y %H:%M")
print(texto)
```

Salida:

```text
01/07/2027 10:30
```

Conviene guardar o intercambiar datos con formatos ISO como
`2027-07-01T10:30:00` cuando sea posible. Son fáciles de reconocer y evitan
ambigüedades entre formatos como `01/07/2027` y `07/01/2027`.

## Modificar una fecha

Los objetos no se modifican directamente. Los métodos `replace()` crean una
nueva versión:

```python
from datetime import date, datetime

vacacion = date(2027, 7, 1)
otra_vacacion = vacacion.replace(day=15)

reunion = datetime(2027, 7, 1, 10, 30)
reunion_mas_tarde = reunion.replace(hour=11)

print(otra_vacacion)
print(reunion_mas_tarde)
```

El objeto original sigue conservando su valor anterior.

## Combinar fecha y hora

`combine()` crea un `datetime` a partir de un `date` y una hora de tipo `time`:

```python
from datetime import date, time, datetime

dia = date(2027, 7, 1)
hora = time(10, 30)

reunion = datetime.combine(dia, hora)
print(reunion)
```

## Fechas con zonas horarias

Un `datetime` puede ser **naive** o **aware**:

- Naive: no contiene información sobre su zona horaria.
- Aware: contiene información sobre su zona horaria.

```python
from datetime import datetime, timezone, timedelta

naive = datetime(2027, 7, 1, 10, 30)

aware = datetime(
    2027,
    7,
    1,
    10,
    30,
    tzinfo=timezone(timedelta(hours=2)),
)

print(naive)
print(aware)
```

Para evitar ambigüedades en aplicaciones con usuarios de distintas regiones,
conviene trabajar con UTC y convertir a la zona horaria local solo al mostrar
la información.

Python permite obtener instantes UTC con `timezone.utc`:

```python
from datetime import datetime, timezone

ahora_utc = datetime.now(timezone.utc)
print(ahora_utc)
```

## Uso con Pydantic

El modelo `Usuario` declara `vacaciones` como una lista de objetos `date`:

```python
from pydantic import BaseModel, Field
from datetime import date
from typing import List


class Usuario(BaseModel):
    username: str
    vacaciones: List[date] = Field(default_factory=list)
```

Pydantic puede convertir una cadena ISO en un objeto `date`:

```python
usuario = Usuario(
    username="Ana",
    vacaciones=["2027-07-01", "2027-07-10"],
)

for vacacion in usuario.vacaciones:
    print(type(vacacion).__name__, vacacion.isoformat())
```

Salida aproximada:

```text
date 2027-07-01
date 2027-07-10
```

También se pueden asignar objetos `date` directamente:

```python
usuario = Usuario(
    username="Ana",
    vacaciones=[date(2027, 7, 1)],
)
```

## Errores habituales

### Formato incorrecto

Si el texto no sigue el patrón indicado, `strptime()` lanzará
`ValueError`:

```python
from datetime import datetime

# Incorrecto si se utiliza el patrón "%d/%m/%Y"
datetime.strptime("2027-07-01", "%d/%m/%Y")
```

Antes de convertir datos externos, conviene comprobar o controlar la
excepción:

```python
try:
    reunion = datetime.strptime("01/07/2027", "%d/%m/%Y")
except ValueError:
    print("La fecha no tiene el formato esperado")
```

### Mezclar objetos naive y aware

Python no permite restar directamente un `datetime` con zona horaria de otro
sin zona horaria:

```python
fecha_utc = datetime.now(timezone.utc)
fecha_local_naive = datetime.now()

# Puede producir TypeError
diferencia = fecha_utc - fecha_local_naive
```

Conviene decidir un modelo de zonas horarias y mantenerlo de forma coherente.

### Confundir año y mes

Al crear una fecha manualmente hay que utilizar el orden `año, mes, día`:

```python
date(2027, 7, 1)  # 1 de julio de 2027
```

No es el mismo orden que muchos formatos locales muestran en un texto.

## Ejercicio

Crea un pequeño programa con los siguientes pasos:

1. Convierte el texto `"01/07/2027"` en un objeto `date`.
2. Convierte el texto `"2027-07-10"` con `date.fromisoformat()`.
3. Calcula cuántos días hay entre ambas fechas.
4. Crea una fecha diez días después del 1 de julio.
5. Convierte el resultado a formato `"día/mes/año"`.
6. Crea una `datetime` a las 10:30 y súmale 45 minutos.

Solución de apoyo:

```python
from datetime import date, datetime, timedelta

fecha_texto = datetime.strptime("01/07/2027", "%d/%m/%Y").date()
fecha_iso = date.fromisoformat("2027-07-10")

print(fecha_iso - fecha_texto)

fecha_final = fecha_texto + timedelta(days=10)
print(fecha_final.strftime("%d/%m/%Y"))

reunion = datetime(2027, 7, 1, 10, 30)
print(reunion + timedelta(minutes=45))
```
