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
    echo Building supplementary scheme proof...
    pushd Supplementary
    pdflatex -interaction=nonstopmode supplementary_scheme_proof.tex
    pdflatex -interaction=nonstopmode supplementary_scheme_proof.tex
    echo Built: supplementary_scheme_proof.pdf

    echo.
    echo Building supplementary signature to frame...
    pdflatex -interaction=nonstopmode supplementary_signature_to_frame.tex
    pdflatex -interaction=nonstopmode supplementary_signature_to_frame.tex
    echo Built: supplementary_signature_to_frame.pdf
    popd

    echo.
    echo All builds complete.
) else (
    echo.
    echo Letter only. Use --all to build cover letter and supplementary documents.
)

pause
