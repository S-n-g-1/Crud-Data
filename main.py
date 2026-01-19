import sys
import gi
import os

# Require GTK 3.0
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio

import database

class InventoryApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Inventory Manager")
        self.set_default_size(900, 600)
        self.set_border_width(0)

        # Initialize Database
        database.init_db()

        # Load CSS
        self.load_css()

        # Main Layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)

        # Header / Title
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header_box.set_name("main-content") # Use ID for padding in CSS
        title_label = Gtk.Label(label="Inventory Management")
        title_label.set_name("title-label")
        title_label.set_halign(Gtk.Align.START)
        header_box.pack_start(title_label, True, True, 0)
        main_box.pack_start(header_box, False, False, 0)

        # Content Area
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        content_box.set_margin_bottom(24)
        main_box.pack_start(content_box, True, True, 0)

        # Form Section
        form_frame = Gtk.Frame()
        form_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        form_box.set_border_width(10)
        form_frame.add(form_box)
        content_box.pack_start(form_frame, False, False, 0)

        # Inputs
        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text("Item Name")
        
        self.category_entry = Gtk.Entry()
        self.category_entry.set_placeholder_text("Category")
        
        self.qty_entry = Gtk.Entry()
        self.qty_entry.set_placeholder_text("Quantity")
        self.qty_entry.set_input_purpose(Gtk.InputPurpose.NUMBER)
        
        self.price_entry = Gtk.Entry()
        self.price_entry.set_placeholder_text("Price")
        self.price_entry.set_input_purpose(Gtk.InputPurpose.NUMBER)

        form_box.pack_start(self.name_entry, True, True, 0)
        form_box.pack_start(self.category_entry, True, True, 0)
        form_box.pack_start(self.qty_entry, False, False, 0)
        form_box.pack_start(self.price_entry, False, False, 0)

        # Buttons
        self.add_btn = Gtk.Button(label="Add Item")
        self.add_btn.set_name("add-btn")
        self.add_btn.connect("clicked", self.on_add_clicked)
        form_box.pack_start(self.add_btn, False, False, 0)

        self.update_btn = Gtk.Button(label="Update")
        self.update_btn.connect("clicked", self.on_update_clicked)
        form_box.pack_start(self.update_btn, False, False, 0)

        self.delete_btn = Gtk.Button(label="Delete")
        self.delete_btn.set_name("delete-btn")
        self.delete_btn.connect("clicked", self.on_delete_clicked)
        form_box.pack_start(self.delete_btn, False, False, 0)

        # TreeView (Table)
        self.list_store = Gtk.ListStore(int, str, str, int, float) # ID, Name, Category, Qty, Price
        self.tree_view = Gtk.TreeView(model=self.list_store)
        
        # Columns
        columns = [
            ("ID", 0),
            ("Name", 1),
            ("Category", 2),
            ("Quantity", 3),
            ("Price", 4)
        ]

        for title, col_id in columns:
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=col_id)
            column.set_sort_column_id(col_id)
            self.tree_view.append_column(column)

        # Selection
        self.selection = self.tree_view.get_selection()
        self.selection.connect("changed", self.on_selection_changed)

        # Scrollable container for TreeView
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_min_content_height(300)
        scrolled_window.add(self.tree_view)
        
        content_box.pack_start(scrolled_window, True, True, 0)

        # Load initial data
        self.refresh_data()

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_path = os.path.join(os.path.dirname(__file__), "style.css")
        try:
            css_provider.load_from_path(css_path)
            screen = Gdk.Screen.get_default()
            style_context = Gtk.StyleContext()
            style_context.add_provider_for_screen(
                screen, 
                css_provider, 
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        except Exception as e:
            print(f"Error loading CSS: {e}")

    def refresh_data(self):
        self.list_store.clear()
        items = database.get_items()
        for item in items:
            self.list_store.append(list(item))

    def on_add_clicked(self, widget):
        name = self.name_entry.get_text()
        category = self.category_entry.get_text()
        qty_text = self.qty_entry.get_text()
        price_text = self.price_entry.get_text()

        if not name:
            self.show_error("Name is required")
            return

        try:
            qty = int(qty_text) if qty_text else 0
            price = float(price_text) if price_text else 0.0
            database.add_item(name, category, qty, price)
            self.clear_form()
            self.refresh_data()
        except ValueError:
            self.show_error("Invalid Quantity or Price")

    def on_update_clicked(self, widget):
        model, treeiter = self.selection.get_selected()
        if not treeiter:
            self.show_error("No item selected")
            return

        item_id = model[treeiter][0]
        name = self.name_entry.get_text()
        category = self.category_entry.get_text()
        qty_text = self.qty_entry.get_text()
        price_text = self.price_entry.get_text()

        try:
            qty = int(qty_text) if qty_text else 0
            price = float(price_text) if price_text else 0.0
            database.update_item(item_id, name, category, qty, price)
            self.clear_form()
            self.refresh_data()
        except ValueError:
            self.show_error("Invalid Quantity or Price")

    def on_delete_clicked(self, widget):
        model, treeiter = self.selection.get_selected()
        if not treeiter:
            self.show_error("No item selected")
            return

        item_id = model[treeiter][0]
        database.delete_item(item_id)
        self.clear_form()
        self.refresh_data()

    def on_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter:
            self.name_entry.set_text(model[treeiter][1])
            self.category_entry.set_text(model[treeiter][2])
            self.qty_entry.set_text(str(model[treeiter][3]))
            self.price_entry.set_text(str(model[treeiter][4]))

    def clear_form(self):
        self.name_entry.set_text("")
        self.category_entry.set_text("")
        self.qty_entry.set_text("")
        self.price_entry.set_text("")
        self.selection.unselect_all()

    def show_error(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error",
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

if __name__ == "__main__":
    app = InventoryApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
