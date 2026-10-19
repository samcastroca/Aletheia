# Aletheia

Taller de videos matemáticos hechos con [ManimGX](https://github.com/academa-labs/manimgx): escenas
en Python con la API de Manim Community Edition, renderizadas en la GPU. Cada video vive en su
carpeta dentro de `videos/`.

## Instalar

Hace falta [uv](https://docs.astral.sh/uv/). Desde la raíz del repo:

```sh
uv sync
```

Crea `.venv` con Python 3.14, ManimGX, el type checker [ty](https://docs.astral.sh/ty/) y el paquete
`common/` (estilo y audio compartidos). No hace falta instalar `manim`, ffmpeg ni LaTeX.

## Renderizar

Con el script (Windows, PowerShell):

```powershell
./scripts/mgx.ps1 inspect proyeccion-estereografica   # storyboard y línea de tiempo, sin video
./scripts/mgx.ps1 draft   proyeccion-estereografica   # 1280x720 a 30 fps -> draft.mp4
./scripts/mgx.ps1 final   proyeccion-estereografica   # 1920x1080 a 60 fps
./scripts/mgx.ps1 present proyeccion-estereografica   # secciones como diapositivas
```

Si Windows bloquea el script: `powershell -ExecutionPolicy Bypass -File scripts/mgx.ps1 ...`.

O directamente:

```sh
uv run manimgx inspect videos/proyeccion-estereografica/scene.py
uv run manimgx render  videos/proyeccion-estereografica/scene.py
```

El MP4, los storyboards y los subtítulos se escriben junto a `scene.py` y no se versionan.

## Voz

La narración (`self.say`) usa fal.ai y cobra por carácter. La clave va en la variable de entorno
`FAL_KEY` (ver `.env.example`), nunca en un archivo. Lo narrado se guarda en `videos/<video>/voice/`
y se versiona: con esa carpeta, el video se vuelve a renderizar sin pagar y sin conexión.

## Estructura

```
common/      estilo (paleta, fondo) y audio sintetizado
videos/      un video por carpeta: scene.py, assets/, voice/
scripts/     mgx.ps1
docs/        ideas.md, el backlog de temas
```
