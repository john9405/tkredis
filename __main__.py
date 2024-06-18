import redis
import tkinter as tk
from tkinter import ttk, messagebox

class RedisManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Redis Manager")
        
        # Redis Connection Frame
        self.conn_frame = tk.Frame(master)
        self.conn_frame.grid(row=0, column=0, padx=10, pady=10)
        
        self.host_label = tk.Label(self.conn_frame, text="Host:")
        self.host_label.grid(row=0, column=0)
        self.host_entry = tk.Entry(self.conn_frame)
        self.host_entry.grid(row=0, column=1)
        
        self.port_label = tk.Label(self.conn_frame, text="Port:")
        self.port_label.grid(row=1, column=0)
        self.port_entry = tk.Entry(self.conn_frame)
        self.port_entry.grid(row=1, column=1)
        
        self.connect_button = tk.Button(self.conn_frame, text="Connect", command=self.connect_to_redis)
        self.connect_button.grid(row=2, column=0, columnspan=2)
        
        # Key-Value Frame
        self.kv_frame = tk.Frame(master)
        self.kv_frame.grid(row=1, column=0, padx=10, pady=10)
        
        self.key_label = tk.Label(self.kv_frame, text="Key:")
        self.key_label.grid(row=0, column=0)
        self.key_entry = tk.Entry(self.kv_frame)
        self.key_entry.grid(row=0, column=1)
        
        self.value_label = tk.Label(self.kv_frame, text="Value:")
        self.value_label.grid(row=1, column=0)
        self.value_entry = tk.Entry(self.kv_frame)
        self.value_entry.grid(row=1, column=1)
        
        self.get_button = tk.Button(self.kv_frame, text="Get", command=self.get_value)
        self.get_button.grid(row=2, column=0)
        
        self.set_button = tk.Button(self.kv_frame, text="Set", command=self.set_value)
        self.set_button.grid(row=2, column=1)
        
        self.delete_button = tk.Button(self.kv_frame, text="Delete", command=self.delete_key)
        self.delete_button.grid(row=3, column=0, columnspan=2)
        
        self.search_button = tk.Button(self.kv_frame, text="Search", command=self.search_key)
        self.search_button.grid(row=4, column=0, columnspan=2)
        
        self.result_label = tk.Label(self.kv_frame, text="")
        self.result_label.grid(row=5, column=0, columnspan=2)
        
        # Treeview Frame
        self.tree_frame = tk.Frame(master)
        self.tree_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
        
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.grid(row=0, column=0)
        
        self.tree.heading('#0', text='Redis Databases and Keys', anchor='w')
        
        self.redis_client = None

    def connect_to_redis(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        
        try:
            self.redis_client = redis.Redis(host=host, port=port)
            self.redis_client.ping()
            messagebox.showinfo("Connection", "Connected to Redis server successfully!")
            self.load_databases()
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def load_databases(self):
        self.tree.delete(*self.tree.get_children())
        for db_index in range(16):  # Redis has 16 databases by default
            self.redis_client.execute_command('SELECT', db_index)
            keys = self.redis_client.keys('*')
            db_node = self.tree.insert('', 'end', text=f'DB {db_index}', open=True)
            for key in keys:
                self.tree.insert(db_node, 'end', text=key.decode('utf-8'))

    def get_value(self):
        key = self.key_entry.get()
        try:
            value = self.redis_client.get(key)
            if value:
                self.result_label.config(text=f"Value: {value.decode('utf-8')}")
            else:
                self.result_label.config(text="Key not found")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def set_value(self):
        key = self.key_entry.get()
        value = self.value_entry.get()
        try:
            self.redis_client.set(key, value)
            self.result_label.config(text="Key set successfully")
            self.load_databases()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_key(self):
        key = self.key_entry.get()
        try:
            self.redis_client.delete(key)
            self.result_label.config(text="Key deleted successfully")
            self.load_databases()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def search_key(self):
        search_key = self.key_entry.get()
        for db_index in range(16):
            self.redis_client.execute_command('SELECT', db_index)
            keys = self.redis_client.keys('*')
            for key in keys:
                if search_key in key.decode('utf-8'):
                    self.result_label.config(text=f"Found in DB {db_index}: {key.decode('utf-8')}")
                    return
        self.result_label.config(text="Key not found")

if __name__ == "__main__":
    root = tk.Tk()
    app = RedisManager(root)
    root.mainloop()
