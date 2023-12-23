import tkinter as tk
import pyperclip
from tkinter import ttk
from tkinter import messagebox
#from rich import print


def get_customer_data():
    # ... (unchanged)
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
    # ... (unchanged)
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
    # ... (unchanged)
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

    # Clear the text area
    format_text.delete(1.0, tk.END)

    # Insert the combined result into the format box
    format_text.insert(tk.END, result_message)

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

root = tk.Tk()
root.title("CTM")

# Create entry widgets and text area
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

# BooleanVar to determine whether to use tab-separated values
use_tab_values = tk.BooleanVar(value=True)

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
customer_data_entry.bind("<KeyRelease>", update_working_memory)


# Button to Toggle Dark Mode
#dark_mode_button = tk.Button(root, text="Toggle Dark Mode", command=toggle_dark_mode)
#dark_mode_button.pack()


# Checkbox to choose between tab-separated values and direct entry
#tab_checkbox = ttk.Checkbutton(root, text="Use Tab-Separated Values", variable=use_tab_values)
#tab_checkbox.pack()

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

variable_label = tk.Label(root, text="Select a variable:")
variable_label.pack()

# Use your defined variable as the values for the dropdown
variable_dropdown = ttk.Combobox(root, textvariable=selected_variable, values=affected_suite)
variable_dropdown.pack()

failure_type_label = tk.Label(root, text="Select failure type:")
failure_type_label.pack()

# Dropdown for selecting failure type
failure_type_dropdown = ttk.Combobox(root, textvariable=failure_type_variable, values=["Full", "Partial"])
failure_type_dropdown.pack()

# Entry for Customer Data
customer_data_label = tk.Label(root, text="Copy/Paste SQL Data (Customer ID, Node/Pod, Domain separated by tabs):")
customer_data_label.pack()

customer_data_entry = tk.Entry(root)
customer_data_entry.pack()

# Labels and Entry Widgets for Data Input
customer_id_label = tk.Label(root, text="Customer ID:")
customer_id_label.pack()

customer_id_entry = tk.Entry(root)
customer_id_entry.pack()

node_pod_label = tk.Label(root, text="Node/Pod:")
node_pod_label.pack()

node_pod_entry = tk.Entry(root)
node_pod_entry.pack()

domain_label = tk.Label(root, text="Domain:")
domain_label.pack()

domain_entry = tk.Entry(root)
domain_entry.pack()

# Entry for Summary
summary_label = tk.Label(root, text="Summary:")
summary_label.pack()

summary_entry = tk.Entry(root)
summary_entry.pack()

# Entry for affected_user
affected_user_label = tk.Label(root, text="Copy/Paste SQL Data (name, email, serviceId, lastBackupDate, sizeInGb):")
affected_user_label.pack()

affected_user_entry = tk.Entry(root)
affected_user_entry.pack()

# Labels and Entry Widgets for Additional Data Input
name_label = tk.Label(root, text="Name:")
name_label.pack()

name_entry = tk.Entry(root)
name_entry.pack()

email_label = tk.Label(root, text="Email:")
email_label.pack()

email_entry = tk.Entry(root)
email_entry.pack()

serviceId_label = tk.Label(root, text="Service ID:")
serviceId_label.pack()

serviceId_entry = tk.Entry(root)
serviceId_entry.pack()

lastBackupDate_label = tk.Label(root, text="Last Backup Date:")
lastBackupDate_label.pack()

lastBackupDate_entry = tk.Entry(root)
lastBackupDate_entry.pack()

sizeInGb_label = tk.Label(root, text="Size in GB:")
sizeInGb_label.pack()

sizeInGb_entry = tk.Entry(root)
sizeInGb_entry.pack()

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

# Format Text Area
format_text = tk.Text(root, height=12, width=40)
format_text.pack()

root.mainloop()
