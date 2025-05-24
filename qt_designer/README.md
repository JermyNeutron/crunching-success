### Things to edit when converting .ui to .py

Conversion Bash
Update ui_mainwindow.py when the ui has been changed:
```
# pyuic5 -d test_app_ui.ui -o ui_mainwindow.py
```

The conversion may experience issues parsing. These are the common fixes I used:
```
spacerItem = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
```
```
self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
```
```
self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
```