def import_pyside():
    try:
        import PySide6.QtCore as QtCore
        import PySide6.QtGui as QtGui
        import PySide6.QtWidgets as QtWidgets
        print("import PySide6")
        return "PySide6", QtCore, QtGui, QtWidgets
    except ImportError:
        try:
            import PySide2.QtCore as QtCore
            import PySide2.QtGui as QtGui
            import PySide2.QtWidgets as QtWidgets
            print("import PySide2")
            return "PySide2", QtCore, QtGui, QtWidgets
        except ImportError:
            try:
                import PySide.QtCore as QtCore
                import PySide.QtGui as QtGui
                import PySide.QtWidgets as QtWidgets
                print("import PySide")
                return "PySide", QtCore, QtGui, QtWidgets
            except ImportError:
                raise ImportError(
                    "Failed to import PySide, PySide2, or PySide6"
                )


def import_shiboken():
    try:
        from shiboken6 import wrapInstance
        print("import shiboken6")
        return "shiboken6", wrapInstance
    except ImportError:
        try:
            from shiboken2 import wrapInstance
            print("import shiboken2")
            return "shiboken2", wrapInstance
        except ImportError:
            try:
                from shiboken import wrapInstance
                print("import shiboken")
                return "shiboken", wrapInstance
            except ImportError:
                raise ImportError(
                    "Failed to import shiboken、shiboken2、or shiboken6"
                    )
