# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# 修复__file__未定义问题：改用sys.argv[0]获取spec文件路径
if '__file__' in locals():
    current_dir = os.path.dirname(os.path.abspath(__file__))
else:
    # PyInstaller执行spec时的兼容方案
    current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

a = Analysis(
    ['docker_jar_diff/cli.py'],
    # 添加工作目录，解决本地模块查找问题
    pathex=[current_dir],
    binaries=[],
    # 静态资源映射：(源路径, 目标路径)
    datas=[
        ('.config/config.json', '.config'), 
        ('docker_jar_diff/templates/report_template.html', 'docker_jar_diff/templates')
    ],
    # 精简hiddenimports：只保留第三方模块，内置模块无需声明
    hiddenimports=[
        # docker核心及依赖
        'docker',
        'docker.api',
        'docker.client',
        'docker.models',
        'docker.types',
        'docker.utils',
        'docker.auth',
        'docker.tls',
        'docker.errors',
        'docker.constants',
        # 其他第三方模块
        'click',
        'requests',
        'urllib3'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)
pyz = PYZ(a.pure)

# 关键修改1：启用include_binaries=True，把所有二进制/数据文件嵌入EXE
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # 把二进制文件加入EXE
    a.datas,     # 把静态资源文件加入EXE
    exclude_binaries=False,  # 改为False，不排除二进制文件
    name='docker-jar-diff',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# 关键修改2：删除COLLECT块（它会生成文件夹，和单文件冲突）
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='docker-jar-diff',
# )
