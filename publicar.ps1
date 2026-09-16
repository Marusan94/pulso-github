#Requires -Version 5.1
<#
.SYNOPSIS
  Publica Pulso GitHub: push a GitHub + deploy en Vercel + variables.
.DESCRIPTION
  Ejecutar por pasos desde PowerShell:
    powershell -ExecutionPolicy Bypass -File .\publicar.ps1
  Antes: crea el repo VACÍO en github.com y pega su URL en $RepoUrl.
  El login de Vercel es interactivo (se abre el navegador una vez).
#>

$ErrorActionPreference = 'Stop'
$RepoDir = 'C:\Users\USUARIO\github-ranking'
$RepoUrl = 'https://github.com/TU-USUARIO/pulso-github.git'  # <-- CAMBIAR por tu repo

Set-Location $RepoDir

function Pausa($msg) {
  Write-Host ''
  Write-Host $msg -ForegroundColor Yellow
  Read-Host 'Pulsa ENTER para continuar (Ctrl+C para salir)'
}

# ---- Paso 0: verificaciones ----
Write-Host '== Paso 0: verificaciones ==' -ForegroundColor Cyan
git status --porcelain
python scripts/verify.py
if ($LASTEXITCODE -ne 0) { throw 'verify.py falló: no sigo' }
Pausa 'Todo verde. Siguiente: push a GitHub.'

# ---- Paso 1: GitHub ----
Write-Host '== Paso 1: GitHub ==' -ForegroundColor Cyan
$remoto = git remote
if (-not $remoto) {
  if ($RepoUrl -like '*TU-USUARIO*') { throw 'Edita $RepoUrl en este script con la URL de tu repo' }
  git remote add origin $RepoUrl
}
git push -u origin main
Pausa 'Push OK. Siguiente: Vercel (se abrirá el navegador para login).'

# ---- Paso 2: Vercel ----
Write-Host '== Paso 2: Vercel ==' -ForegroundColor Cyan
if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
  npm i -g vercel
}
vercel login
vercel --cwd docs --prod
Pausa 'Deploy OK. Siguiente: variables de entorno (opcional).'

# ---- Paso 3: variables en Vercel (requieren redeploy para aplicar) ----
Write-Host '== Paso 3: variables ==' -ForegroundColor Cyan
Write-Host 'Pega tu dominio (vacío para omitir):' -ForegroundColor Yellow
$site = Read-Host 'SITE_URL (ej. https://pulso-github.vercel.app)'
if ($site) { $site | vercel env add SITE_URL production }
Write-Host 'Umami: pega URL e ID (vacío para omitir analytics):' -ForegroundColor Yellow
$uu = Read-Host 'UMAMI_URL (ej. https://umami.midominio.com/script.js)'
if ($uu) { $uu | vercel env add UMAMI_URL production }
$ui = Read-Host 'UMAMI_ID'
if ($ui) { $ui | vercel env add UMAMI_ID production }
if ($site -or $uu -or $ui) { vercel --cwd docs --prod }

Write-Host ''
Write-Host 'Listo. En GitHub (Settings → Secrets/Variables → Actions) añade si aplica:' -ForegroundColor Cyan
Write-Host '  secrets/UMAMI_ID, vars/SITE_URL y vars/UMAMI_URL (GITHUB_TOKEN ya lo pone Actions)'
