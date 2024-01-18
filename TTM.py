import tkinter as tk
import pyperclip
from tkinter import ttk
from tkinter import messagebox
from rich import print
from rich.layout import Layout
from rich.live import Live
from rich.console import Console
#from rich.terminal_theme import MONOKAI


def get_customer_data():
   
   if use_tab_values.get():
        customer_data = customer_data_entry.get().strip().split('\t')
        return customer_data[:3] if len(customer_data) == 3 else ('', '', '')
   else:
        return (
            customer_id_entry.get().strip(),
            node_pod_entry.get().strip(),
            domain_entry.get().strip()
        )
def get_affected_user_data():
     
     if use_tab_values.get():
        user_data = affected_user_entry.get().strip().split('\t')
        return user_data[:5] if len(user_data) == 5 else ('', '', '', '', '')
     else:
        return (
            name_entry.get().strip(),
            email_entry.get().strip(),
            serviceId_entry.get().strip(),
            lastBackupDate_entry.get().strip(),
            sizeInGb_entry.get().strip()
        )

def insert_and_format():

    selected_var = selected_variable.get()
    failure_type = failure_type_variable.get()

    # Format failure message based on the selected failure type
    if failure_type == "Full":
        failure_message = "full failure"
    elif failure_type == "Partial":
        failure_message = "partial failure"
    else:
        failure_message = "unknown failure"

    # Create variable message
    variable_message = f"{selected_var} is failing backups {failure_message}"

    # Get and process customer data
    customer_id, node_pod, domain = get_customer_data()

    # Get and process affected user data
    Name, email, serviceId, lastBackupDate, sizeInGb = get_affected_user_data()

    # Get summary data
    summary_data = summary_entry.get().strip()

    # Create a RichText console
    console = Console()

    # Combine all messages
    result_message = (f"Issue:\n{variable_message}\n\n"
                      f"Customer ID: {customer_id}\nNode/Pod: {node_pod}\nDomain: {domain}\n\n"
                      f"Summary: \n{summary_data}\n\n"
                      f"troubleshooting: \n\n"
                      f"Name: {Name}\nEmail: {email}\nService ID: {serviceId}\n"
                      f"Last Backup Date: {lastBackupDate}\nSize in GB: {sizeInGb}\n\n"
                      f"Log: \n\n"
                      f"Similar Ticket: \n\n"
                      f"Conclusion: \n"
                      f"Action: \n")
    
    # Clear the Text widget
    format_text.delete(1.0, tk.END)

    # Insert the combined result into the format box
    format_text.insert(tk.END, result_message + "\n")

def undo_text():
    try:
        format_text.edit_undo()
    except tk.TclError:
        pass  # Ignore if no more undo operations are available
 

def clear_entries():
    # Clear the content of entry widgets
    customer_data_entry.delete(0, tk.END)
    customer_id_entry.delete(0, tk.END)
    node_pod_entry.delete(0, tk.END)
    domain_entry.delete(0, tk.END)
    summary_entry.delete(0, tk.END)
    affected_user_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    serviceId_entry.delete(0, tk.END)
    lastBackupDate_entry.delete(0, tk.END)
    sizeInGb_entry.delete(0, tk.END)
    selected_var.delete(0, tk.END)
    failure_type_dropdown.delete(0, tk.END)

    # Clear the content of entry widgets
    for entry in entry_widgets:
        entry.delete(0, tk.END)

    

    # Clear the content of the text area
    format_text.delete(1.0, tk.END)

def toggle_dark_mode():
    # ... (unchanged)
    current_theme = root.option_get('theme', 'light')  # Get the current theme

    if current_theme == 'light':
        # Dark mode is currently off, so enable dark mode
        root.configure(bg='#333333')
        #dark_mode_button.configure(bg='#555555', fg='#ffffff', activebackground='#777777')
        format_text.configure(bg='#333333', fg='#ffffff')

        # Configure tab_checkbox using ttk.Style
        style = ttk.Style()
        style.configure("Dark.TCheckbutton", background='#333333', foreground='#ffffff', indicatorbackground='#333333')
        #tab_checkbox.configure(style="Dark.TCheckbutton")

        # Configure other entry widgets
        for entry in (customer_data_entry, customer_id_entry, node_pod_entry, domain_entry,
                      summary_entry, affected_user_entry, name_entry, email_entry,
                      serviceId_entry, lastBackupDate_entry, sizeInGb_entry):
            entry.configure(bg='#333333', fg='#ffffff', insertbackground='#ffffff')
    else:
        # Dark mode is currently on, so disable dark mode
        root.configure(bg='')
        #dark_mode_button.configure(bg='', fg='', activebackground='')
        format_text.configure(bg='', fg='')

        # Configure tab_checkbox using ttk.Style
        style = ttk.Style()
        style.configure("Light.TCheckbutton", background='', foreground='', indicatorbackground='')
        #tab_checkbox.configure(style="Light.TCheckbutton")

        # Configure other entry widgets
        for entry in (customer_data_entry, customer_id_entry, node_pod_entry, domain_entry,
                      summary_entry, affected_user_entry, name_entry, email_entry,
                      serviceId_entry, lastBackupDate_entry, sizeInGb_entry):
            entry.configure(bg='', fg='', insertbackground='')

def toggle_dark_mode_command():
    toggle_dark_mode()

def copy_to_clipboard():
    result_text = format_text.get(1.0, tk.END)
    pyperclip.copy(result_text)
    
    # Create a Toplevel window for the message
    message_window = tk.Toplevel(root)
    message_window.title("Copy to Clipboard")

    # Display the message
    message_label = tk.Label(message_window, text="Output copied to clipboard!")
    message_label.pack(padx=10, pady=10)

    # Schedule the message window to close after 2000 milliseconds (2 seconds)
    message_window.after(2000, message_window.destroy)


def update_working_memory(event):
    # Update working memory with the current value of the entry widget
    widget = event.widget
    working_memory[widget] = widget.get()

def show_about():
    about_text = "CTM App\nVersion 1.1\n\n© October 21 2015 CPazmino, LDuBuisson"
    tk.messagebox.showinfo("About", about_text)
   
# Function to switch to the selected page
def switch_to_page(page_number):
    notebook.select(page_number)
   


root = tk.Tk()
root.title("CTM")


# BooleanVar to determine whether to use tab-separated values
use_tab_values = tk.BooleanVar(value=False)



# Create a Notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)


# Create your pages as separate frames
page1 = ttk.Frame(notebook)
page2 = ttk.Frame(notebook)
page3 = ttk.Frame(notebook)
page4 = ttk.Frame(notebook)


# Add pages to the Notebook
notebook.add(page1, text="Backup Failure")
notebook.add(page2, text="Restore Failure")
notebook.add(page3, text="2FA reset")
notebook.add(page4, text="DBSR error")


# List to store entry widgets for easy access
entry_widgets = []


# Working memory to dynamically store entry widget values
working_memory = {}

# Create a Menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

#file_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode_command)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

# Options Menu
options_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=options_menu)

options_menu.add_command(label="Clear", command=clear_entries)
#options_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode_command)
options_menu.add_command(label="Show About", command=show_about)
options_menu.add_separator()
options_menu.add_checkbutton(label="Use Tab-Separated Values", variable=use_tab_values, command=use_tab_values)

# Bind the event to update working memory dynamically
#customer_data_entry.bind("<KeyRelease>", update_working_memory)

# Entry widgets for Page 1 (Backup Failure)
# Create entry widgets and text area


# Add pages to the Notebook
notebook.add(page1, text="Backup Failure")
notebook.add(page2, text="Restore Failure")
notebook.add(page3, text="2FA reset")
notebook.add(page4, text="DBSR error")
# Add widgets to each page

# Entry widgets for Page 1 (Backup Failure)
# Create entry widgets and text area

# Widgets for Page 1
selected_var = tk.Entry(root)
failure_type_dropdown = tk.Entry(root)
customer_data_entry = tk.Entry(root)
customer_id_entry = tk.Entry(root)
node_pod_entry = tk.Entry(root)
domain_entry = tk.Entry(root)
summary_entry = tk.Entry(root)
affected_user_entry = tk.Entry(root)
name_entry = tk.Entry(root)
email_entry = tk.Entry(root)
serviceId_entry = tk.Entry(root)
lastBackupDate_entry = tk.Entry(root)
sizeInGb_entry = tk.Entry(root)
format_text = tk.Text(root, height=12, width=40)


# Define your variable list here
affected_suite = [
    "Office365Teams",
    "Office365Exchange",
    "Office365SharePoint",
    "Office365OneDrive",
    "GoogleMail",
    "GoogleCalendar",
    "GoogleContacts",
    "GoogleDrive",
    "GoogleTeamDrives",
    "GWS",
    "MS 365"
]

selected_variable = tk.StringVar()
failure_type_variable = tk.StringVar()

variable_label = tk.Label(page1, text="Select a variable:")
variable_label.pack()

# Use your defined variable as the values for the dropdown
variable_dropdown = ttk.Combobox(page1, textvariable=selected_variable, values=affected_suite)
variable_dropdown.pack()

failure_type_label = tk.Label(page1, text="Select failure type:")
failure_type_label.pack()

# Dropdown for selecting failure type
failure_type_dropdown = ttk.Combobox(page1, textvariable=failure_type_variable, values=["Full", "Partial"])
failure_type_dropdown.pack()

# Entry for Customer Data
customer_data_label = tk.Label(page1, text="Copy/Paste SQL Data (Customer ID, Node/Pod, Domain separated by tabs):")
customer_data_label.pack()

customer_data_entry = tk.Entry(page1)
customer_data_entry.pack()

# Labels and Entry Widgets for Data Input
customer_id_label = tk.Label(page1, text="Customer ID:")
customer_id_label.pack()

customer_id_entry = tk.Entry(page1, width= 6)
customer_id_entry.pack()

node_pod_label = tk.Label(page1, text="Node/Pod:")
node_pod_label.pack()

node_pod_entry = tk.Entry(page1)
node_pod_entry.pack()

domain_label = tk.Label(page1, text="Domain:")
domain_label.pack()

domain_entry = tk.Entry(page1)
domain_entry.pack()

# Entry for Summary
summary_label = tk.Label(page1, text="Summary:")
summary_label.pack()

summary_entry = tk.Entry(page1)
summary_entry.pack()

# Entry for affected_user
affected_user_label = tk.Label(page1, text="Copy/Paste SQL Data (name, email, serviceId, lastBackupDate, sizeInGb):")
affected_user_label.pack()

affected_user_entry = tk.Entry(page1)
affected_user_entry.pack()

# Labels and Entry Widgets for Additional Data Input
name_label = tk.Label(page1, text="Name:")
name_label.pack()

name_entry = tk.Entry(page1)
name_entry.pack()

email_label = tk.Label(page1, text="Email:")
email_label.pack()

email_entry = tk.Entry(page1)
email_entry.pack()

serviceId_label = tk.Label(page1, text="Service ID:")
serviceId_label.pack()

serviceId_entry = tk.Entry(page1)
serviceId_entry.pack()

lastBackupDate_label = tk.Label(page1, text="Last Backup Date:")
lastBackupDate_label.pack()

lastBackupDate_entry = tk.Entry(page1)
lastBackupDate_entry.pack()

sizeInGb_label = tk.Label(page1, text="Size in GB:")
sizeInGb_label.pack()

sizeInGb_entry = tk.Entry(page1)
sizeInGb_entry.pack()




# Entry widgets for Page 2 (Restore Failure)
selected_variable_restore = tk.StringVar()
failure_type_variable_restore = tk.StringVar()
variable_dropdown_restore = ttk.Combobox(page2, textvariable=selected_variable_restore, values= "Office365Teams, Office365Exchange, Office365SharePoint, Office365OneDrive, GoogleMail, GoogleCalendar,GoogleContacts,GoogleDrive,GoogleTeamDrives, GWS, MS 365")
variable_dropdown_restore.pack()

failure_type_dropdown_restore = ttk.Combobox(page2, textvariable=failure_type_variable_restore, values=["Restore", "Export"])
failure_type_dropdown_restore.pack()

# Entry for Customer Data
customer_data_label_restore = tk.Label(page2, text="Copy/Paste SQL Data (Customer ID, Node/Pod, Domain separated by tabs):")
customer_data_label_restore.pack()

customer_data_entry_restore = tk.Entry(page2)
customer_data_entry_restore.pack()

# Labels and Entry Widgets for Data Input
customer_id_label_restore = tk.Label(page2, text="Customer ID:")
customer_id_label_restore.pack()

customer_id_entry_restore = tk.Entry(page2, width=6)
customer_id_entry_restore.pack()

node_pod_label_restore = tk.Label(page2, text="Node/Pod:")
node_pod_label_restore.pack()

node_pod_entry_restore = tk.Entry(page2)
node_pod_entry_restore.pack()

domain_label_restore = tk.Label(page2, text="Domain:")
domain_label_restore.pack()

domain_entry_restore = tk.Entry(page2)
domain_entry_restore.pack()

# Entry for Summary
summary_label_restore = tk.Label(page2, text="Summary:")
summary_label_restore.pack()

summary_entry_restore = tk.Entry(page2)
summary_entry_restore.pack()

# Entry for affected_user
affected_user_label_restore = tk.Label(page2, text="Copy/Paste SQL Data (name, email, serviceId, lastBackupDate, sizeInGb):")
affected_user_label_restore.pack()

affected_user_entry_restore = tk.Entry(page2)
affected_user_entry_restore.pack()

# Labels and Entry Widgets for Additional Data Input
name_label_restore = tk.Label(page2, text="Name:")
name_label_restore.pack()

name_entry_restore = tk.Entry(page2)
name_entry_restore.pack()

email_label_restore = tk.Label(page2, text="Email:")
email_label_restore.pack()

email_entry_restore = tk.Entry(page2)
email_entry_restore.pack()

serviceId_label_restore = tk.Label(page2, text="Service ID:")
serviceId_label_restore.pack()

serviceId_entry_restore = tk.Entry(page2)
serviceId_entry_restore.pack()

lastBackupDate_label_restore = tk.Label(page2, text="Last Backup Date:")
lastBackupDate_label_restore.pack()

lastBackupDate_entry_restore = tk.Entry(page2)
lastBackupDate_entry_restore.pack()

sizeInGb_label_restore = tk.Label(page2, text="Size in GB:")
sizeInGb_label_restore.pack()

sizeInGb_entry_restore = tk.Entry(page2)
sizeInGb_entry_restore.pack()

# Entry widgets for Page 3 (2FA reset)
# ... (Define entry widgets for Page 3)

# Entry widgets for Page 4 (DBSR error)
# ... (Define entry widgets for Page 4)



# Button to Insert Variable and Format Data
insert_and_format_button = tk.Button(root, text="Submit", command=insert_and_format)
insert_and_format_button.pack()

# Bind the event to update working memory dynamically
customer_data_entry.bind("<KeyRelease>", update_working_memory)

# Button to Copy to Clipboard
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack()

# Create a clear button
clear_button = tk.Button(root, text="Clear", command=clear_entries)
clear_button.pack()

# Create a button for undo
undo_button = tk.Button(root, text="Undo", command=undo_text)
undo_button.pack()

# Use a Text widget for displaying rich text
format_text = tk.Text(root, height=12, width=40, wrap=tk.WORD)
format_text.pack()

console = Console(width=80)

root.mainloop()
