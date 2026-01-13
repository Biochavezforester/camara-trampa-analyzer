import os
from pathlib import Path

# Ruta a probar
test_path = r"D:\JagueyesMay-Nov2025"

print("=" * 60)
print("DIAGNÓSTICO DE RUTA")
print("=" * 60)
print(f"\nRuta a probar: {test_path}")
print(f"\nTipo de objeto: {type(test_path)}")

# Convertir a Path
path_obj = Path(test_path)
print(f"\nPath object: {path_obj}")
print(f"Path absoluto: {path_obj.absolute()}")

# Verificar existencia
print(f"\n¿Existe? {path_obj.exists()}")
print(f"¿Es directorio? {path_obj.is_dir()}")

# Intentar con os.path
print(f"\nos.path.exists(): {os.path.exists(test_path)}")
print(f"os.path.isdir(): {os.path.isdir(test_path)}")

# Listar unidades disponibles
print("\n" + "=" * 60)
print("UNIDADES DISPONIBLES:")
print("=" * 60)
import string
from pathlib import Path

for letter in string.ascii_uppercase:
    drive = f"{letter}:\\"
    if Path(drive).exists():
        print(f"✅ {drive} - Disponible")
        # Intentar listar contenido
        try:
            items = list(Path(drive).iterdir())
            print(f"   Contiene {len(items)} elementos")
        except PermissionError:
            print(f"   ⚠️ Sin permisos para listar")
        except Exception as e:
            print(f"   ❌ Error: {e}")

# Si D:\ existe, intentar listar su contenido
print("\n" + "=" * 60)
print("CONTENIDO DE D:\\")
print("=" * 60)
if Path("D:\\").exists():
    try:
        for item in Path("D:\\").iterdir():
            print(f"  - {item.name} ({'DIR' if item.is_dir() else 'FILE'})")
    except Exception as e:
        print(f"❌ Error al listar D:\\: {e}")
else:
    print("❌ D:\\ no existe o no está accesible")
