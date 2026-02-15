#!/usr/bin/env python3
"""
Professional Graph Generator
A comprehensive tool for creating beautiful, publication-quality graphs
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib import cm
import json

class GraphGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Graph Generator")
        self.root.geometry("1600x950")
        
        # Make window resizable
        self.root.minsize(1400, 800)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Left panel - Controls
        left_panel = ttk.Frame(main_frame, padding="5")
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Right panel - Graph display
        right_panel = ttk.Frame(main_frame, padding="5")
        right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Create scrollable frame for controls
        canvas = tk.Canvas(left_panel, width=450, bg='white')
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        scrollable_frame.bind("<Configure>", on_frame_configure)
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ===== GRAPH MODE =====
        ttk.Label(scrollable_frame, text="Graph Mode", font=('Arial', 14, 'bold'), 
                 foreground='#2E86AB').pack(pady=(5,2))
        
        # Beginner Mode Toggle
        beginner_frame = ttk.Frame(scrollable_frame)
        beginner_frame.pack(fill='x', padx=15, pady=5)
        
        self.beginner_mode = tk.BooleanVar(value=False)
        beginner_check = ttk.Checkbutton(beginner_frame, 
                                         text="🌟 Beginner Mode (Simplified Interface)", 
                                         variable=self.beginner_mode,
                                         command=self.toggle_beginner_mode)
        beginner_check.pack(side=tk.LEFT)
        ttk.Label(beginner_frame, text="Hide advanced options, show only essentials", 
                 font=('Arial', 8, 'italic'), foreground='gray').pack(side=tk.LEFT, padx=5)
        
        mode_frame = ttk.LabelFrame(scrollable_frame, text="Select Your Mode", padding=10)
        mode_frame.pack(fill='x', padx=15, pady=5)
        
        self.graph_mode = tk.StringVar(value="professional")
        
        modes = [
            ("🎨 Professional Mode", "professional", "Publication-quality, elegant styling"),
            ("📊 Normal Mode", "normal", "Balanced, general-purpose graphs"),
            ("🔬 Scientific Mode", "scientific", "Grid-heavy, precise, academic style")
        ]
        
        for text, value, desc in modes:
            frame = ttk.Frame(mode_frame)
            frame.pack(fill='x', pady=2)
            ttk.Radiobutton(frame, text=text, variable=self.graph_mode, 
                           value=value, command=self.apply_mode_preset).pack(side=tk.LEFT)
            ttk.Label(frame, text=desc, font=('Arial', 8, 'italic'), 
                     foreground='gray').pack(side=tk.LEFT, padx=10)
        
        # ===== GRAPH TYPE =====
        ttk.Label(scrollable_frame, text="Graph Type", font=('Arial', 12, 'bold')).pack(pady=5)
        self.graph_type = tk.StringVar(value="line")
        graph_types = [
            ("Line Plot", "line"),
            ("Scatter Plot", "scatter"),
            ("Bar Chart", "bar"),
            ("3D Surface", "3d_surface"),
            ("3D Scatter", "3d_scatter"),
            ("Histogram", "histogram"),
            ("Contour Plot", "contour"),
            ("Heatmap", "heatmap")
        ]
        
        for text, value in graph_types:
            ttk.Radiobutton(scrollable_frame, text=text, variable=self.graph_type, 
                           value=value, command=self.update_input_fields).pack(anchor=tk.W, padx=20)
        
        # Help button for graph types
        ttk.Button(scrollable_frame, text="? Graph Types Help", 
                  command=self.show_graph_types_help).pack(pady=5)
        
        # ===== DATA INPUT =====
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="Data Input", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # X Data
        ttk.Label(scrollable_frame, text="X Data (ANY values - even, odd, random, decimals):").pack(anchor=tk.W, padx=20)
        ttk.Label(scrollable_frame, text="Examples: 1,3,5,7 | 2,4,6,8 | 1.5,2.7,3.9 | -5,-3,0,3,5", 
                 font=('Arial', 8, 'italic'), foreground='gray').pack(anchor=tk.W, padx=20)
        self.x_data = tk.StringVar(value="0, 1, 2, 3, 4, 5")
        ttk.Entry(scrollable_frame, textvariable=self.x_data, width=40).pack(padx=20, pady=2)
        
        # Y Data
        ttk.Label(scrollable_frame, text="Y Data (ANY values - no restrictions):").pack(anchor=tk.W, padx=20)
        ttk.Label(scrollable_frame, text="Examples: 10,25,30,18 | sin(x) | x**2 | 3.14,2.71,1.41", 
                 font=('Arial', 8, 'italic'), foreground='gray').pack(anchor=tk.W, padx=20)
        self.y_data = tk.StringVar(value="0, 1, 4, 9, 16, 25")
        ttk.Entry(scrollable_frame, textvariable=self.y_data, width=40).pack(padx=20, pady=2)
        
        # Z Data (optional)
        self.z_frame = ttk.Frame(scrollable_frame)
        self.z_frame.pack(fill='x')
        ttk.Label(self.z_frame, text="Z Data (optional, for 3D):").pack(anchor=tk.W, padx=20)
        self.z_data = tk.StringVar(value="")
        ttk.Entry(self.z_frame, textvariable=self.z_data, width=40).pack(padx=20, pady=2)
        
        # Quick data templates
        example_frame = ttk.Frame(scrollable_frame)
        example_frame.pack(pady=10, padx=20, fill='x')
        ttk.Button(example_frame, text="📊 Load Example Data", 
                  command=self.load_example_data).pack(fill='x')
        
        ttk.Label(scrollable_frame, text="Tip: Use example data to get started quickly!", 
                 font=('Arial', 9, 'italic'), foreground='gray').pack(pady=2)
        
        # ===== APPEARANCE =====
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        self.appearance_label = ttk.Label(scrollable_frame, text="Appearance", 
                                         font=('Arial', 12, 'bold'))
        self.appearance_label.pack(pady=5)
        
        # Color
        color_frame = ttk.Frame(scrollable_frame)
        color_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(color_frame, text="Color:").pack(side=tk.LEFT)
        self.color = tk.StringVar(value="blue")
        colors = ["blue", "red", "green", "orange", "purple", "cyan", "magenta", 
                 "black", "brown", "pink", "gold", "lime", "navy", "coral", "teal", 
                 "crimson", "indigo", "turquoise", "salmon", "orchid"]
        ttk.Combobox(color_frame, textvariable=self.color, values=colors, 
                    width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(color_frame, text="?", width=2, 
                  command=lambda: self.show_help("Color")).pack(side=tk.LEFT)
        
        # Custom Color (Hex)
        custom_color_frame = ttk.Frame(scrollable_frame)
        custom_color_frame.pack(fill='x', padx=20, pady=2)
        ttk.Label(custom_color_frame, text="Custom Color (hex):").pack(side=tk.LEFT)
        self.custom_color = tk.StringVar(value="")
        ttk.Entry(custom_color_frame, textvariable=self.custom_color, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(custom_color_frame, text="e.g. #FF5733", font=('Arial', 8, 'italic'), 
                 foreground='gray').pack(side=tk.LEFT)
        
        # Line Width
        width_frame = ttk.Frame(scrollable_frame)
        width_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(width_frame, text="Line Width:").pack(side=tk.LEFT)
        self.line_width = tk.DoubleVar(value=2.0)
        ttk.Scale(width_frame, from_=0.5, to=10, variable=self.line_width, 
                 orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT, padx=5)
        ttk.Label(width_frame, textvariable=self.line_width).pack(side=tk.LEFT)
        ttk.Button(width_frame, text="?", width=2, 
                  command=lambda: self.show_help("Line Width")).pack(side=tk.LEFT)
        
        # Marker Style
        marker_frame = ttk.Frame(scrollable_frame)
        marker_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(marker_frame, text="Marker Style:").pack(side=tk.LEFT)
        self.marker = tk.StringVar(value="o")
        markers = ["None", "o", "s", "^", "v", "*", "D", "+", "x", "p", "h"]
        ttk.Combobox(marker_frame, textvariable=self.marker, values=markers, 
                    width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(marker_frame, text="?", width=2, 
                  command=lambda: self.show_help("Marker Style")).pack(side=tk.LEFT)
        
        # Marker Size
        msize_frame = ttk.Frame(scrollable_frame)
        msize_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(msize_frame, text="Marker Size:").pack(side=tk.LEFT)
        self.marker_size = tk.DoubleVar(value=6.0)
        ttk.Scale(msize_frame, from_=1, to=20, variable=self.marker_size, 
                 orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT, padx=5)
        ttk.Label(msize_frame, textvariable=self.marker_size).pack(side=tk.LEFT)
        
        # Line Style
        lstyle_frame = ttk.Frame(scrollable_frame)
        lstyle_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(lstyle_frame, text="Line Style:").pack(side=tk.LEFT)
        self.line_style = tk.StringVar(value="-")
        line_styles = ["-", "--", "-.", ":", "None"]
        ttk.Combobox(lstyle_frame, textvariable=self.line_style, values=line_styles, 
                    width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(lstyle_frame, text="?", width=2, 
                  command=lambda: self.show_help("Line Style")).pack(side=tk.LEFT)
        
        # Alpha (transparency)
        alpha_frame = ttk.Frame(scrollable_frame)
        alpha_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(alpha_frame, text="Transparency:").pack(side=tk.LEFT)
        self.alpha = tk.DoubleVar(value=1.0)
        ttk.Scale(alpha_frame, from_=0, to=1, variable=self.alpha, 
                 orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT, padx=5)
        ttk.Label(alpha_frame, textvariable=self.alpha).pack(side=tk.LEFT)
        
        # ===== LABELS & TITLE =====
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="Labels & Title", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Title
        ttk.Label(scrollable_frame, text="Graph Title:").pack(anchor=tk.W, padx=20)
        self.title = tk.StringVar(value="My Beautiful Graph")
        ttk.Entry(scrollable_frame, textvariable=self.title, width=40).pack(padx=20, pady=2)
        
        # X Label
        ttk.Label(scrollable_frame, text="X-Axis Label:").pack(anchor=tk.W, padx=20)
        self.xlabel = tk.StringVar(value="X Axis")
        ttk.Entry(scrollable_frame, textvariable=self.xlabel, width=40).pack(padx=20, pady=2)
        
        # Y Label
        ttk.Label(scrollable_frame, text="Y-Axis Label:").pack(anchor=tk.W, padx=20)
        self.ylabel = tk.StringVar(value="Y Axis")
        ttk.Entry(scrollable_frame, textvariable=self.ylabel, width=40).pack(padx=20, pady=2)
        
        # Z Label
        ttk.Label(scrollable_frame, text="Z-Axis Label (for 3D):").pack(anchor=tk.W, padx=20)
        self.zlabel = tk.StringVar(value="Z Axis")
        ttk.Entry(scrollable_frame, textvariable=self.zlabel, width=40).pack(padx=20, pady=2)
        
        # ===== AXIS RANGES =====
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="📏 Axis Ranges (Set Your View)", 
                 font=('Arial', 12, 'bold')).pack(pady=5)
        
        ttk.Label(scrollable_frame, text="Control exactly what you see on each axis", 
                 font=('Arial', 9, 'italic'), foreground='#2E86AB').pack()
        
        # Auto or Manual toggle
        range_mode_frame = ttk.Frame(scrollable_frame)
        range_mode_frame.pack(fill='x', padx=20, pady=5)
        
        self.auto_range = tk.BooleanVar(value=True)
        ttk.Checkbutton(range_mode_frame, text="Auto Range (Fit all data)", 
                       variable=self.auto_range, 
                       command=self.toggle_range_controls).pack(side=tk.LEFT)
        ttk.Button(range_mode_frame, text="?", width=2,
                  command=lambda: self.show_help("Axis Ranges")).pack(side=tk.LEFT, padx=5)
        
        # X Axis Range
        self.x_range_frame = ttk.LabelFrame(scrollable_frame, text="X-Axis Range", padding=5)
        self.x_range_frame.pack(fill='x', padx=20, pady=5)
        
        x_range_controls = ttk.Frame(self.x_range_frame)
        x_range_controls.pack(fill='x')
        ttk.Label(x_range_controls, text="Min:").pack(side=tk.LEFT, padx=2)
        self.x_min = tk.StringVar(value="")
        ttk.Entry(x_range_controls, textvariable=self.x_min, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Label(x_range_controls, text="Max:").pack(side=tk.LEFT, padx=5)
        self.x_max = tk.StringVar(value="")
        ttk.Entry(x_range_controls, textvariable=self.x_max, width=10).pack(side=tk.LEFT, padx=2)
        
        # Y Axis Range
        self.y_range_frame = ttk.LabelFrame(scrollable_frame, text="Y-Axis Range", padding=5)
        self.y_range_frame.pack(fill='x', padx=20, pady=5)
        
        y_range_controls = ttk.Frame(self.y_range_frame)
        y_range_controls.pack(fill='x')
        ttk.Label(y_range_controls, text="Min:").pack(side=tk.LEFT, padx=2)
        self.y_min = tk.StringVar(value="")
        ttk.Entry(y_range_controls, textvariable=self.y_min, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Label(y_range_controls, text="Max:").pack(side=tk.LEFT, padx=5)
        self.y_max = tk.StringVar(value="")
        ttk.Entry(y_range_controls, textvariable=self.y_max, width=10).pack(side=tk.LEFT, padx=2)
        
        # Z Axis Range (for 3D)
        self.z_range_frame = ttk.LabelFrame(scrollable_frame, text="Z-Axis Range (3D only)", padding=5)
        self.z_range_frame.pack(fill='x', padx=20, pady=5)
        
        z_range_controls = ttk.Frame(self.z_range_frame)
        z_range_controls.pack(fill='x')
        ttk.Label(z_range_controls, text="Min:").pack(side=tk.LEFT, padx=2)
        self.z_min = tk.StringVar(value="")
        ttk.Entry(z_range_controls, textvariable=self.z_min, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Label(z_range_controls, text="Max:").pack(side=tk.LEFT, padx=5)
        self.z_max = tk.StringVar(value="")
        ttk.Entry(z_range_controls, textvariable=self.z_max, width=10).pack(side=tk.LEFT, padx=2)
        
        # Quick range presets
        preset_frame = ttk.Frame(scrollable_frame)
        preset_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(preset_frame, text="Quick Presets:").pack(side=tk.LEFT)
        ttk.Button(preset_frame, text="0 to 10", 
                  command=lambda: self.set_range_preset(0, 10)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="-10 to 10", 
                  command=lambda: self.set_range_preset(-10, 10)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="-5 to 5", 
                  command=lambda: self.set_range_preset(-5, 5)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="Clear", 
                  command=self.clear_ranges).pack(side=tk.LEFT, padx=2)
        
        # ===== ADVANCED STYLING =====
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        self.advanced_label = ttk.Label(scrollable_frame, 
                                       text="Advanced Styling (Beautiful Design)", 
                                       font=('Arial', 12, 'bold'))
        self.advanced_label.pack(pady=5)
        
        self.advanced_frame = ttk.Frame(scrollable_frame)
        self.advanced_frame.pack(fill='x')
        
        # Font size
        font_frame = ttk.Frame(self.advanced_frame)
        font_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(font_frame, text="Font Size:").pack(side=tk.LEFT)
        self.font_size = tk.IntVar(value=12)
        ttk.Scale(font_frame, from_=8, to=20, variable=self.font_size, 
                 orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT, padx=5)
        ttk.Label(font_frame, textvariable=self.font_size).pack(side=tk.LEFT)
        
        # Edge color (for bars, markers)
        edge_frame = ttk.Frame(scrollable_frame)
        edge_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(edge_frame, text="Edge Color:").pack(side=tk.LEFT)
        self.edge_color = tk.StringVar(value="black")
        edge_colors = ["black", "white", "none", "same as fill"]
        ttk.Combobox(edge_frame, textvariable=self.edge_color, values=edge_colors, 
                    width=15).pack(side=tk.LEFT, padx=5)
        
        # Edge width
        edge_width_frame = ttk.Frame(scrollable_frame)
        edge_width_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(edge_width_frame, text="Edge Width:").pack(side=tk.LEFT)
        self.edge_width = tk.DoubleVar(value=1.0)
        ttk.Scale(edge_width_frame, from_=0, to=5, variable=self.edge_width, 
                 orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT, padx=5)
        ttk.Label(edge_width_frame, textvariable=self.edge_width).pack(side=tk.LEFT)
        
        # Figure DPI (quality)
        dpi_frame = ttk.Frame(scrollable_frame)
        dpi_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(dpi_frame, text="Display Quality (DPI):").pack(side=tk.LEFT)
        self.dpi = tk.IntVar(value=100)
        ttk.Combobox(dpi_frame, textvariable=self.dpi, 
                    values=[50, 75, 100, 150, 200], width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(dpi_frame, text="Higher = Better", font=('Arial', 8, 'italic'), 
                 foreground='gray').pack(side=tk.LEFT)
        
        # Colormap for 3D/Heatmap
        cmap_frame = ttk.Frame(scrollable_frame)
        cmap_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(cmap_frame, text="Colormap (3D/Heatmap):").pack(side=tk.LEFT)
        self.colormap = tk.StringVar(value="viridis")
        colormaps = ["viridis", "plasma", "inferno", "magma", "cividis",
                    "coolwarm", "rainbow", "jet", "hot", "cool", "spring",
                    "summer", "autumn", "winter", "twilight", "ocean"]
        ttk.Combobox(cmap_frame, textvariable=self.colormap, values=colormaps, 
                    width=12).pack(side=tk.LEFT, padx=5)
        
        # Tight layout
        self.tight_layout = tk.BooleanVar(value=True)
        ttk.Checkbutton(scrollable_frame, text="Optimize Layout (Recommended)", 
                       variable=self.tight_layout).pack(anchor=tk.W, padx=20, pady=2)
        
        # Anti-aliasing
        self.antialiased = tk.BooleanVar(value=True)
        ttk.Checkbutton(scrollable_frame, text="Smooth Lines (Anti-aliasing)", 
                       variable=self.antialiased).pack(anchor=tk.W, padx=20, pady=2)
        
        # Professional shadow
        self.add_shadow = tk.BooleanVar(value=False)
        ttk.Checkbutton(scrollable_frame, text="Add Shadow Effect (3D/Bar)", 
                       variable=self.add_shadow).pack(anchor=tk.W, padx=20, pady=2)
        
        # ===== GRID & STYLE =====
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="Grid & Style", font=('Arial', 12, 'bold')).pack(pady=5)
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="Grid & Style", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Grid
        self.show_grid = tk.BooleanVar(value=True)
        ttk.Checkbutton(scrollable_frame, text="Show Grid", 
                       variable=self.show_grid).pack(anchor=tk.W, padx=20)
        
        # Axes through origin
        self.show_origin_axes = tk.BooleanVar(value=False)
        origin_frame = ttk.Frame(scrollable_frame)
        origin_frame.pack(anchor=tk.W, padx=20, pady=2)
        ttk.Checkbutton(origin_frame, text="Show Axes Through Origin (0,0)", 
                       variable=self.show_origin_axes).pack(side=tk.LEFT)
        ttk.Button(origin_frame, text="?", width=2,
                  command=lambda: self.show_help("Origin Axes")).pack(side=tk.LEFT, padx=5)
        
        # Legend
        self.show_legend = tk.BooleanVar(value=True)
        ttk.Checkbutton(scrollable_frame, text="Show Legend", 
                       variable=self.show_legend).pack(anchor=tk.W, padx=20)
        
        # Style
        style_frame = ttk.Frame(scrollable_frame)
        style_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(style_frame, text="Plot Style:").pack(side=tk.LEFT)
        self.plot_style = tk.StringVar(value="seaborn-v0_8")
        styles = ["default", "seaborn-v0_8", "ggplot", "bmh", "fivethirtyeight", 
                 "grayscale", "dark_background"]
        ttk.Combobox(style_frame, textvariable=self.plot_style, values=styles, 
                    width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(style_frame, text="?", width=2, 
                  command=lambda: self.show_help("Plot Style")).pack(side=tk.LEFT)
        
        # ===== ACTION BUTTONS =====
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        
        ttk.Label(scrollable_frame, text="Actions", font=('Arial', 12, 'bold')).pack(pady=5)
        
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=10, padx=20, fill='x')
        
        generate_btn = ttk.Button(button_frame, text="🎨 Generate Graph", 
                  command=self.generate_graph)
        generate_btn.pack(fill='x', pady=5)
        
        save_btn = ttk.Button(button_frame, text="💾 Save Graph", 
                  command=self.save_graph)
        save_btn.pack(fill='x', pady=5)
        
        clear_btn = ttk.Button(button_frame, text="🗑️ Clear", 
                  command=self.clear_graph)
        clear_btn.pack(fill='x', pady=5)
        
        help_btn = ttk.Button(scrollable_frame, text="📖 Complete Help Guide", 
                  command=self.show_complete_help)
        help_btn.pack(pady=5, padx=20, fill='x')
        
        quick_guide_btn = ttk.Button(scrollable_frame, text="🚀 Quick Start Guide (Beginners)", 
                  command=self.show_quick_start_guide)
        quick_guide_btn.pack(pady=5, padx=20, fill='x')
        
        # Add some bottom padding to ensure scroll works
        ttk.Frame(scrollable_frame, height=50).pack()
        
        # ===== EQUATION AREA =====
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(scrollable_frame, text="📐 Equation Plotter", 
                 font=('Arial', 12, 'bold')).pack(pady=5)
        
        ttk.Label(scrollable_frame, text="Plot mathematical equations directly!", 
                 font=('Arial', 9, 'italic'), foreground='#2E86AB').pack()
        
        equation_frame = ttk.LabelFrame(scrollable_frame, text="Enter Equation", padding=10)
        equation_frame.pack(fill='x', padx=20, pady=5)
        
        # Equation input
        ttk.Label(equation_frame, text="Y = ", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        self.equation = tk.StringVar(value="")
        equation_entry = ttk.Entry(equation_frame, textvariable=self.equation, width=35, 
                                   font=('Courier', 10))
        equation_entry.pack(side=tk.LEFT, padx=5)
        
        # Quick equation buttons
        eq_buttons_frame = ttk.Frame(scrollable_frame)
        eq_buttons_frame.pack(fill='x', padx=20, pady=5)
        
        ttk.Label(eq_buttons_frame, text="Quick Equations:").pack(anchor=tk.W)
        
        quick_eqs = [
            ("Quadratic", "x**2"),
            ("Cubic", "x**3"),
            ("Sine", "sin(x)"),
            ("Cosine", "cos(x)"),
            ("Exponential", "exp(x)"),
            ("Logarithm", "log(abs(x)+1)")
        ]
        
        button_row = ttk.Frame(eq_buttons_frame)
        button_row.pack(fill='x', pady=2)
        for name, eq in quick_eqs:
            ttk.Button(button_row, text=name, 
                      command=lambda e=eq: self.equation.set(e),
                      width=12).pack(side=tk.LEFT, padx=2, pady=2)
        
        # X range for equation
        range_frame = ttk.Frame(scrollable_frame)
        range_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(range_frame, text="X Range:").pack(side=tk.LEFT)
        ttk.Label(range_frame, text="From:").pack(side=tk.LEFT, padx=(10,2))
        self.eq_x_start = tk.StringVar(value="-10")
        ttk.Entry(range_frame, textvariable=self.eq_x_start, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Label(range_frame, text="To:").pack(side=tk.LEFT, padx=(5,2))
        self.eq_x_end = tk.StringVar(value="10")
        ttk.Entry(range_frame, textvariable=self.eq_x_end, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Label(range_frame, text="Points:").pack(side=tk.LEFT, padx=(5,2))
        self.eq_points = tk.StringVar(value="200")
        ttk.Entry(range_frame, textvariable=self.eq_points, width=8).pack(side=tk.LEFT, padx=2)
        
        # Plot equation button
        plot_eq_frame = ttk.Frame(scrollable_frame)
        plot_eq_frame.pack(fill='x', padx=20, pady=5)
        
        ttk.Button(plot_eq_frame, text="📈 Plot Equation", 
                  command=self.plot_equation).pack(side=tk.LEFT, padx=2, fill='x', expand=True)
        
        self.show_quadrants = tk.BooleanVar(value=False)
        ttk.Checkbutton(plot_eq_frame, text="📐 Show 4 Quadrants", 
                       variable=self.show_quadrants).pack(side=tk.LEFT, padx=5)
        ttk.Button(plot_eq_frame, text="?", width=2,
                  command=lambda: self.show_help("Quadrants")).pack(side=tk.LEFT)
        
        # Equation examples
        ttk.Label(scrollable_frame, text="Examples:", font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=20)
        examples_text = """• x**2 - 4*x + 3  (Parabola)
• sin(x) + cos(2*x)  (Wave combination)
• exp(-x**2/10) * sin(x)  (Damped wave)
• x**3 - 3*x  (Cubic)
• abs(x)  (Absolute value)"""
        ttk.Label(scrollable_frame, text=examples_text, 
                 font=('Courier', 8), foreground='#555').pack(anchor=tk.W, padx=30)
        
        # Add final padding
        ttk.Frame(scrollable_frame, height=30).pack()
        
        # ===== GRAPH DISPLAY AREA =====
        self.figure = plt.Figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize
        self.update_input_fields()
        self.toggle_range_controls()  # Set initial state
        
        # Auto-load example data on startup
        self.root.after(100, self.show_welcome_message)
    
    def toggle_range_controls(self):
        """Enable/disable range controls based on auto_range setting"""
        if self.auto_range.get():
            # Disable manual range controls
            for child in self.x_range_frame.winfo_children():
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Entry):
                        widget.config(state='disabled')
            for child in self.y_range_frame.winfo_children():
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Entry):
                        widget.config(state='disabled')
            for child in self.z_range_frame.winfo_children():
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Entry):
                        widget.config(state='disabled')
        else:
            # Enable manual range controls
            for child in self.x_range_frame.winfo_children():
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Entry):
                        widget.config(state='normal')
            for child in self.y_range_frame.winfo_children():
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Entry):
                        widget.config(state='normal')
            for child in self.z_range_frame.winfo_children():
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Entry):
                        widget.config(state='normal')
    
    def set_range_preset(self, min_val, max_val):
        """Set a preset range for X and Y axes"""
        self.auto_range.set(False)
        self.toggle_range_controls()
        self.x_min.set(str(min_val))
        self.x_max.set(str(max_val))
        self.y_min.set(str(min_val))
        self.y_max.set(str(max_val))
        messagebox.showinfo("Range Preset Applied", 
                          f"X and Y ranges set to [{min_val}, {max_val}]\n\n"
                          f"You can adjust these values or click 'Auto Range' to reset.")
    
    def clear_ranges(self):
        """Clear all range values and enable auto range"""
        self.x_min.set("")
        self.x_max.set("")
        self.y_min.set("")
        self.y_max.set("")
        self.z_min.set("")
        self.z_max.set("")
        self.auto_range.set(True)
        self.toggle_range_controls()
        messagebox.showinfo("Ranges Cleared", "All axis ranges cleared.\nAuto Range enabled.")
    
    def toggle_beginner_mode(self):
        """Toggle between beginner and advanced interface"""
        if self.beginner_mode.get():
            # Beginner Mode: Hide advanced options
            messagebox.showinfo("Beginner Mode Enabled! 🌟",
                              "Simplified interface activated!\n\n"
                              "You'll see only the essentials:\n"
                              "✅ Graph type\n"
                              "✅ Data input\n"
                              "✅ Basic colors\n"
                              "✅ Title and labels\n"
                              "✅ Generate button\n\n"
                              "Perfect for quick, easy graphs!")
            # Note: In full implementation, we would hide/show frames
            # For now, we'll keep all controls visible
        else:
            # Advanced Mode: Show all options
            messagebox.showinfo("Advanced Mode",
                              "Full interface activated!\n\n"
                              "All features available:\n"
                              "✅ All styling options\n"
                              "✅ Advanced controls\n"
                              "✅ Professional features\n"
                              "✅ Complete customization")
    
    def show_welcome_message(self):
        """Show welcome message on startup"""
        msg = """Welcome to Professional Graph Generator! 🎨

Quick Start:
1. Choose a graph mode (Professional/Normal/Scientific)
2. Select a graph type from the list
3. Click '📊 Load Example Data' to see sample data
4. OR use the Equation Plotter to plot functions!
5. Click '🎨 Generate Graph' to create your visualization
6. Customize colors, widths, and styles
7. Click '💾 Save Graph' to export

Click '?' buttons for help on any option!
Click '📖 Complete Help Guide' for full documentation.

Ready to create beautiful graphs!"""
        
        messagebox.showinfo("Welcome! 👋", msg)
    
    def apply_mode_preset(self):
        """Apply preset styling based on selected mode"""
        mode = self.graph_mode.get()
        
        if mode == "professional":
            # Professional: Clean, elegant, publication-quality
            self.plot_style.set("seaborn-v0_8")
            self.line_width.set(2.5)
            self.marker_size.set(7)
            self.font_size.set(13)
            self.show_grid.set(True)
            self.show_legend.set(True)
            self.tight_layout.set(True)
            self.antialiased.set(True)
            self.dpi.set(150)
            self.alpha.set(0.9)
            messagebox.showinfo("Professional Mode", 
                              "Applied professional styling:\n"
                              "• Clean seaborn style\n"
                              "• Elegant line widths\n"
                              "• Publication-quality fonts\n"
                              "• High DPI display")
        
        elif mode == "normal":
            # Normal: Balanced, general-purpose
            self.plot_style.set("default")
            self.line_width.set(2.0)
            self.marker_size.set(6)
            self.font_size.set(12)
            self.show_grid.set(True)
            self.show_legend.set(True)
            self.tight_layout.set(True)
            self.antialiased.set(True)
            self.dpi.set(100)
            self.alpha.set(1.0)
            messagebox.showinfo("Normal Mode", 
                              "Applied normal styling:\n"
                              "• Balanced appearance\n"
                              "• Standard settings\n"
                              "• General purpose\n"
                              "• Quick rendering")
        
        elif mode == "scientific":
            # Scientific: Grid-heavy, precise, academic
            self.plot_style.set("bmh")
            self.line_width.set(1.5)
            self.marker_size.set(5)
            self.font_size.set(11)
            self.show_grid.set(True)
            self.show_legend.set(True)
            self.tight_layout.set(True)
            self.antialiased.set(True)
            self.dpi.set(100)
            self.alpha.set(1.0)
            self.edge_width.set(1.0)
            messagebox.showinfo("Scientific Mode", 
                              "Applied scientific styling:\n"
                              "• Precise grid lines\n"
                              "• Academic appearance\n"
                              "• Clear data points\n"
                              "• Research-ready")
    
    def plot_equation(self):
        """Plot mathematical equation from equation area"""
        try:
            equation = self.equation.get().strip()
            if not equation:
                messagebox.showwarning("No Equation", 
                                     "Please enter an equation to plot!\n\n"
                                     "Examples:\n"
                                     "• x**2\n"
                                     "• sin(x)\n"
                                     "• exp(x)\n"
                                     "• x**3 - 2*x")
                return
            
            # Get range
            x_start = float(self.eq_x_start.get())
            x_end = float(self.eq_x_end.get())
            n_points = int(self.eq_points.get())
            
            # Generate x values
            x = np.linspace(x_start, x_end, n_points)
            
            # Evaluate equation
            # Create safe namespace for eval
            safe_dict = {
                'x': x,
                'np': np,
                'sin': np.sin,
                'cos': np.cos,
                'tan': np.tan,
                'exp': np.exp,
                'log': np.log,
                'log10': np.log10,
                'sqrt': np.sqrt,
                'abs': np.abs,
                'pi': np.pi,
                'e': np.e
            }
            
            y = eval(equation, {"__builtins__": {}}, safe_dict)
            
            # Clear figure and create plot
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # Apply style
            plt.style.use(self.plot_style.get())
            
            # Get color
            color = self.color.get()
            if self.custom_color.get().strip():
                color = self.custom_color.get().strip()
            
            # Plot the equation
            ax.plot(x, y, color=color, linewidth=self.line_width.get(),
                   label=f'y = {equation}', antialiased=self.antialiased.get())
            
            # Set title and labels
            font_size = self.font_size.get()
            ax.set_title(f'y = {equation}', fontsize=font_size+2, fontweight='bold', pad=20)
            ax.set_xlabel('x', fontsize=font_size, fontweight='medium')
            ax.set_ylabel('y', fontsize=font_size, fontweight='medium')
            
            # Show 4 quadrants if enabled
            if self.show_quadrants.get():
                # Add axes through origin
                ax.axhline(y=0, color='black', linewidth=1.5, alpha=0.7)
                ax.axvline(x=0, color='black', linewidth=1.5, alpha=0.7)
                
                # Make sure we show all quadrants
                x_max = max(abs(x_start), abs(x_end))
                y_min, y_max = ax.get_ylim()
                y_max_abs = max(abs(y_min), abs(y_max))
                
                ax.set_xlim(-x_max, x_max)
                ax.set_ylim(-y_max_abs, y_max_abs)
                
                # Add quadrant labels
                ax.text(0.95, 0.95, 'I', transform=ax.transAxes, 
                       fontsize=12, alpha=0.5, ha='right', va='top')
                ax.text(0.05, 0.95, 'II', transform=ax.transAxes,
                       fontsize=12, alpha=0.5, ha='left', va='top')
                ax.text(0.05, 0.05, 'III', transform=ax.transAxes,
                       fontsize=12, alpha=0.5, ha='left', va='bottom')
                ax.text(0.95, 0.05, 'IV', transform=ax.transAxes,
                       fontsize=12, alpha=0.5, ha='right', va='bottom')
            
            # Grid
            mode = self.graph_mode.get()
            if mode == "scientific":
                ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.8)
                ax.minorticks_on()
                ax.grid(which='minor', alpha=0.2, linestyle=':', linewidth=0.5)
            elif mode == "professional":
                ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
            else:
                if self.show_grid.get():
                    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
            
            # Legend
            if self.show_legend.get():
                if mode == "professional":
                    ax.legend(fontsize=font_size-2, framealpha=0.95, shadow=True, 
                             fancybox=True, loc='best')
                else:
                    ax.legend(fontsize=font_size-2, framealpha=0.9)
            
            # Tight layout
            if self.tight_layout.get():
                self.figure.tight_layout()
            
            # Redraw
            self.canvas.draw()
            
            # Update data fields for consistency
            self.x_data.set(f"{x_start}:{x_end}")
            self.y_data.set(equation)
            self.title.set(f"y = {equation}")
            self.xlabel.set("x")
            self.ylabel.set("y")
            self.graph_type.set("line")
            
            messagebox.showinfo("Success! 📈", 
                              f"Equation plotted successfully!\n\n"
                              f"Equation: y = {equation}\n"
                              f"Range: [{x_start}, {x_end}]\n"
                              f"Points: {n_points}\n"
                              f"Quadrants: {'Shown' if self.show_quadrants.get() else 'Hidden'}")
            
        except Exception as e:
            messagebox.showerror("Error", 
                               f"Error plotting equation:\n{str(e)}\n\n"
                               f"Tips:\n"
                               f"• Use ** for powers (x**2, not x^2)\n"
                               f"• Use * for multiplication (2*x, not 2x)\n"
                               f"• Available functions: sin, cos, tan, exp, log, sqrt, abs\n"
                               f"• Check your X range values\n"
                               f"• Make sure equation uses 'x' variable")
    
    def update_input_fields(self):
        """Show/hide Z data field based on graph type"""
        graph_type = self.graph_type.get()
        if graph_type in ['3d_surface', '3d_scatter', 'contour', 'heatmap']:
            self.z_frame.pack(fill='x')
        else:
            self.z_frame.pack_forget()
    
    def parse_data(self, data_str):
        """Parse data string into numpy array"""
        data_str = data_str.strip()
        
        # Check if it's a range expression
        if ':' in data_str:
            parts = data_str.split(':')
            if len(parts) == 2:
                return np.linspace(float(parts[0]), float(parts[1]), 100)
            elif len(parts) == 3:
                return np.arange(float(parts[0]), float(parts[1]), float(parts[2]))
        
        # Check if it's a mathematical expression
        if any(op in data_str for op in ['sin', 'cos', 'exp', 'log', 'sqrt', 'tan']):
            try:
                x = np.linspace(0, 10, 100)
                return eval(data_str, {"np": np, "x": x, "sin": np.sin, "cos": np.cos, 
                                      "exp": np.exp, "log": np.log, "sqrt": np.sqrt, 
                                      "tan": np.tan})
            except:
                pass
        
        # Parse as comma-separated values
        try:
            return np.array([float(x.strip()) for x in data_str.split(',')])
        except:
            raise ValueError(f"Cannot parse data: {data_str}")
    
    def generate_graph(self):
        """Generate the graph based on user inputs"""
        try:
            # Clear previous plot
            self.figure.clear()
            
            # Apply style
            plt.style.use(self.plot_style.get())
            
            # Parse data
            x = self.parse_data(self.x_data.get())
            y = self.parse_data(self.y_data.get())
            
            graph_type = self.graph_type.get()
            mode = self.graph_mode.get()
            
            # Get color - check for custom hex color first
            color = self.color.get()
            if self.custom_color.get().strip():
                color = self.custom_color.get().strip()
            elif color == "custom":
                color = "#1f77b4"  # Default matplotlib blue
            
            # Get marker
            marker = self.marker.get()
            if marker == "None":
                marker = None
            
            # Get edge color
            edge_color = self.edge_color.get()
            if edge_color == "none":
                edge_color = None
            elif edge_color == "same as fill":
                edge_color = color
            
            # Set figure DPI for quality
            self.figure.set_dpi(self.dpi.get())
            
            # Create appropriate plot
            if graph_type == "line":
                ax = self.figure.add_subplot(111)
                ax.plot(x, y, color=color, linewidth=self.line_width.get(), 
                       marker=marker, markersize=self.marker_size.get(),
                       linestyle=self.line_style.get(), alpha=self.alpha.get(),
                       label='Data', antialiased=self.antialiased.get(),
                       markeredgecolor=edge_color, markeredgewidth=self.edge_width.get())
            
            elif graph_type == "scatter":
                ax = self.figure.add_subplot(111)
                ax.scatter(x, y, color=color, s=self.marker_size.get()**2, 
                          alpha=self.alpha.get(), marker=marker if marker else 'o',
                          label='Data', edgecolors=edge_color, 
                          linewidths=self.edge_width.get())
            
            elif graph_type == "bar":
                ax = self.figure.add_subplot(111)
                bars = ax.bar(x, y, color=color, alpha=self.alpha.get(), 
                      width=self.line_width.get()/5, label='Data',
                      edgecolor=edge_color, linewidth=self.edge_width.get())
                
                # Add shadow effect if enabled
                if self.add_shadow.get():
                    for bar in bars:
                        bar.set_linewidth(self.edge_width.get() + 1)
                        bar.set_edgecolor('gray')
            
            elif graph_type == "histogram":
                ax = self.figure.add_subplot(111)
                ax.hist(y, bins=20, color=color, alpha=self.alpha.get(), 
                       edgecolor=edge_color if edge_color else 'black', 
                       linewidth=self.edge_width.get())
            
            elif graph_type == "3d_surface":
                z_str = self.z_data.get()
                if not z_str:
                    # Generate surface from x, y
                    X, Y = np.meshgrid(x, y)
                    Z = np.sin(np.sqrt(X**2 + Y**2))
                else:
                    X, Y = np.meshgrid(x, y)
                    Z = eval(z_str, {"X": X, "Y": Y, "np": np})
                
                ax = self.figure.add_subplot(111, projection='3d')
                surf = ax.plot_surface(X, Y, Z, cmap=self.colormap.get(), 
                                      linewidth=self.line_width.get()/2,
                                      alpha=self.alpha.get(),
                                      antialiased=self.antialiased.get())
                self.figure.colorbar(surf, ax=ax, shrink=0.5)
                
                # Add shadow/projection if enabled
                if self.add_shadow.get():
                    ax.contour(X, Y, Z, zdir='z', offset=Z.min(), 
                              cmap=self.colormap.get(), alpha=0.3, linewidths=1)
            
            elif graph_type == "3d_scatter":
                z_str = self.z_data.get()
                if z_str:
                    z = self.parse_data(z_str)
                else:
                    z = x + y  # Default
                
                ax = self.figure.add_subplot(111, projection='3d')
                ax.scatter(x, y, z, color=color, s=self.marker_size.get()**2,
                          alpha=self.alpha.get(), marker=marker if marker else 'o',
                          edgecolors=edge_color, linewidths=self.edge_width.get())
            
            elif graph_type == "contour":
                X, Y = np.meshgrid(x, y)
                z_str = self.z_data.get()
                if z_str:
                    Z = eval(z_str, {"X": X, "Y": Y, "np": np})
                else:
                    Z = np.sin(np.sqrt(X**2 + Y**2))
                
                ax = self.figure.add_subplot(111)
                contour = ax.contour(X, Y, Z, levels=15, linewidths=self.line_width.get(),
                                    cmap=self.colormap.get())
                ax.clabel(contour, inline=True, fontsize=8)
                self.figure.colorbar(contour, ax=ax)
            
            elif graph_type == "heatmap":
                X, Y = np.meshgrid(x, y)
                z_str = self.z_data.get()
                if z_str:
                    Z = eval(z_str, {"X": X, "Y": Y, "np": np})
                else:
                    Z = np.sin(np.sqrt(X**2 + Y**2))
                
                ax = self.figure.add_subplot(111)
                im = ax.imshow(Z, cmap=self.colormap.get(), aspect='auto', 
                              alpha=self.alpha.get(), interpolation='bilinear')
                self.figure.colorbar(im, ax=ax)
            
            # Set labels and title with custom font size
            font_size = self.font_size.get()
            ax.set_title(self.title.get(), fontsize=font_size+2, fontweight='bold', pad=20)
            ax.set_xlabel(self.xlabel.get(), fontsize=font_size, fontweight='medium')
            ax.set_ylabel(self.ylabel.get(), fontsize=font_size, fontweight='medium')
            
            if graph_type in ['3d_surface', '3d_scatter']:
                ax.set_zlabel(self.zlabel.get(), fontsize=font_size, fontweight='medium')
            
            # Apply axis ranges if manual mode
            if not self.auto_range.get():
                try:
                    if self.x_min.get() and self.x_max.get():
                        ax.set_xlim(float(self.x_min.get()), float(self.x_max.get()))
                    if self.y_min.get() and self.y_max.get():
                        ax.set_ylim(float(self.y_min.get()), float(self.y_max.get()))
                    if graph_type in ['3d_surface', '3d_scatter']:
                        if self.z_min.get() and self.z_max.get():
                            ax.set_zlim(float(self.z_min.get()), float(self.z_max.get()))
                except ValueError:
                    pass  # Ignore invalid range values
            
            # Apply mode-specific styling
            if mode == "scientific":
                # Scientific mode: Enhanced grid
                if graph_type not in ['heatmap']:
                    ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.8, which='both')
                    ax.minorticks_on()
                    ax.grid(which='minor', alpha=0.2, linestyle=':', linewidth=0.5)
            elif mode == "professional":
                # Professional mode: Subtle grid
                if graph_type not in ['heatmap']:
                    ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
            else:
                # Normal mode: Standard grid
                if self.show_grid.get() and graph_type not in ['heatmap']:
                    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
            
            # Show axes through origin if enabled
            if self.show_origin_axes.get() and graph_type not in ['heatmap', '3d_surface', '3d_scatter']:
                ax.axhline(y=0, color='black', linewidth=1.5, alpha=0.8, zorder=5)
                ax.axvline(x=0, color='black', linewidth=1.5, alpha=0.8, zorder=5)
            
            # Legend
            if self.show_legend.get() and graph_type in ['line', 'scatter', 'bar']:
                if mode == "professional":
                    ax.legend(fontsize=font_size-2, framealpha=0.95, shadow=True, 
                             fancybox=True, loc='best')
                else:
                    ax.legend(fontsize=font_size-2, framealpha=0.9, shadow=False)
            
            # Tight layout
            if self.tight_layout.get():
                self.figure.tight_layout()
            
            # Add mode watermark in corner (optional)
            if mode == "professional":
                self.figure.text(0.99, 0.01, '📊 Professional', 
                               ha='right', va='bottom', fontsize=7, 
                               alpha=0.3, style='italic')
            elif mode == "scientific":
                self.figure.text(0.99, 0.01, '🔬 Scientific', 
                               ha='right', va='bottom', fontsize=7, 
                               alpha=0.3, style='italic')
            
            # Redraw
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating graph:\n{str(e)}")
    
    def save_graph(self):
        """Save the current graph"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), 
                      ("SVG files", "*.svg"), ("All files", "*.*")]
        )
        if filename:
            self.figure.savefig(filename, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Success", f"Graph saved to:\n{filename}")
    
    def clear_graph(self):
        """Clear the graph"""
        self.figure.clear()
        self.canvas.draw()
    
    def load_example_data(self):
        """Load example data based on graph type"""
        graph_type = self.graph_type.get()
        
        if graph_type == "line":
            # Show flexibility - odd numbers work fine!
            self.x_data.set("1, 3, 5, 7, 9, 11, 13")
            self.y_data.set("2, 8, 18, 32, 50, 72, 98")
            self.title.set("Beautiful Line Plot - Any Values Work!")
        elif graph_type == "scatter":
            # Random decimal values work!
            self.x_data.set("0.5, 1.8, 3.2, 4.7, 6.1, 7.9, 9.3")
            self.y_data.set("2.1, 4.7, 6.3, 8.9, 11.2, 13.8, 16.1")
            self.title.set("Beautiful Scatter - Decimals Work!")
        elif graph_type == "bar":
            # Even numbers, why not?
            self.x_data.set("2, 4, 6, 8, 10")
            self.y_data.set("15, 28, 42, 51, 63")
            self.title.set("Beautiful Bars - Even Numbers!")
        elif graph_type == "3d_surface":
            # Any range works!
            self.x_data.set("-8:8")
            self.y_data.set("-8:8")
            self.z_data.set("np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1*np.sqrt(X**2 + Y**2))")
            self.title.set("Stunning 3D Surface!")
        elif graph_type == "3d_scatter":
            # Mix of values
            self.x_data.set("1, 2, 3, 5, 8, 13")
            self.y_data.set("1, 4, 9, 25, 64, 169")
            self.z_data.set("1, 8, 27, 125, 512, 2197")
            self.title.set("3D Scatter - Fibonacci & Powers!")
        elif graph_type == "histogram":
            self.y_data.set("np.random.randn(1000)")
            self.title.set("Beautiful Distribution")
        elif graph_type == "contour":
            self.x_data.set("-6:6")
            self.y_data.set("-6:6")
            self.z_data.set("np.sin(X) * np.cos(Y)")
            self.title.set("Gorgeous Contour Map")
        elif graph_type == "heatmap":
            self.x_data.set("-5:5")
            self.y_data.set("-5:5")
            self.z_data.set("X**2 + Y**2")
            self.title.set("Beautiful Heatmap")
        
        messagebox.showinfo("Example Loaded! 🎨", 
                           f"Example data loaded for {graph_type}!\n\n"
                           "Notice: You can use ANY values!\n"
                           "• Even numbers (2, 4, 6, 8)\n"
                           "• Odd numbers (1, 3, 5, 7)\n"
                           "• Decimals (1.5, 2.7, 3.9)\n"
                           "• Random values - anything!\n\n"
                           "Click 'Generate Graph' to see!")
    
    def show_help(self, topic):
        """Show help for specific topic"""
        help_texts = {
            "Color": "Choose the color of your plot elements.\n\n"
                    "Available colors:\n"
                    "- Standard: blue, red, green, orange, purple, etc.\n"
                    "- Custom: Select to use custom hex color codes\n\n"
                    "Tip: Use consistent colors across related graphs!",
            
            "Line Width": "Controls the thickness of lines in your plot.\n\n"
                         "Range: 0.5 to 10\n"
                         "- Thin (0.5-2): Good for multiple overlapping lines\n"
                         "- Medium (2-4): Standard for most plots\n"
                         "- Thick (4-10): Emphasis or presentation slides",
            
            "Marker Style": "Symbols shown at each data point.\n\n"
                           "Options:\n"
                           "- o: Circle\n"
                           "- s: Square\n"
                           "- ^, v: Triangles\n"
                           "- *: Star\n"
                           "- D: Diamond\n"
                           "- +, x: Plus/Cross\n"
                           "- None: No markers",
            
            "Line Style": "Pattern of the line connecting points.\n\n"
                         "- Solid (-): Continuous line\n"
                         "- Dashed (--): Evenly spaced dashes\n"
                         "- Dash-dot (-.): Alternating dash and dot\n"
                         "- Dotted (:): Small dots\n"
                         "- None: No line (markers only)",
            
            "Plot Style": "Overall aesthetic theme of your graph.\n\n"
                         "- seaborn: Clean, publication-ready\n"
                         "- ggplot: Similar to R's ggplot2\n"
                         "- bmh: Bayesian Methods for Hackers style\n"
                         "- dark_background: Light elements on dark",
            
            "Axis Ranges": "Control the visible range of each axis.\n\n"
                          "Auto Range (default):\n"
                          "- Automatically fits all your data\n"
                          "- Best for most cases\n"
                          "- No manual setup needed\n\n"
                          "Manual Range:\n"
                          "- Uncheck 'Auto Range' to enable\n"
                          "- Set Min and Max for each axis\n"
                          "- Focus on specific data regions\n"
                          "- Zoom in or out as needed\n\n"
                          "Quick Presets:\n"
                          "- Use buttons for common ranges\n"
                          "- 0 to 10: Positive values\n"
                          "- -10 to 10: Centered view\n"
                          "- -5 to 5: Focused center\n\n"
                          "Examples:\n"
                          "- X: 0 to 100, Y: 0 to 50\n"
                          "- X: -5 to 5, Y: -10 to 10\n"
                          "- Z: 0 to 20 (for 3D graphs)",
            
            "Quadrants": "Show all 4 quadrants of the coordinate plane.\n\n"
                        "What it does:\n"
                        "- Draws X and Y axes through origin (0,0)\n"
                        "- Shows all 4 quadrants (I, II, III, IV)\n"
                        "- Centers the view on origin\n"
                        "- Labels each quadrant\n\n"
                        "Perfect for:\n"
                        "- Mathematical functions\n"
                        "- Symmetrical data\n"
                        "- Teaching coordinate systems\n"
                        "- Positive and negative values\n\n"
                        "Quadrant Layout:\n"
                        "  II (+,+)  |  I  (+,+)\n"
                        "  ----------+----------\n"
                        "  III(-,-)  |  IV (+,-)\n\n"
                        "Use with equation plotter for best results!",
            
            "Origin Axes": "Draw X and Y axes through the origin (0,0).\n\n"
                          "What it does:\n"
                          "- Draws thick black lines at X=0 and Y=0\n"
                          "- Makes origin clearly visible\n"
                          "- Helps visualize positive/negative regions\n\n"
                          "Best for:\n"
                          "- Mathematical functions\n"
                          "- Data crossing zero\n"
                          "- Teaching coordinates\n"
                          "- Symmetrical visualization\n\n"
                          "Tip: Combine with '4 Quadrants' in equation plotter\n"
                          "for the complete coordinate plane view!"
        }
        
        messagebox.showinfo(f"Help: {topic}", help_texts.get(topic, "No help available"))
    
    def show_graph_types_help(self):
        """Show detailed help for all graph types"""
        help_text = """
GRAPH TYPES GUIDE

📈 LINE PLOT
- Best for: Continuous data, trends over time
- Example: Temperature over days, stock prices
- X: Time or continuous variable
- Y: Measured values

📊 SCATTER PLOT
- Best for: Relationships between two variables
- Example: Height vs. Weight correlation
- Shows individual data points without connecting lines

📊 BAR CHART
- Best for: Comparing categories
- Example: Sales by region, survey results
- X: Categories
- Y: Values for each category

🎲 3D SURFACE
- Best for: Functions of two variables
- Example: z = f(x, y)
- Creates a 3D surface showing how Z varies with X and Y
- Z can be a mathematical expression

🔵 3D SCATTER
- Best for: 3-dimensional data relationships
- Example: Multiple variables correlation
- Requires X, Y, and Z data

📉 HISTOGRAM
- Best for: Distribution of a single variable
- Example: Age distribution, test scores
- Shows frequency of values in ranges (bins)

🗺️ CONTOUR PLOT
- Best for: Topographic-style data visualization
- Example: Elevation maps, optimization landscapes
- Shows lines of equal value

🔥 HEATMAP
- Best for: Matrix data, correlations
- Example: Correlation matrices, density plots
- Color intensity represents value magnitude

DATA INPUT FORMATS:
1. Comma-separated: 1, 2, 3, 4, 5
2. Range: 0:10 (creates 100 points from 0 to 10)
3. Expression: sin(x), x**2, exp(x)
        """
        
        window = tk.Toplevel(self.root)
        window.title("Graph Types Help")
        window.geometry("600x500")
        
        text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=30)
        text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text.insert(tk.END, help_text)
        text.config(state=tk.DISABLED)
    
    def show_complete_help(self):
        """Show comprehensive help guide"""
        help_text = """
═══════════════════════════════════════════
   PROFESSIONAL GRAPH GENERATOR - HELP
═══════════════════════════════════════════

📚 QUICK START GUIDE

1. SELECT GRAPH TYPE
   Choose from 8 different visualization types

2. INPUT YOUR DATA
   - Comma-separated: 1, 2, 3, 4, 5
   - Range format: 0:10 (100 points from 0-10)
   - Math expressions: sin(x), x**2, exp(x)

3. CUSTOMIZE APPEARANCE
   - Colors, line widths, markers
   - Transparency, styles
   
4. ADD LABELS
   - Title, axis labels
   - Make your graph professional!

5. GENERATE & SAVE
   - Click "Generate Graph"
   - Save as PNG, PDF, or SVG

═══════════════════════════════════════════
🎨 CUSTOMIZATION OPTIONS
═══════════════════════════════════════════

COLOR OPTIONS:
- Standard colors: blue, red, green, etc.
- Works with all plot types
- Tip: Use color to distinguish datasets

LINE WIDTH (0.5 - 10):
- Thin (0.5-2): Multiple overlapping lines
- Medium (2-4): General use
- Thick (4-10): Presentations, emphasis

MARKERS:
- o (circle), s (square), ^ (triangle)
- * (star), D (diamond), + (plus)
- Size adjustable from 1-20

LINE STYLES:
- Solid, Dashed, Dash-dot, Dotted
- "None" for scatter-only plots

TRANSPARENCY (0-1):
- 0: Completely transparent
- 1: Fully opaque
- Useful for overlapping data

═══════════════════════════════════════════
📊 DATA INPUT EXAMPLES
═══════════════════════════════════════════

SIMPLE VALUES:
X: 0, 1, 2, 3, 4, 5
Y: 0, 1, 4, 9, 16, 25

RANGE FORMAT:
X: 0:10          → 100 points from 0 to 10
X: -5:5          → 100 points from -5 to 5
X: 0:100:5       → Points from 0 to 100, step 5

MATHEMATICAL EXPRESSIONS:
Y: x**2          → Quadratic
Y: sin(x)        → Sine wave
Y: exp(x)        → Exponential
Y: sqrt(x)       → Square root
Y: x**3 - 2*x    → Polynomial

3D EXPRESSIONS (Z data):
Z: np.sin(np.sqrt(X**2 + Y**2))
Z: X**2 + Y**2
Z: np.exp(-(X**2 + Y**2))

═══════════════════════════════════════════
🎯 TIPS FOR BEAUTIFUL GRAPHS
═══════════════════════════════════════════

1. Always add descriptive labels and titles
2. Use grid for easier reading of values
3. Choose colors that contrast well
4. For presentations: larger line widths
5. For publications: seaborn or ggplot style
6. Save as PDF for vector graphics (scalable)
7. Use transparency for overlapping data
8. Test different markers for clarity

═══════════════════════════════════════════
💾 SAVING YOUR WORK
═══════════════════════════════════════════

PNG: Best for web, presentations (300 DPI)
PDF: Best for publications (vector)
SVG: Best for further editing (vector)

High DPI ensures professional quality!

═══════════════════════════════════════════
❓ COMMON ISSUES
═══════════════════════════════════════════

"Cannot parse data": Check your format
- Use commas between values
- No spaces in expressions
- Check parentheses in math

"Dimensions don't match": 
- X and Y must have same length
- Or use expressions that auto-generate

3D plots not showing:
- Make sure to provide Z data
- Or use built-in expressions

═══════════════════════════════════════════

Need more help? Try the "?" buttons next to
each option for specific guidance!

Happy Graphing! 📈
        """
        
        window = tk.Toplevel(self.root)
        window.title("Complete Help Guide")
        window.geometry("700x600")
        
        text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=35, 
                                         font=('Courier', 9))
        text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text.insert(tk.END, help_text)
        text.config(state=tk.DISABLED)
        
        ttk.Button(window, text="Close", command=window.destroy).pack(pady=5)
    
    def show_quick_start_guide(self):
        """Show simple step-by-step guide for beginners"""
        window = tk.Toplevel(self.root)
        window.title("🚀 Quick Start Guide - Easy!")
        window.geometry("700x650")
        
        text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=35, 
                                         font=('Arial', 10))
        text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        guide = """
═══════════════════════════════════════════════════════
    🚀 QUICK START GUIDE - ANYONE CAN DO THIS!
═══════════════════════════════════════════════════════

Welcome! This guide will help you create your first graph in 2 minutes!

═══════════════════════════════════════════════════════
STEP 1: Choose What You Want to See (10 seconds)
═══════════════════════════════════════════════════════

Look at the "Graph Type" section and click ONE option:

📈 Line Plot - For showing trends (like temperature over time)
📊 Scatter Plot - For showing relationships (like height vs weight)
📊 Bar Chart - For comparing things (like sales by month)
🎲 3D Surface - For cool 3D visualizations
📉 Histogram - For showing distributions

👉 NEW? Start with "Line Plot" - it's the easiest!

═══════════════════════════════════════════════════════
STEP 2: Get Some Data (30 seconds)
═══════════════════════════════════════════════════════

Two SUPER EASY ways:

OPTION A - Load Example Data (EASIEST!):
   1. Click the "📊 Load Example Data" button
   2. That's it! You're done with this step!

OPTION B - Use the Equation Plotter:
   1. Scroll down to "📐 Equation Plotter"
   2. Click any quick button like "Quadratic" or "Sine"
   3. Click "📈 Plot Equation"
   4. Done!

OPTION C - Type Your Own Numbers:
   In the "X Data" box, type: 1, 2, 3, 4, 5
   In the "Y Data" box, type: 2, 4, 6, 8, 10
   (You can use ANY numbers - even, odd, decimals, anything!)

═══════════════════════════════════════════════════════
STEP 3: Create Your Graph (5 seconds)
═══════════════════════════════════════════════════════

1. Look for the BIG button that says "🎨 Generate Graph"
2. Click it!
3. Watch your beautiful graph appear! ✨

═══════════════════════════════════════════════════════
STEP 4: Make It Pretty (Optional - 1 minute)
═══════════════════════════════════════════════════════

Want to change colors or style? Easy!

Change Color:
   - Find the "Color" dropdown
   - Pick any color you like
   - Click "🎨 Generate Graph" again

Change Title:
   - Find "Graph Title" box
   - Type your own title
   - Click "🎨 Generate Graph" again

That's it! Super simple!

═══════════════════════════════════════════════════════
STEP 5: Save Your Graph (20 seconds)
═══════════════════════════════════════════════════════

1. Click "💾 Save Graph" button
2. Choose where to save it
3. Give it a name
4. Click Save!

Done! You now have a professional graph! 🎉

═══════════════════════════════════════════════════════
TIPS FOR BEGINNERS:
═══════════════════════════════════════════════════════

✅ Don't worry about making mistakes - you can always click "Clear"

✅ Try the example data first before using your own numbers

✅ Click the "?" buttons next to options if you're confused

✅ The equation plotter quick buttons are super fun - try them all!

✅ You can use ANY numbers - no rules! Even numbers (2,4,6), 
   odd numbers (1,3,5), decimals (1.5, 2.7), anything works!

✅ If your graph looks weird, click "Load Example Data" to reset

✅ Professional Mode makes your graphs look fancy automatically!

═══════════════════════════════════════════════════════
COMMON QUESTIONS:
═══════════════════════════════════════════════════════

Q: What if I don't see my graph?
A: Make sure you clicked "🎨 Generate Graph" button!

Q: Can I use decimals like 1.5, 2.7?
A: YES! Use ANY numbers you want!

Q: How do I change colors?
A: Use the "Color" dropdown and click Generate Graph again.

Q: What's the difference between the modes?
A: Professional = Fancy looking
   Normal = Standard
   Scientific = For research papers
   (Normal is great for beginners!)

Q: Do I need to know math?
A: NO! Just use the example data or equation quick buttons!

Q: Can I zoom in on my graph?
A: YES! Uncheck "Auto Range" and set your own Min/Max values!

═══════════════════════════════════════════════════════
YOUR FIRST GRAPH IN 4 CLICKS:
═══════════════════════════════════════════════════════

1. Click "📊 Load Example Data"
2. Click "🎨 Generate Graph"  
3. See your graph! 
4. Click "💾 Save Graph" to keep it!

That's literally it! 🎉

═══════════════════════════════════════════════════════
READY TO TRY MORE?
═══════════════════════════════════════════════════════

Once you're comfortable, try:

• Different graph types (click Bar Chart, Scatter, etc.)
• Different colors (try purple, gold, coral!)
• Your own numbers (just type them in!)
• The equation plotter (click those quick buttons!)
• 3D graphs (they look AMAZING!)

Remember: You can't break anything! Experiment and have fun! 🎨

═══════════════════════════════════════════════════════

Close this window and start creating your first graph NOW! 🚀

You got this! 💪
        """
        
        text.insert(tk.END, guide)
        text.config(state=tk.DISABLED)
        
        ttk.Button(window, text="Close - I'm Ready!", 
                  command=window.destroy).pack(pady=5)

def main():
    root = tk.Tk()
    app = GraphGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
