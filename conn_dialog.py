# -*- coding: utf-8 -*-
"""连接对话框与连接管理对话框。"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QTableWidgetItem, QMessageBox
)

from conn import Ui_Dialog as Ui_ConnDialog
from conn_manage import Ui_Dialog as Ui_ManageDialog


class ConnDialog(QDialog):
    """新建/编辑连接的对话框,可选择已保存的连接快速回填。"""

    def __init__(self, store, parent=None, conn=None):
        super().__init__(parent)
        self.store = store
        self.ui = Ui_ConnDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("连接Redis")
        self.ui.password.setEchoMode(QLineEdit.Password)

        # 填充已保存的连接列表,选择后回填表单
        self.ui.saved.addItem("请选择已保存的连接", None)
        for item in store.connections:
            label = f"{item['name']} ({item['host']}:{item['port']})"
            self.ui.saved.addItem(label, item)
        self.ui.saved.currentIndexChanged.connect(self.on_saved_selected)

        if conn:
            self.fill(conn)
        elif not store.connections:
            self.ui.host.setText("localhost")
            self.ui.port.setText("6379")

    def on_saved_selected(self, _index):
        item = self.ui.saved.currentData()
        if item:
            self.fill(item)

    def fill(self, conn):
        self.ui.name.setText(conn.get("name", ""))
        self.ui.host.setText(conn.get("host", ""))
        self.ui.port.setText(str(conn.get("port", 6379)))
        self.ui.username.setText(conn.get("username", ""))
        self.ui.password.setText(conn.get("password", ""))

    def get_data(self):
        return {
            "name": self.ui.name.text().strip(),
            "host": self.ui.host.text().strip(),
            "port": self.ui.port.text().strip(),
            "username": self.ui.username.text().strip(),
            "password": self.ui.password.text().strip(),
            "remember": self.ui.remember.isChecked(),
        }


class ConnManageDialog(QDialog):
    """连接管理对话框:列表展示已保存的连接,支持连接/新建/编辑/删除。"""

    connect_requested = pyqtSignal(dict)

    def __init__(self, store, parent=None):
        super().__init__(parent)
        self.store = store
        self.ui = Ui_ManageDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("连接管理")

        self.ui.table.horizontalHeader().setStretchLastSection(True)

        self.ui.btn_connect.clicked.connect(self.on_connect)
        self.ui.btn_new.clicked.connect(self.on_new)
        self.ui.btn_edit.clicked.connect(self.on_edit)
        self.ui.btn_delete.clicked.connect(self.on_delete)
        self.ui.btn_close.clicked.connect(self.reject)
        self.ui.table.itemDoubleClicked.connect(lambda _item: self.on_connect())

        self.refresh()

    def refresh(self):
        self.ui.table.setRowCount(0)
        for conn in self.store.connections:
            row = self.ui.table.rowCount()
            self.ui.table.insertRow(row)
            self.ui.table.setItem(row, 0, QTableWidgetItem(conn["name"]))
            self.ui.table.setItem(row, 1, QTableWidgetItem(conn["host"]))
            self.ui.table.setItem(row, 2, QTableWidgetItem(str(conn["port"])))
            self.ui.table.setItem(row, 3, QTableWidgetItem(conn["username"]))
            self.ui.table.item(row, 0).setData(0x0100, conn)
        if self.store.connections:
            self.ui.table.selectRow(0)

    def _selected_conn(self):
        row = self.ui.table.currentRow()
        if row < 0 or row >= self.ui.table.rowCount():
            QMessageBox.warning(self, "提示", "请先选择一个连接")
            return None
        return self.ui.table.item(row, 0).data(0x0100)

    def on_connect(self):
        conn = self._selected_conn()
        if conn:
            self.connect_requested.emit(dict(conn))
            self.accept()

    def on_new(self):
        self._edit_conn(None)

    def on_edit(self):
        conn = self._selected_conn()
        if conn:
            self._edit_conn(dict(conn))

    def _edit_conn(self, conn):
        dialog = ConnDialog(self.store, self, conn)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            host = data["host"]
            port = data["port"]
            if not host:
                QMessageBox.warning(self, "提示", "主机地址不能为空")
                return
            try:
                port = int(port) if port else 6379
            except ValueError:
                QMessageBox.warning(self, "提示", "端口号必须是数字")
                return
            self.store.upsert({
                "name": data["name"] or f"{host}:{port}",
                "host": host,
                "port": port,
                "username": data["username"],
                "password": data["password"],
            })
            # 修改了 host:port 时删除旧记录
            if conn and (conn["host"] != host or int(conn["port"]) != port):
                self.store.delete(conn["host"], conn["port"])
            self.refresh()

    def on_delete(self):
        conn = self._selected_conn()
        if not conn:
            return
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除连接 '{conn['name']} ({conn['host']}:{conn['port']})' 吗?",
            QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.store.delete(conn["host"], conn["port"])
            self.refresh()
