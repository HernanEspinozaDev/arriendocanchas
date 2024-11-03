import os

def print_tree(root_path, exclude_dirs=None, prefix='', lines=None):
    if exclude_dirs is None:
        exclude_dirs = []
    if lines is None:
        lines = []

    # Obtener todos los elementos en el directorio actual
    try:
        items = sorted(os.listdir(root_path))
    except PermissionError:
        # Si no se tiene permiso para acceder a un directorio, se omite
        return lines

    # Filtrar los elementos excluidos
    items = [item for item in items if item not in exclude_dirs]

    # Iterar sobre los elementos
    for index, item in enumerate(items):
        path = os.path.join(root_path, item)
        connector = '├── ' if index < len(items) - 1 else '└── '

        # Añadir el elemento con el prefijo adecuado
        lines.append(prefix + connector + item)

        # Si el elemento es un directorio y no está en la lista de exclusión, recursivamente imprimir su contenido
        if os.path.isdir(path) and item not in exclude_dirs:
            extension = '│   ' if index < len(items) - 1 else '    '
            print_tree(path, exclude_dirs, prefix + extension, lines)

    return lines

def main():
    # Ruta raíz de tu proyecto
    root_project = 'arriendo_canchas'

    # Directorios a excluir
    exclude = ['venv', '__pycache__']

    if not os.path.exists(root_project):
        print(f"La ruta especificada '{root_project}' no existe.")
        return

    # Generar la estructura del árbol
    tree_lines = [root_project + '/']
    tree_lines += print_tree(root_project, exclude)

    # Especificar el nombre del archivo de salida
    output_file = 'estructura_proyecto.txt'

    # Escribir la estructura en el archivo de texto
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in tree_lines:
            f.write(line + '\n')

    print(f"La estructura de directorios se ha guardado en '{output_file}'.")

if __name__ == "__main__":
    main()
