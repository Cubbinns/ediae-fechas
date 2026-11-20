# Arrow: fechas fáciles

Arrow es una biblioteca para crear, comparar y transformar fechas y horas.
El proyecto ya declara `arrow>=1.4.0`, aunque todavía no hay código que lo
utilice directamente.

## Fecha y hora actual

```python
import arrow

ahora = arrow.now()
print(ahora.format("YYYY-MM-DD"))
print(ahora.format("DD/MM/YYYY HH:mm"))
```

`format()` recibe una cadena de formato propia de Arrow.

## Crear una fecha

```python
import arrow

inicio = arrow.get("2027-07-01", "YYYY-MM-DD")
fin = arrow.get("2027-07-10", "YYYY-MM-DD")
```

Las cadenas de fecha se pueden convertir a objetos más útiles que simples
textos.

## Operaciones con fechas

```python
import arrow

inicio = arrow.get("2027-07-01", "YYYY-MM-DD")
fin = inicio.shift(days=9)

print(fin.format("YYYY-MM-DD"))  # 2027-07-10
print(inicio < fin)
```

`shift()` crea una nueva fecha desplazada sin modificar el objeto original.

## Intervalos

Para recorrer un periodo:

```python
import arrow

inicio = arrow.get("2027-07-01", "YYYY-MM-DD")
fin = arrow.get("2027-07-10", "YYYY-MM-DD")

for dia in arrow.Arrow.range("day", inicio, fin):
    print(dia.format("YYYY-MM-DD"))
```

## Convertir desde Python

Arrow puede envolver objetos estándar de Python:

```python
from datetime import date
import arrow

vacacion = date(2027, 7, 1)
flecha = arrow.get(vacacion)
print(flecha.format("YYYY-MM-DD"))
```

Pydantic utiliza `datetime.date` en el modelo `Usuario`, mientras que Arrow
proporciona herramientas cómodas para construir y mostrar esas fechas.

## Precauciones

- Decide siempre si trabajas con fecha, hora o zona horaria.
- Al leer fechas externas, valida primero el formato.
- Guarda fechas con formatos compatibles e inequívocos, como ISO.
- Arrow no sustituye a Pydantic: puede crear fechas, pero Pydantic puede
  validar y asegurar el tipo que recibe el modelo.

## Ejercicio

Calcula una fecha final nueve días después del 1 de julio de 2027 y recórrela
desde el inicio hasta el final. Intenta hacer que el formato mostrado sea
`día/mes/año`.
