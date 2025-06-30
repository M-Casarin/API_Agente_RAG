@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo         AGENTE RAG IP - EXECUTION SCRIPT
echo ==========================================
echo.

set STEPS=^
1:src/ingestion/main_ingest.py,^
2:src/ingestion/chunker.py,^
3:src/indexer/embed.py,^
4:src/indexer/faiss_indexer.py

for %%S in (%STEPS%) do (
    for /f "tokens=1,2 delims=:" %%A in ("%%S") do (
        echo [%%A/4] Ejecutando %%B...
        echo Comando: uv run python %%B
        uv run python %%B
        if !ERRORLEVEL! neq 0 (
            echo ERROR: Fallo en %%B
            pause
            exit /b !ERRORLEVEL!
        )
        echo  %%B completado exitosamente
        echo ""
        echo.

    )
)


echo ==========================================
echo      SE HA ACTUALIZADO EL RAG DE FORMA EXITOSA!
echo ==========================================
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
