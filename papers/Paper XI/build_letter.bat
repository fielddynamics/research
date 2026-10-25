@echo off
echo Building PDF (pass 1 of 2)...
pdflatex -interaction=nonstopmode "letter.tex"
echo.
echo Building PDF (pass 2 of 2 - resolving references)...
pdflatex -interaction=nonstopmode "letter.tex"
echo.
echo Build complete.
pause
