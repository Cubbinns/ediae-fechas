# Decimal: números decimales exactos

El módulo `decimal` permite representar y operar con números decimales con
precisión controlada. Es especialmente útil en aplicaciones financieras,
facturas, precios, impuestos o porcentajes, donde los errores de redondeo
pueden provocar diferencias.

Los números `float` utilizan representación binaria. Aunque muestran valores
correctos en muchos casos, pueden introducir resultados inesperados:

```python
print(0.1 + 0.2)
```

Resultado:

```text
0.30000000000000004
```

Esta diferencia suele ser irrelevante en gráficos o cálculos científicos, pero
no debería aparecer al calcular dinero.

## Crear un Decimal

Para trabajar con números decimales exactos se importa `Decimal`:

```python
from decimal import Decimal
```

Lo más seguro es crear un `Decimal` a partir de una cadena de texto:

```python
precio = Decimal("19.95")
impuesto = Decimal("0.21")

print(precio)
print(impuesto)
```

También se puede convertir un entero:

```python
cantidad = Decimal(3)
```

No se recomienda crear un `Decimal` directamente desde un `float` si el valor
decimal debe ser exacto:

```python
Decimal(0.1)
```

Este objeto puede conservar la representación binaria aproximada del `float`.
El patrón recomendado es utilizar texto o convertir primero el `float` con
`str()` si no existe otra opción.

```python
Decimal(str(0.1))
```

## Operaciones básicas

`Decimal` admite las operaciones aritméticas habituales:

```python
precio = Decimal("19.95")
cantidad = Decimal("3")

subtotal = precio * cantidad
descuento = Decimal("5.00")
total = subtotal - descuento

print(subtotal)
print(total)
```

También se pueden dividir, sumar y calcular potencias:

```python
subtotal = Decimal("59.85")
iva = subtotal * Decimal("0.21")
total = subtotal + iva
parte = Decimal("10") / Decimal("4")

print(iva)
print(total)
print(parte)
```

Es importante utilizar `Decimal` en ambos operandos. Mezclar `Decimal` y
`float` normalmente produce un `TypeError`.

```python
Decimal("10") + 0.5
# TypeError: unsupported operand type(s)
```

Para operar con seguridad, convierte los dos valores al mismo tipo:

```python
Decimal("10") + Decimal("0.5")
```

## Comparar valores

Los objetos `Decimal` se pueden comparar con operadores habituales:

```python
precio = Decimal("19.95")
presupuesto = Decimal("20.00")

print(precio < presupuesto)
print(precio == Decimal("19.95"))
print(precio > presupuesto)
```

Salida:

```text
True
True
False
```

Al comparar cadenas o enteros, primero debe existir una conversión:

```python
Decimal("19.95") == Decimal("19.950")
```

Los ceros finales no cambian el valor decimal, por lo que la comparación
devuelve `True`.

## Precisión y redondeo

Las operaciones pueden verse afectadas por la precisión configurada en el
contexto decimal. Por defecto, Python utiliza 28 dígitos significativos:

```python
from decimal import getcontext

print(getcontext().prec)
```

Para cálculos con muchos decimales se puede cambiar temporalmente la precisión:

```python
from decimal import Decimal, getcontext

getcontext().prec = 6

resultado = Decimal("1") / Decimal("3")
print(resultado)
```

Salida:

```text
0.333333
```

Si una aplicación necesita cifras diferentes, conviene definir un contexto
local sin afectar a todo el programa:

```python
from decimal import Decimal, localcontext

with localcontext() as contexto:
    contexto.prec = 4
    resultado = Decimal("1") / Decimal("3")
    print(resultado)

print(Decimal("1") / Decimal("3"))
```

Dentro del bloque se utilizan cuatro dígitos de precisión. Después vuelve a
aplicarse el contexto anterior.

## Modos de redondeo

El método `quantize()` permite limitar un número a una cantidad determinada
de decimales:

```python
from decimal import Decimal, ROUND_HALF_UP

precio = Decimal("19.956")

precio_redondeado = precio.quantize(
    Decimal("0.01"),
    rounding=ROUND_HALF_UP,
)

print(precio_redondeado)
```

Salida:

```text
19.96
```

Los modos de redondeo más conocidos son:

| Constante | Comportamiento |
| --- | --- |
| `ROUND_HALF_UP` | Redondea hacia arriba al alcanzar 5 |
| `ROUND_HALF_EVEN` | Redondea al dígito par más cercano |
| `ROUND_DOWN` | Elimina los decimales sobrantes |
| `ROUND_UP` | Se aleja de cero al eliminar decimales |

En España, las aplicaciones comerciales suelen usar `ROUND_HALF_UP` para
redondeos humanos tradicionales, salvo que exista una norma contable distinta.

## Ejemplo con precios

Supongamos un producto con precio sin impuestos:

```python
from decimal import Decimal, ROUND_HALF_UP

precio = Decimal("24.99")
cantidad = Decimal("2")
tipo_iva = Decimal("0.21")

subtotal = precio * cantidad
iva = (subtotal * tipo_iva).quantize(
    Decimal("0.01"),
    rounding=ROUND_HALF_UP,
)
total = (subtotal + iva).quantize(
    Decimal("0.01"),
    rounding=ROUND_HALF_UP,
)

print(f"Subtotal: {subtotal} EUR")
print(f"IVA: {iva} EUR")
print(f"Total: {total} EUR")
```

Salida:

```text
Subtotal: 49.98 EUR
IVA: 10.50 EUR
Total: 60.48 EUR
```

El impuesto se calcula sobre el subtotal y después se redondea a céntimos.

## Porcentajes

Un porcentaje se puede expresar como una fracción decimal:

```python
from decimal import Decimal

precio = Decimal("80")
porcentaje_descuento = Decimal("15")

descuento = precio * porcentaje_descuento / Decimal("100")
precio_final = precio - descuento

print(descuento)
print(precio_final)
```

Resultado:

```text
12
68
```

Otra opción consiste en almacenar el porcentaje como `0.15`:

```python
descuento = precio * Decimal("0.15")
```

Las dos formas son válidas; conviene elegir una y mantenerla de manera
consistente en todo el programa.

## Conversión desde texto

Las entradas de usuarios suelen llegar como cadenas:

```python
precio_texto = "19.95"
precio = Decimal(precio_texto)
```

Una cadena no válida produce una excepción:

```python
from decimal import Decimal, InvalidOperation

try:
    precio = Decimal("diecinueve euros")
except InvalidOperation:
    print("El precio no tiene un formato válido")
```

El tratamiento de entradas es importante, ya que los datos externos no pueden
convertirse automáticamente en valores seguros.

## Convertir a texto

`str()` devuelve una representación adecuada para mostrar o guardar:

```python
precio = Decimal("19.95")
print(str(precio))
```

Para mostrar siempre dos cifras decimales se puede usar `format()`:

```python
precio = Decimal("19.5")
print(format(precio, ".2f"))
```

Salida:

```text
19.50
```

Esta operación es principalmente visual. El objeto todavía contiene su valor
decimal original.

## Decimal y Pydantic

Pydantic puede usar `Decimal` como tipo de un modelo:

```python
from decimal import Decimal
from pydantic import BaseModel


class Factura(BaseModel):
    concepto: str
    importe: Decimal
```

Se puede crear una factura con una cadena:

```python
factura = Factura(
    concepto="Suscripción",
    importe="19.95",
)

print(factura.importe)
print(type(factura.importe).__name__)
```

Pydantic conserva el valor como `Decimal`, en lugar de convertirlo
automáticamente a `float`.

## Decimal y JSON

El tipo `Decimal` no forma parte del formato JSON estándar y puede necesitar
una conversión antes de guardar los datos:

```python
importe = Decimal("19.95")
importe_json = str(importe)

print(importe_json)
print(type(importe_json).__name__)
```

Al leer el dato se puede volver a convertir:

```python
importe_recuperado = Decimal(importe_json)
```

Para mantener la precisión, conviene guardar el número como cadena o como
parte entera y decimales separadas, según el formato elegido.

## Errores habituales

### Usar float para dinero

```python
precio = 0.1
impuesto = 0.2

print(precio + impuesto)
```

En cálculos financieros puede aparecer una representación binaria innecesaria.
Utiliza cadenas al crear objetos `Decimal`.

### Mezclar Decimal y float

Evita operaciones como `Decimal("10") * 0.21`. Convierte los valores a
`Decimal` antes de operar:

```python
Decimal("10") * Decimal("0.21")
```

### Olvidar el redondeo

Una división puede producir muchos decimales:

```python
Decimal("10") / Decimal("3")
```

Si el resultado representa dinero, aplica un redondeo explícito con
`quantize()` al producirlo.

### Operar antes de validar

Las entradas externas pueden contener texto, espacios o símbolos. Valida y
convierte el dato antes de realizar operaciones para evitar excepciones o
cálculos incorrectos.

## Ejercicio

Crea un pequeño programa para calcular el total de una factura:

1. Crea el precio unitario con `Decimal("12.50")`.
2. Crea la cantidad con `Decimal("3")`.
3. Calcula el subtotal.
4. Calcula el IVA al 21 %.
5. Redondea el IVA y el total a dos decimales.
6. Muestra cada importe con dos cifras decimales.

Solución de apoyo:

```python
from decimal import Decimal, ROUND_HALF_UP

precio = Decimal("12.50")
cantidad = Decimal("3")
tipo_iva = Decimal("0.21")

subtotal = precio * cantidad
iva = (subtotal * tipo_iva).quantize(
    Decimal("0.01"),
    rounding=ROUND_HALF_UP,
)
total = (subtotal + iva).quantize(
    Decimal("0.01"),
    rounding=ROUND_HALF_UP,
)

print(f"Subtotal: {format(subtotal, '.2f')} EUR")
print(f"IVA: {format(iva, '.2f')} EUR")
print(f"Total: {format(total, '.2f')} EUR")
```
