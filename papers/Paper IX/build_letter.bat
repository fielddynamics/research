@echo off
echo Building letter.tex...
echo.

pdflatex letter.tex
if errorlevel 1 (
    echo.
    echo ERROR: First pdflatex pass failed.
    pause
    exit /b 1
)

echo.
echo First pass complete. Running second pass for references...
echo.

pdflatex letter.tex
if errorlevel 1 (
    echo.
    echo ERROR: Second pdflatex pass failed.
    pause
    exit /b 1
)

echo.
echo Build complete: letter.pdf
pause
