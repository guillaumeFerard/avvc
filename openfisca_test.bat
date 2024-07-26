@echo off
call %CONDA_PATH%\Scripts\activate.bat test_openfisca

pause
call openfisca test -c openfisca_avvc openfisca_avvc/tests

cmd /k
pause