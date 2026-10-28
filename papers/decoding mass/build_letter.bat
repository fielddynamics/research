@echo off
REM ============================================================================
REM Build the Nelson 2026 letter (letter.pdf).
REM
REM Usage:
REM   build_letter.bat           Build the PDF only (assumes figures already
REM                             exist in this folder or in figures\).
REM   build_letter.bat --all     Regenerate all figures (Fig 1, 2, 3) by running
REM                             figures\generate_letter_figures.py, copy the
REM                             outputs here, then build the PDF with references.
REM                             Use --all when you changed the figure script or
REM                             want a full rebuild from scratch.
REM ============================================================================
cd /d "%~dp0"

if "%1"=="--all" (
  echo [build_letter] --all: regenerating figures...
  cd figures
  python generate_letter_figures.py
  if errorlevel 1 (
    echo [build_letter] generate_letter_figures.py failed.
    cd ..
    exit /b 1
  )
  cd ..
  echo [build_letter] Copying figures to letter directory...
  copy /Y figures\fig1_mw_m33.png .
  copy /Y figures\fig1_mw_m33.pdf .
  copy /Y figures\fig2_camb.png .
  copy /Y figures\fig2_camb.pdf .
  copy /Y figures\fig3_ngc3198.png .
  copy /Y figures\fig3_ngc3198.pdf .
  echo [build_letter] Building letter PDF...
)

pdflatex -interaction=nonstopmode letter.tex
if errorlevel 1 (echo [build_letter] First pdflatex failed. & exit /b 1)
bibtex letter
if errorlevel 1 (echo [build_letter] bibtex failed. & exit /b 1)
pdflatex -interaction=nonstopmode letter.tex
if errorlevel 1 (echo [build_letter] Second pdflatex failed. & exit /b 1)
pdflatex -interaction=nonstopmode letter.tex
if errorlevel 1 (echo [build_letter] Third pdflatex failed. & exit /b 1)

echo Done. letter.pdf in %~dp0
