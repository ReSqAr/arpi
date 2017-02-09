lupdate:
	pylupdate5 -verbose arpi/apps/*/*.py -ts arpi/res/i18n/arpi_de_DE.ts
	lupdate -locations none arpi/res/lib/OnScreenTextEdit/OnScreenTextEdit.qml -ts arpi/res/i18n/arpi_qml_de_DE.ts
	
linguist:
	linguist arpi/res/i18n/arpi_de_DE.ts arpi/res/i18n/arpi_qml_de_DE.ts

lrelease:
	lrelease arpi/res/i18n/arpi_de_DE.ts arpi/res/i18n/arpi_qml_de_DE.ts -qm arpi/res/i18n/arpi_de_DE.qm
