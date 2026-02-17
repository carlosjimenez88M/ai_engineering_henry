# Instalar Make en Windows, Linux y macOS

`make` permite convertir comandos largos en flujos reproducibles.
Para un curso tecnico, esto reduce errores manuales.

## 1. Verificar si ya lo tienes

```bash
make --version
```

Si imprime version, no necesitas instalarlo.

## 2. macOS

### Opcion recomendada

```bash
xcode-select --install
```

Esto instala Command Line Tools, incluyendo `make`.

### Opcion alternativa (Homebrew)

```bash
brew install make
```

En algunos casos el binario se llama `gmake`.

## 3. Linux

### Debian / Ubuntu

```bash
sudo apt update
sudo apt install -y make
```

### Fedora / RHEL

```bash
sudo dnf install -y make
```

### Arch Linux

```bash
sudo pacman -S make
```

## 4. Windows

Recomendacion profesional: usar WSL2 para desarrollo Python.

### Opcion A (recomendada): WSL2

1. Instala WSL2.
2. Abre Ubuntu en WSL.
3. Sigue pasos de Linux (apt).

### Opcion B: Windows nativo con package manager

Con Chocolatey:

```powershell
choco install make
```

Con Scoop:

```powershell
scoop install make
```

Con Winget (si esta disponible en tu catalogo):

```powershell
winget search make
winget install <ID-del-paquete>
```

## 5. Validacion final

```bash
make --version
```

Si falla, revisa PATH de tu shell.
