from pydantic import BaseModel
from typing import List

from .usuario import Usuario

class Almacen(BaseModel):
    usuarios: List[Usuario]

    def usuario_exists(self, username: str) -> bool:
        """
        Check if a user with the given username exists in the almacen.

        Args:
            username (str): The username to check for.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return any(usuario.username == username for usuario in self.usuarios)