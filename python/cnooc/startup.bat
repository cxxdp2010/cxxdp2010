@echo.
cd /d e:\CnoocService
python CnoocService.py --startup auto install
python CnoocService.py restart
@echo.
@echo.
@pause >nul
exit