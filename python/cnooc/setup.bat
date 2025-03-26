cd /d D:\CnoocService\lib
pip --version
python -m pip install --upgrade pip
pip install pywin32
pip install selenium
pip install apscheduler
cd /d D:\CnoocService
python CnoocService.py --startup auto install
python CnoocService.py restart
@echo.
@echo 已经完成
@echo.
@pause >nul
exit