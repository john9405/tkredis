# This Python file uses the following encoding: utf-8
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))

from PyQt5.QtWidgets import (
    QApplication, QWidget, QDialog, QMessageBox, QTreeWidgetItem,
    QMenu, QTableWidgetItem, QWidget as QtWidget, QPushButton, QHBoxLayout, QStatusBar
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt

from ui_form import Ui_Widget
from conn import Ui_Dialog as Ui_ConnDialog
from dialog import Ui_Dialog as Ui_AddKeyDialog
from list import Ui_Form
import redis


class ConnDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ConnDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("连接Redis")
        self.ui.host.setText("localhost")
        self.ui.port.setText("6379")


class AddKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AddKeyDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("添加键")

    def get_data(self):
        return {
            'key': self.ui.lineEdit.text().strip(),
            'type': self.ui.comboBox.currentText(),
            'value': self.ui.textEdit.toPlainText(),
            'ttl': self.ui.spinBox.value()
        }


class RedisConnection:
    def __init__(self, name, host, port, username=None, password=None):
        self.name = name
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.clients = {}

    def get_client(self, db=0):
        if db not in self.clients:
            self.clients[db] = redis.Redis(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                db=db,
                decode_responses=True
            )
        return self.clients[db]

    def close(self):
        for client in self.clients.values():
            try:
                client.close()
            except:
                pass
        self.clients.clear()


class LoadDbsThread(QThread):
    loaded = pyqtSignal(object, object)
    error = pyqtSignal(object, str)

    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self):
        db_keys = {}
        try:
            client = self.conn.get_client(0)
            info = client.info('keyspace')
            for db_str, db_info in info.items():
                db_num = int(db_str.replace('db', ''))
                db_keys[db_num] = db_info.get('keys', 0)
            self.loaded.emit(self.conn, db_keys)
        except Exception as e:
            self.error.emit(self.conn, str(e))


class LoadKeysThread(QThread):
    loaded = pyqtSignal(object, int, list)
    error = pyqtSignal(object, int, str)

    def __init__(self, conn, db):
        super().__init__()
        self.conn = conn
        self.db = db

    def run(self):
        try:
            client = self.conn.get_client(self.db)
            keys = client.keys("*")
            self.loaded.emit(self.conn, self.db, keys)
        except Exception as e:
            self.error.emit(self.conn, self.db, str(e))


class KeyListWidget(QtWidget):
    def __init__(self, conn, db, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.conn = conn
        self.db = db
        self.keys = []
        self.filtered_keys = []
        self.page_size = 10
        self.current_page = 1
        self.total_pages = 1
        self.load_thread = None

        self.ui.add.clicked.connect(self.on_add)
        self.ui.refreshBtn.clicked.connect(self.load_keys)
        self.ui.searchBtn.clicked.connect(self.on_search)
        self.ui.clearBtn.clicked.connect(self.on_clear)
        self.ui.home.clicked.connect(self.go_home)
        self.ui.previous.clicked.connect(self.go_previous)
        self.ui.next.clicked.connect(self.go_next)
        self.ui.end.clicked.connect(self.go_end)
        self.ui.spinBox.valueChanged.connect(self.on_page_changed)

        self.update_page_info()
        self.load_keys()

    def _get_main_window(self):
        widget = self.parent()
        while widget:
            if isinstance(widget, Widget):
                return widget
            widget = widget.parent()
        return None

    def set_status(self, message):
        main_window = self._get_main_window()
        if main_window:
            main_window.set_status(message)

    def load_keys(self):
        self.set_status("加载中...")
        if self.load_thread and self.load_thread.isRunning():
            self.load_thread.quit()
            self.load_thread.wait()

        self.load_thread = LoadKeysThread(self.conn, self.db)
        self.load_thread.loaded.connect(self.on_keys_loaded)
        self.load_thread.error.connect(self.on_keys_error)
        self.load_thread.start()

    def on_keys_loaded(self, conn, db, keys):
        self.keys = keys
        self.filtered_keys = keys
        self.total_pages = max(1, (len(self.filtered_keys) + self.page_size - 1) // self.page_size)
        self.current_page = 1
        self.update_page_info()
        self.update_table()
        self.set_status(f"加载完成，共 {len(self.keys)} 个键")

    def on_keys_error(self, conn, db, error_msg):
        self.set_status(f"加载失败: {error_msg}")
        QMessageBox.warning(self, "错误", f"加载键列表失败: {error_msg}")

    def update_table(self):
        self.ui.tableWidget.setRowCount(0)

        if not self.filtered_keys:
            self.update_page_info()
            return

        start = (self.current_page - 1) * self.page_size
        end = min(start + self.page_size, len(self.filtered_keys))
        page_keys = self.filtered_keys[start:end]

        client = self.conn.get_client(self.db)

        for key in page_keys:
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)

            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(key))

            try:
                key_type = client.type(key)
                self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(key_type))

                if key_type == 'string':
                    value = client.get(key) or ''
                elif key_type == 'list':
                    value = ', '.join(client.lrange(key, 0, -1))
                elif key_type == 'set':
                    value = ', '.join(client.smembers(key))
                elif key_type == 'zset':
                    value = ', '.join([f"{m}:{s}" for m, s in client.zrange(key, 0, -1, withscores=True)])
                elif key_type == 'hash':
                    value = ', '.join([f"{k}:{v}" for k, v in client.hgetall(key).items()])
                else:
                    value = ''

                self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(value[:100] if len(value) > 100 else value))
                self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(len(value))))

                ttl = client.ttl(key)
                ttl_text = str(ttl) if ttl > 0 else "永不过期" if ttl == -1 else "已过期"
                self.ui.tableWidget.setItem(row, 4, QTableWidgetItem(ttl_text))

                # 操作按钮
                btn_widget = QtWidget()
                btn_layout = QHBoxLayout(btn_widget)
                btn_layout.setContentsMargins(2, 2, 2, 2)

                edit_btn = QPushButton("编辑")
                edit_btn.setProperty("key", key)
                edit_btn.clicked.connect(self.on_edit)

                delete_btn = QPushButton("删除")
                delete_btn.setProperty("key", key)
                delete_btn.clicked.connect(self.on_delete)

                btn_layout.addWidget(edit_btn)
                btn_layout.addWidget(delete_btn)

                self.ui.tableWidget.setCellWidget(row, 5, btn_widget)

            except Exception as e:
                self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(f"错误: {e}"))

    def update_page_info(self):
        self.ui.spinBox.setMaximum(self.total_pages)
        self.ui.spinBox.setValue(self.current_page)
        self.ui.total.setText(f"{self.current_page}/{self.total_pages}")

    def on_page_changed(self, page):
        if page != self.current_page and 1 <= page <= self.total_pages:
            self.current_page = page
            self.update_page_info()
            self.update_table()

    def go_home(self):
        self.current_page = 1
        self.update_page_info()
        self.update_table()

    def go_previous(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_page_info()
            self.update_table()

    def go_next(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_page_info()
            self.update_table()

    def go_end(self):
        self.current_page = self.total_pages
        self.update_page_info()
        self.update_table()

    def on_search(self):
        keyword = self.ui.searchEdit.text().strip()
        if keyword:
            self.filtered_keys = [k for k in self.keys if keyword.lower() in k.lower()]
        else:
            self.filtered_keys = self.keys

        self.total_pages = max(1, (len(self.filtered_keys) + self.page_size - 1) // self.page_size)
        self.current_page = 1
        self.update_page_info()
        self.update_table()
        if keyword:
            self.set_status(f"搜索完成，找到 {len(self.filtered_keys)} 个键")
        else:
            self.set_status(f"显示全部，共 {len(self.filtered_keys)} 个键")

    def on_clear(self):
        self.ui.searchEdit.clear()
        self.filtered_keys = self.keys
        self.total_pages = max(1, (len(self.filtered_keys) + self.page_size - 1) // self.page_size)
        self.current_page = 1
        self.update_page_info()
        self.update_table()
        self.set_status(f"清除搜索，共 {len(self.filtered_keys)} 个键")

    def on_add(self):
        dialog = AddKeyDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not data['key']:
                QMessageBox.warning(self, "错误", "键名不能为空")
                return

            try:
                client = self.conn.get_client(self.db)

                if data['type'] == 'string':
                    client.set(data['key'], data['value'])
                elif data['type'] == 'list':
                    for item in data['value'].split('\n'):
                        if item.strip():
                            client.rpush(data['key'], item.strip())
                elif data['type'] == 'set':
                    for item in data['value'].split('\n'):
                        if item.strip():
                            client.sadd(data['key'], item.strip())
                elif data['type'] == 'zset':
                    for line in data['value'].split('\n'):
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            try:
                                score = float(parts[-1])
                                member = ' '.join(parts[:-1])
                                client.zadd(data['key'], {member: score})
                            except ValueError:
                                continue
                elif data['type'] == 'hash':
                    for line in data['value'].split('\n'):
                        parts = line.strip().split(':', 1)
                        if len(parts) == 2:
                            client.hset(data['key'], parts[0], parts[1])

                if data['ttl'] > 0:
                    client.expire(data['key'], data['ttl'])

                self.set_status(f"添加成功: {data['key']}")
                self.load_keys()
            except Exception as e:
                self.set_status(f"添加失败: {e}")
                QMessageBox.critical(self, "错误", f"添加失败: {e}")

    def on_edit(self):
        btn = self.sender()
        key = btn.property("key")
        if not key:
            return

        # 找到按钮所在的行
        for row in range(self.ui.tableWidget.rowCount()):
            widget = self.ui.tableWidget.cellWidget(row, 5)
            if widget and widget.findChild(QPushButton, btn.objectName()) == btn:
                break

        try:
            client = self.conn.get_client(self.db)
            key_type = client.type(key)

            if key_type == 'string':
                value = client.get(key) or ''
            elif key_type == 'list':
                value = '\n'.join(client.lrange(key, 0, -1))
            elif key_type == 'set':
                value = '\n'.join(client.smembers(key))
            elif key_type == 'zset':
                value = '\n'.join([f"{m} {s}" for m, s in client.zrange(key, 0, -1, withscores=True)])
            elif key_type == 'hash':
                value = '\n'.join([f"{k}:{v}" for k, v in client.hgetall(key).items()])
            else:
                value = ''

            # 从表格获取有效期
            ttl_item = self.ui.tableWidget.item(row, 4)
            ttl_text = ttl_item.text() if ttl_item else "永不过期"
            ttl = int(ttl_text) if ttl_text.isdigit() else -1

            dialog = AddKeyDialog(self)
            dialog.setWindowTitle("编辑键")
            dialog.ui.lineEdit.setText(key)
            dialog.ui.lineEdit.setReadOnly(True)
            dialog.ui.comboBox.setCurrentText(key_type)
            dialog.ui.textEdit.setPlainText(value)
            dialog.ui.spinBox.setValue(ttl)

            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()

                if data['type'] == 'string':
                    client.set(key, data['value'])
                elif data['type'] == 'list':
                    client.delete(key)
                    for item in data['value'].split('\n'):
                        if item.strip():
                            client.rpush(key, item.strip())
                elif data['type'] == 'set':
                    client.delete(key)
                    for item in data['value'].split('\n'):
                        if item.strip():
                            client.sadd(key, item.strip())
                elif data['type'] == 'zset':
                    client.delete(key)
                    for line in data['value'].split('\n'):
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            try:
                                score = float(parts[-1])
                                member = ' '.join(parts[:-1])
                                client.zadd(key, {member: score})
                            except ValueError:
                                continue
                elif data['type'] == 'hash':
                    client.delete(key)
                    for line in data['value'].split('\n'):
                        parts = line.strip().split(':', 1)
                        if len(parts) == 2:
                            client.hset(key, parts[0], parts[1])

                if data['ttl'] > 0:
                    client.expire(key, data['ttl'])
                elif data['ttl'] == -1:
                    client.persist(key)

                self.set_status(f"修改成功: {key}")
                self.load_keys()

        except Exception as e:
            self.set_status(f"修改失败: {e}")
            QMessageBox.critical(self, "错误", f"编辑失败: {e}")

    def on_delete(self):
        key = self.sender().property("key")
        if not key:
            return

        reply = QMessageBox.question(self, "确认删除", f"确定要删除键 '{key}' 吗?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        try:
            client = self.conn.get_client(self.db)
            client.delete(key)
            self.set_status(f"删除成功: {key}")
            self.load_keys()
        except Exception as e:
            self.set_status(f"删除失败: {e}")
            QMessageBox.critical(self, "错误", f"删除失败: {e}")


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setWindowTitle("TkRedis")

        self.connections = {}

        # Status bar
        self.statusBar = QStatusBar()
        self.statusBar.setFixedHeight(12)
        self.ui.verticalLayout.addWidget(self.statusBar)

        self.load_threads = []

        # 设置 splitter 初始比例为 1:3
        total_width = self.width()
        self.ui.splitter.setSizes([total_width // 4, total_width * 3 // 4])

        self.ui.treeWidget.setHeaderLabel("服务器")
        self.ui.conn.clicked.connect(self.on_connect)
        self.ui.treeWidget.itemExpanded.connect(self.on_item_expanded)
        self.ui.treeWidget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.ui.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.on_context_menu)

        self.clear_tabs()
        self.ui.tabWidget.tabCloseRequested.connect(self.on_tab_close)

    def clear_tabs(self):
        while self.ui.tabWidget.count() > 0:
            self.ui.tabWidget.removeTab(0)

    def set_status(self, message):
        self.statusBar.showMessage(message)

    def on_tab_close(self, index):
        self.ui.tabWidget.removeTab(index)

    def on_connect(self):
        dialog = ConnDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            host = dialog.ui.host.text().strip()
            port_str = dialog.ui.port.text().strip()
            username = dialog.ui.username.text().strip()
            password = dialog.ui.password.text().strip()

            if not host:
                QMessageBox.warning(self, "错误", "主机地址不能为空")
                return

            try:
                port = int(port_str) if port_str else 6379
            except ValueError:
                QMessageBox.warning(self, "错误", "端口号必须是数字")
                return

            conn_name = f"{host}:{port}"
            self.set_status("连接中...")

            try:
                conn = RedisConnection(conn_name, host, port,
                                       username if username else None,
                                       password if password else None)
                conn.get_client(0).ping()

                self.connections[conn_name] = conn

                exists = False
                for i in range(self.ui.treeWidget.topLevelItemCount()):
                    if self.ui.treeWidget.topLevelItem(i).data(0, 0x0101) == conn_name:
                        exists = True
                        break

                if not exists:
                    server_item = QTreeWidgetItem(self.ui.treeWidget)
                    server_item.setText(0, conn_name)
                    server_item.setData(0, 0x0100, 'server')
                    server_item.setData(0, 0x0101, conn_name)
                    server_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

                self.set_status(f"已连接到 {conn_name}")

            except redis.AuthenticationError:
                self.set_status("连接失败: 认证失败")
                QMessageBox.critical(self, "错误", "认证失败，请检查用户名和密码")
            except redis.ConnectionError as e:
                self.set_status("连接失败")
                QMessageBox.critical(self, "错误", f"无法连接到Redis服务器: {e}")
            except Exception as e:
                self.set_status("连接失败")
                QMessageBox.critical(self, "错误", f"连接失败: {e}")

    def on_item_expanded(self, item):
        item_type = item.data(0, 0x0100)
        conn_name = item.data(0, 0x0101)

        if item_type == 'server' and conn_name in self.connections:
            self.set_status("加载数据库...")
            self.load_databases(item, self.connections[conn_name])

    def on_item_double_clicked(self, item, _column):
        item_type = item.data(0, 0x0100)
        conn_name = item.data(0, 0x0101)

        if item_type == 'db' and conn_name in self.connections:
            db = item.data(0, 0x0102)
            self.show_key_list(self.connections[conn_name], db)

    def load_databases(self, server_item, conn):
        server_item.takeChildren()

        thread = LoadDbsThread(conn)
        thread.loaded.connect(self.on_dbs_loaded)
        thread.error.connect(self.on_dbs_error)
        self.load_threads.append(thread)
        thread.start()

    def on_dbs_loaded(self, conn, db_keys):
        for i in range(self.ui.treeWidget.topLevelItemCount()):
            server_item = self.ui.treeWidget.topLevelItem(i)
            if server_item.data(0, 0x0101) == conn.name:
                for db_num in range(16):
                    keys_count = db_keys.get(db_num, 0)
                    db_item = QTreeWidgetItem(server_item)
                    db_item.setText(0, f"DB{db_num} ({keys_count})")
                    db_item.setData(0, 0x0100, 'db')
                    db_item.setData(0, 0x0101, conn.name)
                    db_item.setData(0, 0x0102, db_num)
                break
        self.set_status("数据库加载完成")

    def on_dbs_error(self, conn, error_msg):
        self.set_status(f"加载数据库失败: {error_msg}")

    def show_key_list(self, conn, db):
        tab_name = f"{conn.name}/DB{db}"
        for i in range(self.ui.tabWidget.count()):
            if self.ui.tabWidget.tabText(i) == tab_name:
                self.ui.tabWidget.setCurrentIndex(i)
                return

        key_list = KeyListWidget(conn, db)
        self.ui.tabWidget.addTab(key_list, tab_name)
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

    def on_context_menu(self, pos):
        item = self.ui.treeWidget.itemAt(pos)
        if not item:
            return

        item_type = item.data(0, 0x0100)
        menu = QMenu(self)

        if item_type == 'server':
            disconnect_action = menu.addAction("断开连接")
            disconnect_action.triggered.connect(lambda: self.on_disconnect(item))
            menu.exec_(self.ui.treeWidget.mapToGlobal(pos))
        elif item_type == 'db':
            refresh_action = menu.addAction("刷新")
            refresh_action.triggered.connect(lambda: self.on_refresh_db(item))
            menu.exec_(self.ui.treeWidget.mapToGlobal(pos))

    def on_refresh_db(self, db_item):
        conn_name = db_item.data(0, 0x0101)
        db = db_item.data(0, 0x0102)

        if conn_name not in self.connections:
            return

        conn = self.connections[conn_name]
        self.set_status("刷新中...")

        try:
            client = conn.get_client(db)
            keys_count = len(client.keys("*"))
            db_item.setText(0, f"DB{db} ({keys_count})")
            self.set_status(f"刷新完成，DB{db} 共 {keys_count} 个键")
        except Exception as e:
            self.set_status(f"刷新失败: {e}")

    def on_disconnect(self, server_item):
        conn_name = server_item.data(0, 0x0101)

        if conn_name in self.connections:
            self.connections[conn_name].close()
            del self.connections[conn_name]

        index = self.ui.treeWidget.indexOfTopLevelItem(server_item)
        if index >= 0:
            self.ui.treeWidget.takeTopLevelItem(index)

        self.set_status(f"已断开: {conn_name}")

    def closeEvent(self, event):
        for thread in self.load_threads:
            if thread.isRunning():
                thread.quit()
                thread.wait()

        for conn in self.connections.values():
            conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
