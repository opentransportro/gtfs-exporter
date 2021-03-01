poetry install
pyinstaller --clean --strip --additional-hooks-dir installer_hooks/ --distpath artifacts/Linux-x86_64 exporter.spec