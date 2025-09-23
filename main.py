import pyodbc

#Clase País
class Pais:
    id_pais: int = 0
    nombre_pais: str = None

    # Métodos get-set para id_pais
    def GetIdPais(self) -> int:
        return self.id_pais
    
    def SetIdPais(self, value: int) -> None:
        self.id_pais = value

    # Métodos get-set para nombre_pais
    def GetNombrePais(self) -> str:
        return self.nombre_pais
    
    def SetNombrePais(self, value: str) -> None:
        self.nombre_pais = value

#Clase comida
class Comida:
    id: int = 0
    nombre: str = None
    pais: str = None

    # Métodos get-set
    def GetId(self) -> int:
        return self.id

    def SetId(self, value: int) -> None:
        self.id = value

    def GetNombre(self) -> str:
        return self.nombre

    def SetNombre(self, value: str) -> None:
        self.nombre = value

    def GetPais(self) -> str:
        return self.pais

    def SetPais(self, value: str) -> None:
        self.pais = value

class Conexion:
    cadena_conexion: str = """
            Driver={MySQL ODBC 9.4 Unicode Driver};
            Server=localhost;
            Database=gastronomia;
            PORT=3306;
            user=user_python1;
            password=1234""";

    def CargarPaises(self) -> list:
        conexion = pyodbc.connect(self.cadena_conexion)
        consulta: str = """ SELECT id_pais, nombre_pais FROM paises order by id_pais asc; """
        cursor = conexion.cursor()
        cursor.execute(consulta)

        lista: list = []
        for elemento in cursor:
            entidad: Pais = Pais()
            entidad.SetIdPais(elemento[0])
            entidad.SetNombrePais(elemento[1])
            lista.append(entidad)

        cursor.close()

        # Imprimir resultados
        for pais in lista:
            print(str(pais.GetIdPais()) + ", " + pais.GetNombrePais())

        return lista
    
    # Método para devolver comidas con su país
    def CargarComidas(self) -> None:
        conexion = pyodbc.connect(self.cadena_conexion)

        consulta: str = """
            SELECT c.id_comida, c.nombre_comida AS comida, p.nombre_pais AS pais
            FROM comidas_tipicas c
            INNER JOIN paises p ON c.id_pais = p.id_pais;
        """

        cursor = conexion.cursor()
        cursor.execute(consulta)

        lista2: list = []
        for elemento in cursor:
            comida: Comida = Comida()
            comida.SetId(elemento[0])
            comida.SetNombre(elemento[1])
            comida.SetPais(elemento[2])
            lista2.append(comida)

        cursor.close()

        # Mostrar resultados
        for c in lista2:
            print(str(c.GetId()) + " | " + c.GetNombre() + " -> " + c.GetPais())

        return lista2
    
    # INSERTAR nueva comida
    def InsertarComida(self, nombre: str, id_pais: int) -> None:
        conexion = pyodbc.connect(self.cadena_conexion)
        cursor = conexion.cursor()
        consulta: str = """
            INSERT INTO comidas_tipicas (nombre_comida, id_pais)
            VALUES (?, ?);
        """
        cursor.execute(consulta, (nombre, id_pais))
        conexion.commit()
        cursor.close()
        print(f"Comida '{nombre}' insertada con éxito.")

    # ACTUALIZAR comida por id
    def ActualizarComida(self, id_comida: int, nuevo_nombre: str, nuevo_id_pais: int) -> None:
        conexion = pyodbc.connect(self.cadena_conexion)
        cursor = conexion.cursor()
        consulta: str = """
            UPDATE comidas_tipicas
            SET nombre_comida = ?, id_pais = ?
            WHERE id_comida = ?;
        """
        cursor.execute(consulta, (nuevo_nombre, nuevo_id_pais, id_comida))
        conexion.commit()
        cursor.close()
        print(f"Comida con id={id_comida} actualizada.")

    # ELIMINAR comida por id
    def EliminarComida(self, id_comida: int) -> None:
        conexion = pyodbc.connect(self.cadena_conexion)
        cursor = conexion.cursor()
        consulta: str = """
            DELETE FROM comidas_tipicas
            WHERE id_comida = ?;
        """
        cursor.execute(consulta, (id_comida,))
        conexion.commit()
        cursor.close()
        print(f"Comida con id={id_comida} eliminada.")


conexion = Conexion()
print("Conexión a base de datos MySQL")
print("==============================")
print("Imprimiendo paises")
conexion.CargarPaises()
print("=========================================")
print("Imprimiendo paises y platos de comida tipica")
conexion.CargarComidas()
print("=========================================")
#print("Ejecutando CRUD")
#conexion.InsertarComida("Ajiaco",2)
#conexion.ActualizarComida(17, "Updated", 1)
#conexion.EliminarComida(11)
