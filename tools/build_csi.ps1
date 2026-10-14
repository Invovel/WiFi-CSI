$ErrorActionPreference = 'Stop'
$env:IDF_PATH = 'D:\ESP32\toolchains\esp-idf-v6.0'
$env:IDF_TOOLS_PATH = 'D:\.espressif\v6.1\tools'
$env:IDF_PYTHON_ENV_PATH = 'D:\ESP32\toolchains\idf-v6.0-venv'
$env:IDF_COMPONENT_MANAGER = '0'
$env:PATH = 'D:\ESP32\toolchains\idf-v6.0-venv\Scripts;D:\.espressif\v6.1\tools\cmake\4.0.3\bin;D:\.espressif\v6.1\tools\ninja\1.12.1;D:\.espressif\v6.1\tools\xtensa-esp-elf\esp-15.2.0_20251204\xtensa-esp-elf\bin;' + $env:PATH
Set-Location -LiteralPath 'D:\PythonProject\CSI\firmware'
& 'D:\ESP32\toolchains\idf-v6.0-venv\Scripts\python.exe' 'D:\ESP32\toolchains\esp-idf-v6.0\tools\idf.py' -B build build
exit $LASTEXITCODE
