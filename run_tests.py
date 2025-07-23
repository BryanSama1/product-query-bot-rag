#!/usr/bin/env python3
"""
Script para ejecutar tests desde cualquier directorio
"""
import os
import sys
import subprocess

def main():
    # Cambiar al directorio raíz del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Ejecutar pytest
    result = subprocess.run([sys.executable, "-m", "pytest", "-v"] + sys.argv[1:])
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
