from tkinter import ttk

PRIMARY_BG = '#f2f6fc'
PRIMARY_ACCENT = '#1e3a8a'
SECONDARY_ACCENT = '#10b981'
DANGER_COLOR = '#ef4444'
TEXT_COLOR = '#1f2937'
BUTTON_HOVER = '#2563eb'
FONT_FAMILY = 'Segoe UI'

def configure_styles(root):
    style = ttk.Style(root)
    style.theme_use('clam')
    
    # Frame style
    style.configure('TFrame', background=PRIMARY_BG)
    
    # Label styles
    style.configure('TLabel', background=PRIMARY_BG, foreground=TEXT_COLOR, font=(FONT_FAMILY, 12))
    style.configure('Large.TLabel', font=(FONT_FAMILY, 16, 'bold'))
    style.configure('Title.TLabel', font=(FONT_FAMILY, 24, 'bold'), foreground=PRIMARY_ACCENT)
    
    # Button styles
    style.configure('TButton', 
                   font=(FONT_FAMILY, 12), 
                   foreground='white', 
                   background=PRIMARY_ACCENT,
                   padding=10)
    style.map('TButton',
              background=[('active', BUTTON_HOVER), ('pressed', PRIMARY_ACCENT)],
              relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
    
    style.configure('TEntry', font=(FONT_FAMILY, 12), padding=5)

    style.configure('Treeview', 
                   font=(FONT_FAMILY, 11), 
                   rowheight=25,
                   background='white',
                   fieldbackground='white')
    style.configure('Treeview.Heading', 
                   font=(FONT_FAMILY, 12, 'bold'),
                   background=PRIMARY_ACCENT,
                   foreground='white')
    style.map('Treeview.Heading',
              background=[('active', BUTTON_HOVER)])
    
    style.configure('TRadiobutton', 
                   font=(FONT_FAMILY, 12), 
                   background=PRIMARY_BG,
                   foreground=TEXT_COLOR)
    
    style.configure('Heading.TLabel', font=(FONT_FAMILY, 14, 'bold'), foreground=PRIMARY_ACCENT)
    style.configure('Accent.TButton', background=SECONDARY_ACCENT)
    style.map('Accent.TButton',
              background=[('active', '#0d9b6e'), ('!active', SECONDARY_ACCENT)])
    
    style.map('Invalid.TEntry',
              fieldbackground=[('invalid', '#ffdddd'), ('!invalid', 'white')],
              foreground=[('invalid', 'red'), ('!invalid', 'black')])
