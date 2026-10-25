@echo off
cd /d "%~dp0"

pdflatex -interaction=nonstopmode letter.tex
pdflatex -interaction=nonstopmode letter.tex
echo.
echo Built: letter.pdf

if "%~1"=="--all" (
    echo.
    echo Building cover letter...
    pdflatex -interaction=nonstopmode cover_letter.tex
    pdflatex -interaction=nonstopmode cover_letter.tex
    echo Built: cover_letter.pdf

    echo.
    echo Building supplementary document...
    pushd Supplementary
    pdflatex -interaction=nonstopmode supplementary_tetb_fraction.tex
    pdflatex -interaction=nonstopmode supplementary_tetb_fraction.tex
    echo Built: supplementary_tetb_fraction.pdf
    popd

    echo.
    echo All builds complete.
) else (
    echo.
    echo Letter only. Use --all to build cover letter and supplementary document.
)

pause
