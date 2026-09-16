# Esquema de la API

Base: `data/` del repositorio. Versionado por fecha en `data/history/<fecha>-top.json`
y `data/history/<fecha>-tre.json` (formato compacto: `n` nombre, `s` estrellas, `f` forks).

## `repos.json` / `trending.json`

| Campo | Tipo | Ejemplo |
|---|---|---|
| `fecha` | texto `AAAA-MM-DD` | `2026-09-14` |
| `ventana` | solo trending: rango de creación cubierto | `creados desde 2026-08-15` |
| `repos[].rank` | entero, puesto en su corte | `1` |
| `repos[].full_name` | texto `dueño/repo` | `facebook/react` |
| `repos[].description` | texto original (puede venir vacío) | `The library for...` |
| `repos[].descripcion_es` | texto en español con contexto | `Es una librería...` |
| `repos[].stars` / `repos[].forks` | enteros | `250439` |
| `repos[].language` | texto o `—` | `JavaScript` |
| `repos[].categoria` | `IA/LLM`, `Frontend`, `Educación/Recursos`, `Backend/DevOps`, `Templates`, `Seguridad`, `DevTools` | — |
| `repos[].license` | SPDX o `—` | `MIT` |
| `repos[].tipo` | `herramienta/app`, `awesome-list`, `educativo`, `framework/librería` | — |
| `repos[].pushed_at` / `repos[].created_at` | texto `AAAA-MM-DD` | `2026-09-14` |
| `repos[].archived` | booleano | `false` |
| `repos[].url` | enlace GitHub | `https://github.com/...` |

Ejemplo: `fetch("data/history/2026-09-14-top.json").then(r => r.json())`.
