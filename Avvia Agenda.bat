@echo off
echo.
echo  Avvio dell'Agenda Personale...
echo.

:: Vai nella cartella del progetto
cd /d "C:\Users\Francesco Merlin\Desktop\Documents\Python\agenda_personale"

:: Attiva l'ambiente Conda usando il percorso corretto
call "C:\Users\fmerl\miniconda3\condabin\conda.bat" activate agenda

:: Avvia il browser automaticamente
start "" http://127.0.0.1:5000

:: Avvia Flask usando il Python dell'ambiente
call "C:\Users\fmerl\miniconda3\envs\agenda\python.exe" app.py

:: Mantieni aperta la finestra per vedere errori
echo.
echo  Agenda in esecuzione! Premi un tasto per fermare...
pause