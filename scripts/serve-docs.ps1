# Preview the documentation site locally.
# Assembles the docs/ folder from the knowledge bundle, then runs `mkdocs serve`.
#
#   pip install -r requirements-docs.txt   # first time
#   ./scripts/serve-docs.ps1               # then open http://127.0.0.1:8000
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

Remove-Item -Recurse -Force docs -ErrorAction SilentlyContinue
New-Item -ItemType Directory docs | Out-Null
Copy-Item index.md, recipes, ingredients, knowledge, menus, shopping-lists, calendars `
    -Destination docs -Recurse

mkdocs serve
