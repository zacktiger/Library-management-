import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# Color Scheme - Modern Dark Theme
# ==========================================
COLORS = {
    'bg_dark': '#1e1e2e',
    'bg_medium': '#2a2a3e',
    'bg_light': '#363654',
    'accent': '#7c3aed',
    'accent_hover': '#9333ea',
    'text': '#e0e0e0',
    'text_secondary': '#a0a0a0',
    'success': '#10b981',
    'danger': '#ef4444',
    'warning': '#f59e0b',
    'border': '#4a4a6a'
}

# ==========================================
# Library Item Classes (Same logic as C++)
# ==========================================
class LibraryItem(ABC):
    def __init__(self, item_id, title):
        self.id = item_id
        self.title = title
        self.is_borrowed = False
    
    @abstractmethod
    def get_type(self):
        pass
    
    @abstractmethod
    def to_dict(self):
        pass
    
    @abstractmethod
    def get_display_info(self):
        pass

class Book(LibraryItem):
    def __init__(self, item_id, title, author, pages):
        super().__init__(item_id, title)
        self.author = author
        self.pages = pages
    
    def get_type(self):
        return "BOOK"
    
    def to_dict(self):
        return {
            'type': 'BOOK',
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'pages': self.pages,
            'is_borrowed': self.is_borrowed
        }
    
    def get_display_info(self):
        return {
            'ID': self.id,
            'Type': 'Book',
            'Title': self.title,
            'Author': self.author,
            'Pages': self.pages,
            'Status': 'Borrowed' if self.is_borrowed else 'Available'
        }

class Journal(LibraryItem):
    def __init__(self, item_id, title, publisher, volume):
        super().__init__(item_id, title)
        self.publisher = publisher
        self.volume = volume
    
    def get_type(self):
        return "JOURNAL"
    
    def to_dict(self):
        return {
            'type': 'JOURNAL',
            'id': self.id,
            'title': self.title,
            'publisher': self.publisher,
            'volume': self.volume,
            'is_borrowed': self.is_borrowed
        }
    
    def get_display_info(self):
        return {
            'ID': self.id,
            'Type': 'Journal',
            'Title': self.title,
            'Publisher': self.publisher,
            'Volume': self.volume,
            'Status': 'Borrowed' if self.is_borrowed else 'Available'
        }

# ==========================================
# Library Manager (Backend Logic)
# ==========================================
class LibraryManager:
    def __init__(self):
        self.inventory = {}
        self.filename = "library_data.json"
        self.load_from_file()
    
    def add_item(self, item):
        if item.id in self.inventory:
            return False, "ID already exists!"
        self.inventory[item.id] = item
        self.save_to_file()
        return True, "Item added successfully"
    
    def remove_item(self, item_id):
        if item_id in self.inventory:
            del self.inventory[item_id]
            self.save_to_file()
            return True, "Item removed successfully"
        return False, "Item not found"
    
    def search_items(self, keyword):
        results = []
        for item in self.inventory.values():
            if keyword.lower() in item.title.lower():
                results.append(item)
        return results
    
    def toggle_borrow(self, item_id):
        if item_id in self.inventory:
            item = self.inventory[item_id]
            item.is_borrowed = not item.is_borrowed
            self.save_to_file()
            return True, f"Status updated to: {'Borrowed' if item.is_borrowed else 'Available'}"
        return False, "Item not found"
    
    def get_all_items(self):
        return list(self.inventory.values())
    
    def get_item(self, item_id):
        return self.inventory.get(item_id)
    
    def save_to_file(self):
        data = [item.to_dict() for item in self.inventory.values()]
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self):
        if not os.path.exists(self.filename):
            return
        
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            
            for item_data in data:
                if item_data['type'] == 'BOOK':
                    item = Book(
                        item_data['id'],
                        item_data['title'],
                        item_data['author'],
                        item_data['pages']
                    )
                elif item_data['type'] == 'JOURNAL':
                    item = Journal(
                        item_data['id'],
                        item_data['title'],
                        item_data['publisher'],
                        item_data['volume']
                    )
                else:
                    continue
                
                item.is_borrowed = item_data.get('is_borrowed', False)
                self.inventory[item.id] = item
        except Exception as e:
            print(f"Error loading data: {e}")

# ==========================================
# Custom Styled Widgets
# ==========================================
class ModernButton(tk.Button):
    def __init__(self, parent, text, command, bg_color=COLORS['accent'], **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=COLORS['text'],
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10,
            **kwargs
        )
        self.default_bg = bg_color
        self.hover_bg = COLORS['accent_hover'] if bg_color == COLORS['accent'] else bg_color
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_enter(self, e):
        self['bg'] = self.hover_bg
    
    def on_leave(self, e):
        self['bg'] = self.default_bg

class ModernEntry(tk.Entry):
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(
            parent,
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            insertbackground=COLORS['text'],
            **kwargs
        )
        self.placeholder = placeholder
        self.placeholder_active = False
        
        if placeholder:
            self.insert(0, placeholder)
            self.config(fg=COLORS['text_secondary'])
            self.placeholder_active = True
            
            self.bind('<FocusIn>', self.on_focus_in)
            self.bind('<FocusOut>', self.on_focus_out)
    
    def on_focus_in(self, e):
        if self.placeholder_active:
            self.delete(0, tk.END)
            self.config(fg=COLORS['text'])
            self.placeholder_active = False
    
    def on_focus_out(self, e):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=COLORS['text_secondary'])
            self.placeholder_active = True
    
    def get_value(self):
        if self.placeholder_active:
            return ""
        return self.get()

# ==========================================
# Main Application GUI
# ==========================================
class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Library Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLORS['bg_dark'])
        
        self.manager = LibraryManager()
        
        # Configure root grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        self.create_header()
        self.create_sidebar()
        self.create_main_area()
        
        # Show initial view
        self.show_all_items()
    
    def create_header(self):
        header = tk.Frame(self.root, bg=COLORS['bg_medium'], height=80)
        header.grid(row=0, column=0, columnspan=2, sticky='ew')
        header.grid_propagate(False)
        
        title = tk.Label(
            header,
            text="📚 Library Management System",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_medium'],
            fg=COLORS['text']
        )
        title.pack(side=tk.LEFT, padx=30, pady=20)
        
        # Stats
        stats_frame = tk.Frame(header, bg=COLORS['bg_medium'])
        stats_frame.pack(side=tk.RIGHT, padx=30)
        
        total_items = len(self.manager.get_all_items())
        borrowed = sum(1 for item in self.manager.get_all_items() if item.is_borrowed)
        
        self.stats_label = tk.Label(
            stats_frame,
            text=f"Total: {total_items} | Available: {total_items - borrowed} | Borrowed: {borrowed}",
            font=('Segoe UI', 11),
            bg=COLORS['bg_medium'],
            fg=COLORS['text_secondary']
        )
        self.stats_label.pack()
    
    def update_stats(self):
        total_items = len(self.manager.get_all_items())
        borrowed = sum(1 for item in self.manager.get_all_items() if item.is_borrowed)
        self.stats_label.config(
            text=f"Total: {total_items} | Available: {total_items - borrowed} | Borrowed: {borrowed}"
        )
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg=COLORS['bg_medium'], width=250)
        sidebar.grid(row=1, column=0, sticky='ns')
        sidebar.grid_propagate(False)
        
        # Sidebar buttons
        buttons = [
            ("📖 View All Items", self.show_all_items),
            ("➕ Add Book", self.show_add_book),
            ("➕ Add Journal", self.show_add_journal),
            ("🔍 Search Items", self.show_search),
            ("🔄 Borrow/Return", self.show_borrow_return),
            ("🗑️ Remove Item", self.show_remove_item),
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(
                sidebar,
                text=text,
                command=command,
                bg=COLORS['bg_light'],
                fg=COLORS['text'],
                font=('Segoe UI', 11),
                relief=tk.FLAT,
                cursor='hand2',
                anchor='w',
                padx=20,
                pady=15
            )
            btn.pack(fill=tk.X, padx=10, pady=5)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=COLORS['accent']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=COLORS['bg_light']))
    
    def create_main_area(self):
        self.main_area = tk.Frame(self.root, bg=COLORS['bg_dark'])
        self.main_area.grid(row=1, column=1, sticky='nsew', padx=20, pady=20)
        self.main_area.grid_rowconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)
    
    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
    
    def show_all_items(self):
        self.clear_main_area()
        
        title = tk.Label(
            self.main_area,
            text="Library Inventory",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORS['bg_dark'],
            fg=COLORS['text']
        )
        title.pack(pady=(0, 20))
        
        # Create treeview
        tree_frame = tk.Frame(self.main_area, bg=COLORS['bg_dark'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        columns = ('ID', 'Type', 'Title', 'Info', 'Status')
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set,
            height=20
        )
        
        # Configure scrollbar
        scrollbar.config(command=tree.yview)
        
        # Define headings
        tree.heading('ID', text='ID')
        tree.heading('Type', text='Type')
        tree.heading('Title', text='Title')
        tree.heading('Info', text='Author/Publisher')
        tree.heading('Status', text='Status')
        
        # Define columns
        tree.column('ID', width=50, anchor='center')
        tree.column('Type', width=80, anchor='center')
        tree.column('Title', width=250)
        tree.column('Info', width=200)
        tree.column('Status', width=100, anchor='center')
        
        # Style
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            'Treeview',
            background=COLORS['bg_light'],
            foreground=COLORS['text'],
            fieldbackground=COLORS['bg_light'],
            borderwidth=0,
            font=('Segoe UI', 10)
        )
        style.configure('Treeview.Heading', font=('Segoe UI', 11, 'bold'))
        style.map('Treeview', background=[('selected', COLORS['accent'])])
        
        # Populate data
        items = self.manager.get_all_items()
        for item in items:
            info = item.to_dict()
            if info['type'] == 'BOOK':
                detail = info['author']
            else:
                detail = info['publisher']
            
            status = 'Borrowed' if item.is_borrowed else 'Available'
            tag = 'borrowed' if item.is_borrowed else 'available'
            
            tree.insert('', tk.END, values=(
                info['id'],
                info['type'],
                info['title'],
                detail,
                status
            ), tags=(tag,))
        
        tree.tag_configure('borrowed', foreground=COLORS['warning'])
        tree.tag_configure('available', foreground=COLORS['success'])
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def show_add_book(self):
        self.clear_main_area()
        
        title = tk.Label(
            self.main_area,
            text="Add New Book",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORS['bg_dark'],
            fg=COLORS['text']
        )
        title.pack(pady=(0, 30))
        
        form_frame = tk.Frame(self.main_area, bg=COLORS['bg_dark'])
        form_frame.pack(pady=20)
        
        # Form fields
        fields = []
        labels_text = ['ID:', 'Title:', 'Author:', 'Pages:']
        
        for i, label_text in enumerate(labels_text):
            label = tk.Label(
                form_frame,
                text=label_text,
                font=('Segoe UI', 12),
                bg=COLORS['bg_dark'],
                fg=COLORS['text']
            )
            label.grid(row=i, column=0, sticky='e', padx=10, pady=15)
            
            entry = ModernEntry(form_frame, width=40)
            entry.grid(row=i, column=1, padx=10, pady=15, ipady=8)
            fields.append(entry)
        
        id_entry, title_entry, author_entry, pages_entry = fields
        
        def add_book():
            try:
                item_id = int(id_entry.get_value())
                title = title_entry.get_value()
                author = author_entry.get_value()
                pages = int(pages_entry.get_value())
                
                if not all([title, author]):
                    messagebox.showerror("Error", "Please fill all fields")
                    return
                
                book = Book(item_id, title, author, pages)
                success, message = self.manager.add_item(book)
                
                if success:
                    messagebox.showinfo("Success", message)
                    self.update_stats()
                    self.show_all_items()
                else:
                    messagebox.showerror("Error", message)
            except ValueError:
                messagebox.showerror("Error", "ID and Pages must be numbers")
        
        ModernButton(form_frame, "Add Book", add_book).grid(
            row=len(labels_text), column=1, pady=30, sticky='ew', padx=10
        )
    
    def show_add_journal(self):
        self.clear_main_area()
        
        title = tk.Label(
            self.main_area,
            text="Add New Journal",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORS['bg_dark'],
            fg=COLORS['text']
        )
        title.pack(pady=(0, 30))
        
        form_frame = tk.Frame(self.main_area, bg=COLORS['bg_dark'])
        form_frame.pack(pady=20)
        
        # Form fields
        fields = []
        labels_text = ['ID:', 'Title:', 'Publisher:', 'Volume:']
        
        for i, label_text in enumerate(labels_text):
            label = tk.Label(
                form_frame,
                text=label_text,
                font=('Segoe UI', 12),
                bg=COLORS['bg_dark'],
                fg=COLORS['text']
            )
            label.grid(row=i, column=0, sticky='e', padx=10, pady=15)
            
            entry = ModernEntry(form_frame, width=40)
            entry.grid(row=i, column=1, padx=10, pady=15, ipady=8)
            fields.append(entry)
        
        id_entry, title_entry, publisher_entry, volume_entry = fields
        
        def add_journal():
            try:
                item_id = int(id_entry.get_value())
                title = title_entry.get_value()
                publisher = publisher_entry.get_value()
                volume = int(volume_entry.get_value())
                
                if not all([title, publisher]):
                    messagebox.showerror("Error", "Please fill all fields")
                    return
                
                journal = Journal(item_id, title, publisher, volume)
                success, message = self.manager.add_item(journal)
                
                if success:
                    messagebox.showinfo("Success", message)
                    self.update_stats()
                    self.show_all_items()
                else:
                    messagebox.showerror("Error", message)
            except ValueError:
                messagebox.showerror("Error", "ID and Volume must be numbers")
        
        ModernButton(form_frame, "Add Journal", add_journal).grid(
            row=len(labels_text), column=1, pady=30, sticky='ew', padx=10
        )
    
    def show_search(self):
        self.clear_main_area()
        
        title = tk.Label(
            self.main_area,
            text="Search Items",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORS['bg_dark'],
            fg=COLORS['text']
        )
        title.pack(pady=(0, 20))
        
        search_frame = tk.Frame(self.main_area, bg=COLORS['bg_dark'])
        search_frame.pack(pady=20)
        
        search_entry = ModernEntry(search_frame, width=40)
        search_entry.pack(side=tk.LEFT, padx=10, ipady=8)
        
        results_frame = tk.Frame(self.main_area, bg=COLORS['bg_dark'])
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        def perform_search():
            keyword = search_entry.get_value()
            if not keyword:
                messagebox.showwarning("Warning", "Please enter a search term")
                return
            
            # Clear previous results
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            results = self.manager.search_items(keyword)
            
            if not results:
                no_results = tk.Label(
                    results_frame,
                    text=f"No items found matching '{keyword}'",
                    font=('Segoe UI', 12),
                    bg=COLORS['bg_dark'],
                    fg=COLORS['text_secondary']
                )
                no_results.pack(pady=50)
            else:
                for item in results:
                    item_frame = tk.Frame(results_frame, bg=COLORS['bg_light'])
                    item_frame.pack(fill=tk.X, pady=5, padx=20)
                    
                    info = item.get_display_info()
                    text = f"[{info['Type']}] {info['Title']} - "
                    if info['Type'] == 'Book':
                        text += f"by {info['Author']}"
                    else:
                        text += f"Publisher: {info['Publisher']}"
                    text += f" | Status: {info['Status']}"
                    
                    label = tk.Label(
                        item_frame,
                        text=text,
                        font=('Segoe UI', 11),
                        bg=COLORS['bg_light'],
                        fg=COLORS['text'],
                        anchor='w'
                    )
                    label.pack(fill=tk.X, padx=15, pady=10)
        
        ModernButton(search_frame, "Search", perform_search).pack(side=tk.LEFT)
    
    def show_borrow_return(self):
        self.clear_main_area()
        
        title = tk.Label(
            self.main_area,
            text="Borrow / Return Item",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORS['bg_dark'],
            fg=COLORS['text']
        )
        title.pack(pady=(0, 30))
        
        form_frame = tk.Frame(self.main_area, bg=COLORS['bg_dark'])
        form_frame.pack(pady=20)
        
        label = tk.Label(
            form_frame,
            text="Item ID:",
            font=('Segoe UI', 12),
            bg=COLORS['bg_dark'],
            fg=COLORS['text']
        )
        label.grid(row=0, column=0, sticky='e', padx=10, pady=15)
        
        id_entry = ModernEntry(form_frame, width=40)
        id_entry.grid(row=0, column=1, padx=10, pady=15, ipady=8)
        
        def toggle_borrow():
            try:
                item_id = int(id_entry.get_value())
                success, message = self.manager.toggle_borrow(item_id)
                
                if success:
                    messagebox.showinfo("Success", message)
                    self.update_stats()
                    id_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", message)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid ID")
        
        ModernButton(form_frame, "Toggle Status", toggle_borrow).grid(
            row=1, column=1, pady=30, sticky='ew', padx=10
        )
    
    def show_remove_item(self):
        self.clear_main_area()
        
        title = tk.Label(
            self.main_area,
            text="Remove Item",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORS['bg_dark'],
            fg=COLORS['text']
        )
        title.pack(pady=(0, 30))
        
        form_frame = tk.Frame(self.main_area, bg=COLORS['bg_dark'])
        form_frame.pack(pady=20)
        
        label = tk.Label(
            form_frame,
            text="Item ID:",
            font=('Segoe UI', 12),
            bg=COLORS['bg_dark'],
            fg=COLORS['text']
        )
        label.grid(row=0, column=0, sticky='e', padx=10, pady=15)
        
        id_entry = ModernEntry(form_frame, width=40)
        id_entry.grid(row=0, column=1, padx=10, pady=15, ipady=8)
        
        def remove_item():
            try:
                item_id = int(id_entry.get_value())
                
                # Confirmation dialog
                if messagebox.askyesno("Confirm", f"Are you sure you want to remove item ID {item_id}?"):
                    success, message = self.manager.remove_item(item_id)
                    
                    if success:
                        messagebox.showinfo("Success", message)
                        self.update_stats()
                        self.show_all_items()
                    else:
                        messagebox.showerror("Error", message)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid ID")
        
        ModernButton(form_frame, "Remove Item", remove_item, bg_color=COLORS['danger']).grid(
            row=1, column=1, pady=30, sticky='ew', padx=10
        )

# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
