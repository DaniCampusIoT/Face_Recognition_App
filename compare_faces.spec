# -*- mode: python ; coding: utf-8 -*-
import os

# Ruta a los modelos en tu proyecto
models_dir = os.path.join(os.getcwd(), 'face_recognition_models', 'models')

# Lista de archivos .dat necesarios
face_models = [
    (os.path.join(models_dir, 'shape_predictor_5_face_landmarks.dat'), 'face_recognition_models/models'),
    (os.path.join(models_dir, 'shape_predictor_68_face_landmarks.dat'), 'face_recognition_models/models'),
    (os.path.join(models_dir, 'dlib_face_recognition_resnet_model_v1.dat'), 'face_recognition_models/models'),
    (os.path.join(models_dir, 'mmod_human_face_detector.dat'), 'face_recognition_models/models')
]

a = Analysis(
    ['compare_faces.py'],
    pathex=[],
    binaries=[],
    datas=face_models,  # Incluye los modelos aquí
    hiddenimports=['face_recognition_models'],  # Importante para el reconocimiento
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='compare_faces',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
