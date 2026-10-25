@echo off
echo Building sst_two_scale_jcap.tex (pass 1 of 2)...
pdflatex -interaction=nonstopmode sst_two_scale_jcap.tex
echo.
echo Building sst_two_scale_jcap.tex (pass 2 of 2)...
pdflatex -interaction=nonstopmode sst_two_scale_jcap.tex
echo.
echo Build complete.
pause
