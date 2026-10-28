@echo off
REM Build GFD_essentials.pdf from GFD_essentials.tex (pdflatex + bibtex)
cd /d "%~dp0"

echo Running pdflatex (pass 1)...
pdflatex -interaction=nonstopmode GFD_essentials.tex
if errorlevel 1 exit /b 1

echo Running bibtex...
bibtex GFD_essentials
if errorlevel 1 exit /b 1

echo Running pdflatex (pass 2)...
pdflatex -interaction=nonstopmode GFD_essentials.tex
if errorlevel 1 exit /b 1

echo Running pdflatex (pass 3)...
pdflatex -interaction=nonstopmode GFD_essentials.tex
if errorlevel 1 exit /b 1

echo Done. Output: GFD_essentials.pdf
exit /b 0
