# Requirements - harness_base_files

Este documento define los requisitos funcionales y no funcionales para la creación de los archivos base del arnés, redactados bajo el estándar EARS.

## R1
El script `init.ps1` DEBE verificar si existe un entorno virtual local de Python buscando `.venv\Scripts\python.exe` y `venv\Scripts\python.exe` en ese orden de prioridad.

## R2
CUANDO el entorno virtual de Python existe localmente, el script `init.ps1` DEBE ejecutar `scripts/validate_harness.py` utilizando dicho intérprete virtual y propagando todos los argumentos recibidos.

## R3
CUANDO el entorno virtual de Python no existe localmente, el script `init.ps1` DEBE ejecutar `scripts/validate_harness.py` utilizando el comando `python` del sistema y propagando todos los argumentos recibidos.

## R4
El script `init.ps1` DEBE propagar el código de salida (`exit code`) retornado por la ejecución de `scripts/validate_harness.py`.

## R5
El script `init.sh` DEBE verificar si existe un entorno virtual local de Python buscando `.venv/bin/python` y `venv/bin/python` en ese orden de prioridad.

## R6
CUANDO el entorno virtual de Python existe localmente, el script `init.sh` DEBE ejecutar `scripts/validate_harness.py` utilizando dicho intérprete virtual y propagando todos los argumentos recibidos.

## R7
CUANDO el entorno virtual de Python no existe localmente, el script `init.sh` DEBE intentar ejecutar `scripts/validate_harness.py` utilizando `python3` o `python` del sistema (en ese orden de prioridad) y propagando todos los argumentos recibidos.

## R8
El script `init.sh` DEBE propagar el código de salida (`exit code`) retornado por la ejecución de `scripts/validate_harness.py`.

## R9
El documento `docs/engineering/conventions/shared.md` DEBE definir convenciones estándar transversales de codificación (UTF-8, LF, nomenclaturas, commits) y explicar cómo extenderlas para tecnologías específicas.

## R10
El documento `docs/engineering/verification/shared.md` DEBE definir guías de verificación de software (tests automáticos, reviews, smoke tests) con ejemplos concretos para Python, Node.js y Monorepos.
