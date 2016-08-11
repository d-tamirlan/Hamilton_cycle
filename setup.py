from cx_Freeze import setup, Executable

includes = ['matplotlib', 'PyQt5.QtWidgets', 'networkx']
# includes = []
packages = []
path = []

GUI2Exe_Target_1 = Executable(
    # what to build
    script = "Main.py",
    initScript = None,
    base = 'Win32GUI',
    targetDir = r"dist",
    targetName = "acup_new.exe",
    compress = True,
    copyDependentFiles = True,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    icon = None
    )

setup(
    version = "0.1",
    description = "No Description",
    author = "d-tamirlan",
    name = "Hamilton_cycle",

    options = {"build_exe": {"includes": includes,
                 "packages": packages,
                 "path": path}
              },
    executables = [GUI2Exe_Target_1]
)
