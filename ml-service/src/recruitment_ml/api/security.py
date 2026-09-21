"""Autenticacion de servicio a servicio.

La Fase 16 pone a Laravel a consumir este servicio por red interna. Un token
compartido es el mecanismo proporcionado al problema: los dos extremos son
componentes del mismo despliegue, no terceros, y no hay usuarios que
autenticar aqui -- el boundary de aplicacion sigue siendo Laravel.

Tres decisiones:

- **El token vive solo en el entorno.** Nunca en el codigo ni en el
  repositorio. Sin variable definida la autenticacion queda desactivada, que es
  lo razonable en desarrollo local; el arranque lo deja anotado en el log para
  que nadie lo confunda con estar protegido.
- **La comparacion es en tiempo constante.** `hmac.compare_digest` evita que el
  tiempo de respuesta filtre cuantos caracteres del token son correctos.
- **`/health` queda abierto.** Es una sonda de vida: responde si el proceso
  esta vivo y si hay modelo cargado, sin rutas, versiones de bibliotecas ni
  nada del experimento. Pedirle token complicaria los chequeos del despliegue
  sin proteger nada que importe.

Esto **no** convierte al servicio en algo publicable: sigue siendo experimental
y debe permanecer en localhost o en la red interna.
"""

from __future__ import annotations

import hmac
import logging
import os

from fastapi import Header, HTTPException, status

LOGGER = logging.getLogger("recruitment_ml.api")

#: Variable de entorno que porta el secreto compartido.
TOKEN_ENV = "RECRUITMENT_ML_INTERNAL_TOKEN"

#: Cabecera que lo transporta.
TOKEN_HEADER = "X-Internal-Token"

UNAUTHORIZED_MESSAGE = "Credencial de servicio ausente o invalida."


def configured_token() -> str | None:
    """Token configurado, o `None` si la autenticacion esta desactivada."""
    token = os.environ.get(TOKEN_ENV, "").strip()
    return token or None


def authentication_enabled() -> bool:
    return configured_token() is not None


def require_internal_token(
    x_internal_token: str | None = Header(default=None, alias=TOKEN_HEADER),
) -> None:
    """Exige el token compartido en las rutas del modelo.

    Sin token configurado no comprueba nada: el servicio queda abierto en la
    red donde este, que es lo que ocurre hoy en desarrollo.
    """
    expected = configured_token()
    if expected is None:
        return

    if x_internal_token is None or not hmac.compare_digest(x_internal_token, expected):
        # Ni el valor recibido ni el esperado llegan al log: uno es un secreto
        # y el otro seria un regalo para quien esta probando combinaciones.
        LOGGER.warning("credencial de servicio rechazada")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UNAUTHORIZED_MESSAGE,
        )
