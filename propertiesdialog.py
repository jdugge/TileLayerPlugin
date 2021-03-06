# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TileLayer Plugin
                                 A QGIS plugin
 Plugin layer for Tile Maps
                             -------------------
        begin                : 2012-12-16
        copyright            : (C) 2013 by Minoru Akagi
        email                : akaginch@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QDialog, QDialogButtonBox, QPainter

from ui_propertiesdialog import Ui_Dialog

class PropertiesDialog(QDialog):

  applyClicked = pyqtSignal()

  def __init__(self, layer):
    QDialog.__init__(self)
    # set up the user interface
    self.ui = Ui_Dialog()
    self.ui.setupUi(self)
    self.setWindowTitle(u"%s - %s" % (self.tr("Layer Properties"), layer.name()))

    self.layer = layer
    self.initBlendingCombo()
    self.ui.horizontalSlider_Transparency.valueChanged.connect(self.sliderChanged)
    self.ui.spinBox_Transparency.valueChanged.connect(self.spinBoxChanged)
    self.ui.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.applyClicked)

    self.ui.textEdit_Properties.setText(layer.metadata())
    self.ui.spinBox_Transparency.setValue(layer.transparency)
    i = self.ui.comboBox_BlendingMode.findText(layer.blendModeName)
    if i != -1:
      self.ui.comboBox_BlendingMode.setCurrentIndex(i)

    if layer.layerDef.serviceUrl[0] == ":":
      self.ui.checkBox_SmoothRender.setEnabled(False)
      self.ui.checkBox_CreditVisibility.setEnabled(False)
    else:
      self.ui.checkBox_SmoothRender.setChecked(layer.smoothRender)
      self.ui.checkBox_CreditVisibility.setChecked(layer.creditVisibility)

  def initBlendingCombo(self):
    attrs = dir(QPainter)
    for attr in attrs:
      if attr.startswith("CompositionMode_"):
        self.ui.comboBox_BlendingMode.addItem(attr[16:])

  def sliderChanged(self, val):
    s = self.ui.spinBox_Transparency
    s.blockSignals(True)
    s.setValue(val)
    s.blockSignals(False)

  def spinBoxChanged(self, val):
    s = self.ui.horizontalSlider_Transparency
    s.blockSignals(True)
    s.setValue(val)
    s.blockSignals(False)
