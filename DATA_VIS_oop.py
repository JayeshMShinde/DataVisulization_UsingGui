import itertools
import tkinter as tk
from tkinter import PhotoImage, ttk, filedialog, messagebox
from tkinter.messagebox import showinfo, showwarning
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import seaborn as sns
import squarify
import waterfall_chart
import statsmodels.tsa.stattools as stattools

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


class App(tk.Tk):
 # Constructor of Class which is by default Main Window(Root Window)   
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_geometry(self, "1400x760")
        tk.Tk.wm_resizable(self, False, False)
        tk.Tk.grid_rowconfigure(self, 0, weight=1)
        tk.Tk.grid_columnconfigure(self, 1, weight=1)

      # Global Variables
        self.flag = 0
        self.fill_var = 0
        self.filepath = ""
        self.df = pd.DataFrame()
        self.x_col_barplot = []
        self.y_col_barplot = []

      # Side Bar
        self.cur_width = 50 # Increasing width of the frame
        self.expanded = False # Check if it is completely exanded

        self.SideBar_frame = tk.Frame(self, width=50, bg='grey')
        self.SideBar_frame.grid(row=0, column=0, sticky='NS')
        self.SideBar_frame.bind('<Enter>',lambda e: self.expand())                            # Event Binding Completed
        self.SideBar_frame.bind('<Leave>',lambda e: self.contract())                            # Event Binding Completed
        self.SideBar_frame.grid_propagate(False)

       # Side Bar Buttons
        self.Frame1_raise = ttk.Button(self.SideBar_frame, text="H", width=3, command= lambda : self.Frame_Raise_Func(1))
        self.Frame2_raise = ttk.Button(self.SideBar_frame, text="A", width=3, command= lambda : self.Frame_Raise_Func(2))
        self.Frame3_raise = ttk.Button(self.SideBar_frame, text="Ml", width=3, command= lambda : self.Frame_Raise_Func(3)) 
        self.Frame1_raise.grid(row=0, column=0, padx=5, pady=10)
        self.Frame2_raise.grid(row=0, column=0, padx=5, pady=10)
        self.Frame3_raise.grid(row=1, column=0, padx=5, pady=10)

      # Main Frames for Data Loading, Analytics , Ml Algos
        self.f1 = tk.Frame(self)
        self.f1.grid(row=0, column=0, columnspan=2, sticky='EWNS')
        self.f2 = tk.Frame(self)
        self.f2.grid(row=0, column=0, columnspan=2, sticky='EWNS')
        self.f3 = tk.Frame(self)
        self.f3.grid(row=0, column=0, columnspan=2, sticky='EWNS')
        self.f3.tkraise()
        self.SideBar_frame.tkraise()

      # Frame 1
       # Browse Load delete
        tk.Label(self.f1, text="...............  ").grid(row=0, column=0)
        self.Load_btn = ttk.Button(self.f1, text="Load File", command=self.Load_File_Func)
        self.Browse_btn = ttk.Button(self.f1, text="Browse File", command=self.Browse_File_Func)
        self.Delete_Data_btn = ttk.Button(self.f1, text="Delete File", command=self.Delete_File_Func)

        self.Browse_btn.grid(row=1, column=1, pady=10)
        self.Load_btn.grid(row=2, column=1)
        self.Delete_Data_btn.grid(row=2, column=2)

       # Sort, Delete Row, Nan and Outlier
        self.Sortby_btn = ttk.Button(self.f1, text="Sort By", command=self.Sortby_Window_func)
        self.Delete_Row_btn = ttk.Button(self.f1, text="Delete Row", command=self.DeleteRow_EventFunction)
        self.Nan_btn = ttk.Button(self.f1, text="Nan's", command=self.Nans_Window_func)
        self.Outlier_btn = ttk.Button(self.f1, text="Outlier", command=self.Outliers_Window_func)

        self.Sortby_btn.grid(row=3, column=1, pady=10)
        self.Delete_Row_btn.grid(row=3, column=2, padx=5)
        self.Nan_btn.grid(row=4, column=1)
        self.Outlier_btn.grid(row=4, column=2)

       # Remove, Replace, Entry for Replacing Value and Combo box for Column and Column Values
        self.Replace_Value_f1 = tk.StringVar()
        tk.Label(self.f1, text="Remove or Replace Selected Value").grid(row=5, column=1, pady=10, columnspan=2)
        tk.Label(self.f1, text="Select Column").grid(row=6, column=1, pady=10, columnspan=2)
        self.Remove_btn = ttk.Button(self.f1, text="Remove", command= lambda : self.Remove_Replace_func(0, self.Column_Name_ComboBox_f1.get()))
        self.Replace_btn = ttk.Button(self.f1, text="Replace", command= lambda : self.Remove_Replace_func(1, self.Column_Name_ComboBox_f1.get()))
        
        self.Column_Name_ComboBox_f1 = ttk.Combobox(self.f1, state='readonly', width=23)
        self.Column_Values_ComboBox_f1 = ttk.Combobox(self.f1, state='readonly', width=23)
        self.Replcae_Entry_f1 = tk.Entry(self.f1, textvariable=self.Replace_Value_f1, width=25)

        self.DropColumn_btn = ttk.Button(self.f1, text="DropCol", command= lambda : self.DropColumn_func(self.Column_Name_ComboBox_f1.get()))

        self.Column_Name_ComboBox_f1.grid(row=7, column=1, columnspan=2)
        tk.Label(self.f1, text="Select Value From Column").grid(row=8, column=1, pady=10, columnspan=2)
        self.Column_Values_ComboBox_f1.grid(row=9, column=1, columnspan=2, pady=5, padx=5)

        self.Remove_btn.grid(row=10, column=1)
        self.DropColumn_btn.grid(row=10, column=2)
        tk.Label(self.f1, text="Enter Value to Replace").grid(row=11, column=1, pady=10, columnspan=2)
        self.Replcae_Entry_f1.grid(row=12, column=1, columnspan=2, pady=5)
        self.Replace_btn.grid(row=13, column=1, sticky="N")
        
        self.Column_Name_ComboBox_f1.bind("<<ComboboxSelected>>", lambda e: self.Colmun_Name_and_Value_Selected_Func(self.Column_Name_ComboBox_f1.get()))

       # TreeView
        self.f1.columnconfigure(3, weight=1)
        self.f1.rowconfigure(13, weight=1)

        self.tree = ttk.Treeview(self.f1)
        self.scrollbar_ver = ttk.Scrollbar(self.f1, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_hori = ttk.Scrollbar(self.f1, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.scrollbar_ver.set,xscrollcommand=self.scrollbar_hori.set)
        self.tree.bind("<Delete>", lambda e: self.DeleteRow_EventFunction())

        self.tree.grid(row=0, column=3, rowspan=14, sticky="EWNS")
        self.scrollbar_ver.grid(row=0, column=4, rowspan=13, sticky="WNS")
        self.scrollbar_hori.grid(row=14, column=3, sticky="EW")

      # Frame 2
        tk.Label(self.f2, text=".............  ").grid(row=0, column=0)
        self.f2.rowconfigure(0, weight=1)
        self.f2.columnconfigure(1, weight=1)
        self.PlotFrame_Plot_f2 = tk.Frame(self.f2, bg='orange')
        self.PlotFrame_Btn_f2 = tk.Frame(self.f2)
        self.PlotFrame_Plot_f2.grid(row=0, column=1, sticky="EWNS")
        self.PlotFrame_Btn_f2.grid(row=0, column=2, sticky="EWNS")

       # Buttons for Graphs and Plots in PlotFrame_Btn_f2
        tk.Label(self.PlotFrame_Btn_f2, text="Plots and Graphs").grid(row=0, column=0, padx=5, pady=10, columnspan=4)
        tk.Label(self.PlotFrame_Btn_f2, text="").grid(row=1, column=0)
        tk.Label(self.PlotFrame_Btn_f2, text=" ").grid(row=1, column=5)
       
       # Plot Buttons Images
        p1 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/25.png")  # Barplot
        self.Barplot = p1.subsample(5, 5)
        p2 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/SP.png")  # Scatterplot
        self.Scatterplot = p2.subsample(6, 6)
        p3 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/27.png")  # PieChart
        self.PieChart = p3.subsample(5, 5)
        p4 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/28.png")  # Histogram
        self.Histogram = p4.subsample(7, 7)
        p5 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/26.png")  # LineChart
        self.LineChart = p5.subsample(5, 5)
        p6 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/box-plot.png")  # boxplot
        self.Boxplot = p6.subsample(5, 5)
        p7 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/TM.png")  # TreeMap
        self.TreeMap = p7.subsample(15, 15)
        p8 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/HM.png")  # Heatmap
        self.HeatMap = p8.subsample(7, 7)
        p9 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/29.png")  # Dountplot
        self.Dountchart = p9.subsample(6, 6)
        p10 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/30.png")  # Dountplot
        self.Lolipop = p10.subsample(6, 6)
        p11 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/31.png")  # violinPlot
        self.violin = p11.subsample(6, 6)
        p12 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/32.png")  # Densityplot
        self.Densityplot = p12.subsample(6, 6)
        p13 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/33.png")  # PairWiseplot
        self.PairWiseplot = p13.subsample(10, 8)
        p14 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/34.png")  # Waterfallplot
        self.Waterfallplot = p14.subsample(6, 6)
        p15 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/36.png") # CrossCorrelationplot
        self.CrossCorrelationplot = p15.subsample(8, 7)
        p16 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/37.png")  # AreaChart
        self.AreaChart = p16.subsample(26, 26)
        p17 = tk.PhotoImage(file=r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/38.png")  # StackAreaChart
        self.StackAreaChart = p17.subsample(15, 15)
        p18 = tk.PhotoImage(file = r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/40.png")# 3d scatterplots
        self.ThreeDimensional = p18.subsample(14,14)
        p19 = tk.PhotoImage(file = r"C:/Users/LENOVO/OneDrive/Desktop/Project_4-3-2022/Icon/41.png") #  Surface plot
        self.Surfaceplt = p19.subsample(5,5)

       # Plot Buttons Declaration and Grid
        self.BarPlot_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.Barplot, height=35, width=35, command=self.bar_plot_selected)
        self.ScatterPlot_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.Scatterplot, height=35, width=35, command=self.scatter_plot_selected)
        self.PieChart_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.PieChart, height=35, width=35, command=self.pie_plot_selected)        
        self.Histogram_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.Histogram, height=35, width=35, command=self.histogram_plot_selected)
        self.LineChart_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.LineChart, height=35, width=35, command=self.line_plot_selected)
        self.Boxplot_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.Boxplot, height=35, width=35, command=self.box_plot_selected)
        self.TreeMap_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.TreeMap, height=35, width=35, command=self.treemap_plot_selected)
        self.HeatMap_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.HeatMap, height=35, width=35, command=self.heatmap_plot_selected)

        self.Donutchart_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.Dountchart, height=35, width=35, command=self.donut_plot_selected)
        self.Lollipop_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.Lolipop, height=35, width=35, command=self.lollipop_plot_selected)
        self.violin_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.violin, height=35, width=35, command=self.violin_plot_selected)

        self.Densityplot_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.Densityplot, height=35, width=35, command=self.density_plot_selected)
        self.PairWiseplot_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.PairWiseplot, height=35, width=35, command=self.pairwise_plot_selected)
        self.Waterfallplot_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.Waterfallplot, height=35, width=35, command=self.waterfall_plot_selected)
        self.CrossCorrelationplot_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.CrossCorrelationplot, height=35, width=35, command=self.crosscorr_plot_selected)
        self.AreaChart_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.AreaChart, height=35, width=35, command=self.area_plot_selected)
        self.StackAreaChart_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.StackAreaChart, height=35, width=35)
        self.ThreeDimensional_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.ThreeDimensional, height=35, width=35,command = self._3d_Scaterplot_selected)
        self.Surfaceplt_btn = tk.Button(self.PlotFrame_Btn_f2, image=self.Surfaceplt, height=35, width=35,command = self._3d_SurfacePlot_selected)
    
       # GRID of Buttons 
        self.BarPlot_btn.grid(row=1, column=1, padx=5, pady=5)
        self.ScatterPlot_btn.grid(row=2, column=1, pady=5)
        self.PieChart_btn.grid(row=3, column=1, pady=5)
        self.Histogram_btn.grid(row=4, column=1, pady=5)
        self.LineChart_btn.grid(row=5, column=1, pady=5)

        self.Boxplot_btn.grid(row=1, column=2)
        self.TreeMap_btn.grid(row=2, column=2)
        self.HeatMap_btn.grid(row=3, column=2)
        self.Donutchart_btn.grid(row=4, column=2)
        self.Lollipop_btn.grid(row=5, column=2)

        self.violin_btn.grid(row=1, column=3, padx=5)
        self.Densityplot_btn.grid(row=2, column=3)
        self.PairWiseplot_btn.grid(row=3, column=3)
        self.Waterfallplot_btn.grid(row=4, column=3)
        self.CrossCorrelationplot_btn.grid(row=5, column=3)

        self.AreaChart_btn.grid(row=1, column=4)
        self.StackAreaChart_btn.grid(row=2, column=4)
        self.ThreeDimensional_btn.grid(row=3, column=4)
        self.Surfaceplt_btn.grid(row=4, column=4)


      # Frame 3
       # Frame 3 Variables
        
        self.train_percentage = tk.IntVar()
       #
        self.f3.rowconfigure(0, weight=1)
        tk.Label(self.f3, text=".............  ").grid(row=0, column=0)
        self.MachineLearningAlgorithm_Frame = ttk.LabelFrame(self.f3, text="Machine Learning Algorithm")
        self.MachineLearningAlgorithm_Frame.grid(row=0, column=1, sticky="NSEW")

        self.PropertiesMachineLearningAlgorithm_Frame = ttk.LabelFrame(self.f3, text="Properties Of Algorithm", width=1000)
        self.PropertiesMachineLearningAlgorithm_Frame.grid(row=0, column=2, sticky="NSEW")
        self.PropertiesMachineLearningAlgorithm_Frame.grid_propagate(False)


       # Widgets of MachineLearningAlgorithm_Frame 
        self.Linear_Regression_Button = ttk.Button(self.MachineLearningAlgorithm_Frame, text="Linear\nRegression", command=self.LinearRegression_Window)
        self.Linear_Regression_Button.grid(row=1, column=1, padx=10, pady=10)



       # Widgets of PropertiesMachineLearningAlgorithm_Frame 
       










 # Constructor End

 # Side Bar Functionality Which Includes ( Expantion and Contraction of Side Bar) and ( Frame Raise Function to Navigate Other Frames )
    def expand(self): # Complete
        self.cur_width += 55 # Increase the width by 10
        self.SideBar_frame.config(width=self.cur_width) # Change the width to new increase width
        self.expanded = True # Frame is expended
        self.fill()

    def contract(self): # Complete
        self.cur_width -= 55 # Increase the width by 10
        self.SideBar_frame.config(width=self.cur_width) # Change the width to new increase width
        self.expanded = False # Frame is expended
        self.fill()

    def fill(self): # Complete
        if self.expanded: # If the frame is Expanding
            if self.fill_var == 1 or self.fill_var == 0:
                self.Frame2_raise.config(text="Analytics", width=10)
                self.Frame3_raise.config(text="ML Algo", width=10)
            elif self.fill_var == 2:
                self.Frame1_raise.config(text="Home", width=10)
                self.Frame3_raise.config(text="ML Algo", width=10)
            elif self.fill_var == 3:
                self.Frame1_raise.config(text="Home", width=10)
                self.Frame2_raise.config(text="Analytics", width=10)
            else:
                print("Something Went Wrong in fill function")
        else: # If Frame is Contracted/Collapsed
            if self.fill_var == 1 or self.fill_var == 0:
                self.Frame2_raise.config(text="A", width=3)
                self.Frame3_raise.config(text="ML", width=3)
            elif self.fill_var == 2:
                self.Frame1_raise.config(text="H", width=3)
                self.Frame3_raise.config(text="ML", width=3)
            elif self.fill_var == 3:
                self.Frame1_raise.config(text="H", width=3)
                self.Frame2_raise.config(text="A", width=3)

    def Frame_Raise_Func(self, indicator=None): # Complete
        if indicator == 1:
            self.f1.tkraise()
            self.Frame1_raise.grid_forget()
            self.Frame2_raise.grid_forget()
            self.Frame3_raise.grid_forget()
            self.Frame2_raise.grid(row=0, column=0, padx=5, pady=10)
            self.Frame3_raise.grid(row=1, column=0, padx=5, pady=10)
        elif indicator == 2:
            self.f2.tkraise()
            self.Frame1_raise.grid_forget()
            self.Frame2_raise.grid_forget()
            self.Frame3_raise.grid_forget()
            self.Frame1_raise.grid(row=0, column=0, padx=5, pady=10)
            self.Frame3_raise.grid(row=1, column=0, padx=5, pady=10)
        elif indicator == 3:
            self.f3.tkraise()
            self.Frame1_raise.grid_forget()
            self.Frame2_raise.grid_forget()
            self.Frame3_raise.grid_forget()
            self.Frame1_raise.grid(row=0, column=0, padx=5, pady=10)
            self.Frame2_raise.grid(row=1, column=0, padx=5, pady=10)
        else:
            print("Something Went Wrong in 'Frame_Raise_Func' !!!!!!!!!")
        if self.fill_var == 0: 
            self.fill_var = indicator
            self.fill()
        self.fill_var = indicator
        self.SideBar_frame.tkraise()

 # Frame 1 Functionality Which Includes (Browsing and Loading File) , ( Creating TreeView ), ()
  
  # Browse & Load File, Delete and Create TreeView 
    def Load_File_Func(self): # Complete
        print("Load File Function Called")
        if len(self.filepath) == 0:
            showwarning("No File Selected", "Please Select The File First And Then Load")
        else:
            path1 = str(self.filepath)
            if path1[-3] == 'c':
                print("Csv File Loaded")
                self.df = pd.read_csv(self.filepath)
            elif path1[-3] == 'l':
                print("Xlsx File Loaded")
                self.df = pd.read_excel(self.filepath)
            else:
                print("Something Went Wrong in Load_File_Func")
                return
            self.Create_TreeView_Func()

    def Browse_File_Func(self): # Completed
        print("Browse File Function Called")
        ft = (("CSV file", ".csv"), ("xlsx files", ".xlsx"))
        self.filepath = filedialog.askopenfilename(initialdir="/", title="Select A File", filetype=ft)

    def Delete_File_Func(self): # Complete
        print("Delete File Function Called")
        self.tree.delete(*self.tree.get_children())
        for column in self.tree["column"]: 
            self.tree.delete(*self.tree.heading(column, text=" "))
        self.flag = 0
        pass

    def Create_TreeView_Func(self): # Complete
        if(self.flag == 1):
            self.tree.delete(*self.tree.get_children())
            for column in self.tree["column"]: self.tree.delete(*self.tree.heading(column, text=" "))
        column = [x for x in self.df.columns]
        self.Column_Name_ComboBox_f1['values'] = (column)
        self.Column_Name_ComboBox_f1.set('')
        self.tree.configure(columns=column, show='headings')
        for col in column:
            self.tree.heading(col, text=col)
        ctr = 0
        for row in range(len(self.df)):
            self.tree.insert("", "end", id=ctr,values=self.df.iloc[row].tolist())
            ctr +=1
        self.flag = 1

    def Colmun_Name_and_Value_Selected_Func(self, colname): # Complete
        distinct_elements = self.df[colname].unique()
        distinct_elements = [ x for x in distinct_elements if x == x]
        self.Column_Values_ComboBox_f1['values'] = (distinct_elements)
        self.Column_Values_ComboBox_f1.set('')

    def Remove_Replace_func(self, indicator, colname): # Complete
        val = self.Column_Values_ComboBox_f1.get()  # Retrieving The Specified Value for Removing/Replacing 
        val1 = self.Replace_Value_f1.get()          # Retrieving The Value Entered in Entry Box
        # --------- Checking Data Type of Value
        dt = self.df[colname].dtype     
        if (dt == np.int64):
            val = np.int64(val)
            val1 = np.int64(val1)
        elif(dt == np.float64):
            val = np.float64(val)
            val1 = np.float64(val1)

        idx =  self.df.index[self.df[colname] == val].tolist() # Retrieving The Indexes for Specified Value

        if indicator == 0:
            self.df = self.df.drop(labels=idx, axis=0)  # Drop Specified Value by index
            # ----------         
            for i in idx:                               # Deleting Specified Value from TreeView
                self.tree.delete(i)
            showinfo("Task Completed", message=f"{val} Has Been Successfully Dropped")
        else:
            self.df.loc[idx, colname] = val1 # Updating Specified Value in DataFrame
            # ----------
            for i in idx:                               # Updating the TreeView
                curItem = [x for x in self.df.loc[i]]   
                self.tree.item(i, values=tuple(curItem))
            showinfo("Task Completed", message=f"{val} Has Been Successfully Updated by {val1}")

    def DropColumn_func(self, colname): # Complete
        self.df.drop(colname, axis=1, inplace=True)
        self.df.reset_index(inplace = True, drop = True)
       # Delete Previous TreeView 
        self.tree.delete(*self.tree.get_children())
        for column in self.tree["column"]: 
            self.tree.delete(*self.tree.heading(column, text=" "))
       # Create New TreeView    
        self.Create_TreeView_Func()     
        
  # Sortby, Delete Row , Nans and Outliers
    def Sortby_Window_func(self): # Complete
        print("Sortby Window is Created")
        sortby_top = tk.Toplevel()
        sortby_top.geometry("420x210")
        sortby_top.resizable(False, False)
        colname = [x for x in self.df.columns]
        tk.Label(sortby_top, text="Select Column To Sort").pack()
        cbo_box = ttk.Combobox(sortby_top, values=colname, state='readonly')
        cbo_box.pack(pady=10)
        var = tk.IntVar(value=1)
        radio1 = ttk.Radiobutton(sortby_top, text="Ascending", variable=var, value=1)
        radio2 = ttk.Radiobutton(sortby_top, text="Descending", variable=var, value=0)
        radio1.pack()
        radio2.pack()
        ttk.Button(sortby_top, text="Sort", command=lambda:self.sort_fun(cbo_box.get(), var.get())).pack(pady=5)
    
    def sort_fun(self, col_selected, AorD): # Completed
        self.df.sort_values(by=col_selected, ascending=AorD,inplace=True)
        self.df.reset_index(inplace = True, drop = True)
        for row in range(len(self.df)):
            self.tree.item(row,values=self.df.iloc[row].tolist())
        
    def DeleteRow_EventFunction(self): # Complete
        row = self.tree.selection()
        if len(row) == 0:
            showwarning("Warning", message="Select The Row First")
        else:
            # print("Delete Row | Row Index = ", row)
            try:
                # Go Through All Selected Rows From Table/DataFrame
                for xr in row:
                    self.tree.delete(xr)
                    self.df.drop(int(xr), inplace=True)
            except:
                print('DeleteRow_EventFunction | Unexpected Error')
        
    def Nans_Window_func(self): # Complete
        print("Nan Window is Created")
        rplc_nan_str = tk.StringVar()
        self.Nan_top = tk.Toplevel()
        self.Nan_top.geometry("420x210")
        self.Nan_top.grab_set()
        colname = self.df.columns[self.df.isna().any()].tolist()
        tk.Label(self.Nan_top, text="Select Column Which Contains Nan").grid(row=0, column=0, columnspan=4, sticky="W", padx=10)
        cbo_box = ttk.Combobox(self.Nan_top, values=colname, state='readonly')
        cbo_box.grid(row=1, column=0, columnspan=4, sticky="W", padx=10)
        cbo_box.bind("<<ComboboxSelected>>", lambda e: self.callbackFunc(cbo_box.get()))
        ttk.Button(self.Nan_top, text="DropNan", command=lambda : self.Drop_Nan_and_OutLiers(cbo_box.get(),0,0,0)).grid(row=2, column=0, padx=10, pady=10, sticky="W")

        self.nan_sum = ttk.Button(self.Nan_top, text="Sum", command=lambda:self.ReplaceNanBy_Sum_Mean_Median_Mode(0, cbo_box.get()))
        self.nan_mean = ttk.Button(self.Nan_top, text="Mean", command=lambda:self.ReplaceNanBy_Sum_Mean_Median_Mode(1, cbo_box.get()))
        self.nan_median = ttk.Button(self.Nan_top, text="Median", command=lambda:self.ReplaceNanBy_Sum_Mean_Median_Mode(2, cbo_box.get())) 
        self.nan_mode = ttk.Button(self.Nan_top, text="Mode", command=lambda:self.ReplaceNanBy_Sum_Mean_Median_Mode(3, cbo_box.get())) 
        
        self.nan_txt_ent = ttk.Entry(self.Nan_top, textvariable=rplc_nan_str)
        self.nan_specific = ttk.Button(self.Nan_top, text="Specified Values", command=lambda:self.ReplaceNanInStringBy_SpecificValue(0, rplc_nan_str.get(), cbo_box.get()))
        self.nan_mode1 = ttk.Button(self.Nan_top, text="Mode Values", command=lambda:self.ReplaceNanInStringBy_SpecificValue(1, rplc_nan_str.get(), cbo_box.get()))
    
    def callbackFunc(self, colname): # Complete
        dt = self.df[colname].dtype
        if (dt == np.int64) or (dt == np.float64):
            self.nan_sum.grid(row=2, column=1, padx=5)
            self.nan_mean.grid(row=2, column=2, padx=5)
            self.nan_median.grid(row=3, column=1, padx=5)
            self.nan_mode.grid(row=3, column=2, padx=5)
            self.nan_txt_ent.grid_forget()
            self.nan_specific.grid_forget()
            self.nan_mode1.grid_forget()
        else:
            self.nan_txt_ent.grid(row=2, column=1, padx=5)
            self.nan_specific.grid(row=3, column=2, padx=5)
            self.nan_mode1.grid(row=3, column=1, padx=5)
            self.nan_sum.grid_forget()
            self.nan_mean.grid_forget()
            self.nan_median.grid_forget()
            self.nan_mode.grid_forget()
    
    def ReplaceNanBy_Sum_Mean_Median_Mode(self, indicator, colname): # Complete
        idx = np.where(self.df[colname].isna())[0] # Finding Index of all Nan Values Present in Column of DataFrame
        if indicator == 0:                  # For Sum
            IQR = self.df[colname].sum()
        elif  indicator == 1:               # For Mean
            IQR = self.df[colname].mean()
        elif  indicator == 2:               # For Median
            IQR = self.df[colname].median()
        elif indicator == 3:                # For Mode
            IQR = self.df[colname].mode()[1]
        
        self.df[colname].fillna(IQR, inplace=True) # Filling/Replacing all Nan Values Present in Column of DataFrame
        
        for i in idx:                               # Updating the TreeView
            curItem = [x for x in self.df.loc[i]]   
            self.tree.item(i, values=tuple(curItem))
        showinfo("Task Completed", message=f"NaN Values Has Been Successfully Replaced By {IQR}")

    def ReplaceNanInStringBy_SpecificValue(self, indicator, val, colname): # Complete
        idx = np.where(self.df[colname].isna())[0] # Finding Index of all Nan Values Present in Column of DataFrame
        if indicator == 0:               # For Specified Value
            self.df[colname].fillna(val, inplace=True)
        elif indicator == 1:             # For Mode
            val = self.df[colname].mode(dropna=True)[0]
            self.df[colname].fillna(val, inplace=True)
        else:
            print("Some Thing Went Wrong")
        # ----------
        for i in idx:                               # Updating the TreeView
            curItem = [x for x in self.df.loc[i]]   
            self.tree.item(i, values=tuple(curItem))
        showinfo("Task Completed", message=f"NaN Values Has Been Successfully Replaced By = {val}")

    def Outliers_Window_func(self): # Complete
        print("Outliers Window is Created")
        OutLier_Win = tk.Toplevel(self)
        OutLier_Win.title("Outlier Window")
        OutLier_Win.geometry('850x500')
        OutLier_Win.resizable(False, False)
        OutLier_Win.rowconfigure(0, weight=1)
        OutLier_Win.columnconfigure(1, weight=1)

        self.ol_f1 = tk.Frame(OutLier_Win)
        self.ol_f2 = tk.Frame(OutLier_Win, padx=10)
        self.ol_f1.grid(row=0, column=0)
        self.ol_f2.grid(row=0, column=1, sticky="W")

        Upper_Limit = tk.DoubleVar()
        Lower_Limit = tk.DoubleVar()
        colname = [x for x in self.df.columns]
        
        tk.Label(self.ol_f1, text="Select The Column ").grid(row=0, column=0, columnspan=2, padx=15, pady=15)
        cbo_box = ttk.Combobox(self.ol_f1, values=colname, state='readonly')
        cbo_box.grid(row=1, column=0, columnspan=4, sticky="W", padx=10)
        cbo_box.bind("<<ComboboxSelected>>", lambda e: self.Plot_Outlier_to_ol_f2(cbo_box.get()))

        tk.Label(self.ol_f1, text="Select The Preferred Operation").grid(row=2, column=0, columnspan=2, padx=15, pady=15)
        tk.Label(self.ol_f1, text="Set Limits\nIn Range of 0-1").grid(row=3, column=0, padx=15, rowspan=1) # 1= 3, 2 =4, 3=4
        tk.Label(self.ol_f1, text="Upper Limit").grid(row=3, column=1, padx=15, sticky='w')
        tk.Label(self.ol_f1, text="Lower Limit").grid(row=4, column=1, padx=15, sticky='w')
        tk.Entry(self.ol_f1, textvariable=Upper_Limit, width=5).grid(row=3, column=2, sticky='w')
        tk.Entry(self.ol_f1, textvariable=Lower_Limit, width=5).grid(row=4, column=2, sticky='w')
        tk.Label(self.ol_f1, text="Drop / Remove").grid(row=5, column=0, padx=15)
        tk.Label(self.ol_f1, text="Replace By ").grid(row=5, column=1, padx=15)
        # - Drop Outliers Button
        ttk.Button(self.ol_f1, text="Drop OutLiers", command=lambda : self.Drop_Nan_and_OutLiers(cbo_box.get(), Upper_Limit.get(), Lower_Limit.get(), 1)).grid(row=6, column=0)

        ttk.Button(self.ol_f1, text="IQR", command= lambda : self.ReplaceOutliersBy_IQR_Mean_Median_Mode(cbo_box.get(), Upper_Limit.get(), Lower_Limit.get(), 0)).grid(row=6, column=1)
        ttk.Button(self.ol_f1, text="Mean", command= lambda : self.ReplaceOutliersBy_IQR_Mean_Median_Mode(cbo_box.get(), Upper_Limit.get(), Lower_Limit.get(), 1)).grid(row=6, column=2)
        ttk.Button(self.ol_f1, text="Median", command= lambda : self.ReplaceOutliersBy_IQR_Mean_Median_Mode(cbo_box.get(), Upper_Limit.get(), Lower_Limit.get(), 2)).grid(row=7, column=1)
        ttk.Button(self.ol_f1, text="Mode", command= lambda : self.ReplaceOutliersBy_IQR_Mean_Median_Mode(cbo_box.get(), Upper_Limit.get(), Lower_Limit.get(), 3)).grid(row=7, column=2)

        ttk.Button(self.ol_f1, text="Close Window", command=OutLier_Win.destroy).grid(row=8, column=0)
        OutLier_Win.grab_set()
        
    def ReplaceOutliersBy_IQR_Mean_Median_Mode(self, colname, upper_limit, lower_limit,indicator): # Complete
        print(f"Col = {colname} | Indicator = {indicator}\nUpper Limit = {upper_limit} | Lower Limit = {lower_limit}")
        if(upper_limit < 1.0 and lower_limit > 0.0) and (lower_limit < 1.0 and upper_limit > 0.0):
            dt = self.df[colname].dtypes
            if  indicator == 1:                 # For Mean
                if (dt == np.int64):
                    IQR = np.int64(self.df[colname].mean())
                else:
                    IQR = self.df[colname].mean()
                print("Mean = ",IQR)
            elif  indicator == 2:               # For Median
                if (dt == np.int64):
                    IQR = np.int64(self.df[colname].mean())
                else:
                    IQR = self.df[colname].mean()
                print("Median = ",IQR)
            elif indicator == 3:                # For Mode
                IQR = self.df[colname].mode()[1]
                print("Mode = ",IQR)
            else:                               # For IQR
                Q1 = self.df[colname].quantile(0.25)
                Q3 = self.df[colname].quantile(0.75)
                if (dt == np.int64):
                    IQR = np.int64(Q3-Q1)
                else:
                    IQR = Q3-Q1
                print("InterQuartile Range = ",IQR)

            upper_limit = self.df[colname].quantile(upper_limit)    # - Getting Quantile Value for Upper Limit
            lower_limit = self.df[colname].quantile(lower_limit)    # - Getting Quantile Value for Lower Limit

            idx =  self.df.index[self.df[colname] >= upper_limit].tolist()    # - Getting Index of Upper Limit
            idx +=  self.df.index[self.df[colname] <= lower_limit].tolist()    # - Getting Index of Lower Limit
            idx = sorted(idx)       # - Sorting to Make Algo Perform Better

            self.df.loc[idx, colname] = IQR # Updating Value in DataFrame
            # ----------
            for i in idx:                               # Updating the TreeView
                curItem = [x for x in self.df.loc[i]]   
                self.tree.item(i, values=tuple(curItem))
            # - Refresh the Box Plot    
            self.Plot_Outlier_to_ol_f2(colname)
        else:
            showwarning("Warning", message="Set Upper Limit and Lower Limit\nIn Range of ( 0.0 - 1.0 )")

    def Plot_Outlier_to_ol_f2(self, colname): # Completed
        dt = self.df[colname].dtype
        if (dt == np.int64) or (dt == np.float64):
            fig = Figure(figsize=(5, 5), dpi=100)
            # Create a plot on that figure
            plot = fig.add_subplot(111)
            plot.boxplot(self.df[colname])
            # Create a canvas widget from the figure
            canvas = FigureCanvasTkAgg(fig, master=self.ol_f2)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0)
        else:
            showwarning("Warning", message="Select The Column Which Contains Numeric Values")

    def Drop_Nan_and_OutLiers(self, colname, upper_limit, lower_limit, indicator): # Complete
        if indicator == 0:
            idx =  self.df.index[self.df[colname] != self.df[colname]].tolist()
            self.df = self.df.drop(labels=idx, axis=0)  # Drop Nan by index
            # ----------         Deleting Nan from TreeView
            for i in idx:                               
                self.tree.delete(i)
            self.Nan_top.destroy()
            showinfo("Task Completed", message="NaN Values Has Been Successfully Dropped")
            self.Nans_Window_func()
        else:
            if(upper_limit < 1.0 and lower_limit > 0.0) and (lower_limit < 1.0 and upper_limit > 0.0):
                upper_limit = self.df[colname].quantile(upper_limit)    # - Getting Quantile Value for Upper Limit
                lower_limit = self.df[colname].quantile(lower_limit)    # - Getting Quantile Value for Lower Limit
                # ----------    Indexes That Connects TreeView and Dataframe
                ridx = np.asarray(self.df.index)
                idx =  self.df.index[self.df[colname] >= upper_limit].tolist()      # - Getting Index of Upper Limit
                idx +=  self.df.index[self.df[colname] <= lower_limit].tolist()     # - Getting Index of Lower Limit
                idx = sorted(idx)                                                   # - Sorting to Make Algo Perform Better
                # ----------  Dropping the Outliers
                self.df.drop(idx, axis=0, inplace=True)
                # ----------  Resetting Index
                ridx = np.setdiff1d(ridx, idx)
                self.df.set_index(ridx)
                # ----------  Deleting Outliers from TreeView
                for i in idx:          
                    self.tree.delete(i)
                # ----------  Refresh the Box Plot    
                showinfo("Task Completed", message="NaN Values Has Been Successfully Dropped")
                self.Plot_Outlier_to_ol_f2(colname)
            else:
                showwarning("Warning", message="Set Upper Limit and Lower Limit\nIn Range of ( 0.0 - 1.0 )")

 # Frame 2 Functionality Which Includes (Plotting 2D and 3D Graphs)
  # Bar Plot
    def bar_plot_selected(self):
        stackvar = tk.BooleanVar(value=0)
        subplotvar = tk.BooleanVar(value=0)
        barplot_window = tk.Toplevel()
        plotname = tk.StringVar(value='bar')
        barplot_window.geometry("720x460")
        colname = [x for x in self.df.columns]
        tk.Label(barplot_window, text="Bar Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(barplot_window, text="Select X-axis variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(barplot_window, values=colname)
        tk.Label(barplot_window, text="Select Y-axis variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(barplot_window, values=colname)
        tk.Label(barplot_window, text="Measure/Aggregate").grid(row=5,column=0, padx=10, pady=10, sticky='W')
        aggregate_type = ttk.Combobox(barplot_window, values=['sum', 'mean', 'median', 'max', 'min', 'standard deviation', 'variance','none'])
        aggregate_type.set('none')
        xbar_combo_box.grid(row=2, column=0, padx=10)
        ybar_combo_box.grid(row=4, column=0, padx=10)
        aggregate_type.grid(row=6, column=0, padx=10)
        tk.Checkbutton(barplot_window, text="Stacked Plot", variable=stackvar, onvalue=1, offvalue=0).grid(row=7, column=0, padx=10,sticky='W')
        tk.Checkbutton(barplot_window, text="Sub-Plot", variable=subplotvar, onvalue=1, offvalue=0).grid(row=8, column=0, padx=10, sticky='W')
        tk.Checkbutton(barplot_window, text="On : Vertical BarPlot    \nOff : Horizontal Barplot", variable=plotname, onvalue='bar', offvalue='barh').grid(row=9, column=0, padx=10, sticky='W')
        ttk.Button(barplot_window, text="Plot", command=lambda : self.Plot_BarPlot(plotname=plotname.get(), agg=aggregate_type.get(), stack=stackvar.get(), subplt=subplotvar.get() )).grid(row=10, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(barplot_window, text="Variables selected for X axis are :")
        self.y_axis_barplot_label = tk.Label(barplot_window, text="Variables selected for Y axis are :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xybarplot(xbar_combo_box.get(), 0))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xybarplot(ybar_combo_box.get(), 1))

        barplot_window.bind("<Destroy>", lambda e:self.destroyed())

    def lbl_xybarplot(self, colname, indicator):
        if indicator==0:
            if colname not in self.x_col_barplot:
                self.x_col_barplot.append(str(colname))
            else:
                self.x_col_barplot.remove(colname)
            x = "Variables selected for X axis are :"
            ctr = 0
            for i in self.x_col_barplot:
                x = x + f"\n{i}"
            self.x_axis_barplot_label.configure(text=x)
        else:
            if colname not in self.y_col_barplot:
                self.y_col_barplot.append(str(colname))
            else:
                self.y_col_barplot.remove(colname)
            y = "Variables selected for X axis are :"
            for i in self.y_col_barplot:
                y = y + f"\n{i}"
            self.y_axis_barplot_label.configure(text=y)

    def Plot_BarPlot(self, plotname, agg, stack, subplt):
        if agg == 'sum':
            gdf = self.df.groupby(by=self.x_col_barplot)[self.y_col_barplot].sum()
        elif agg == 'mean':
            gdf = self.df.groupby(by=self.x_col_barplot)[self.y_col_barplot].mean()
        elif agg == 'median':
            gdf = self.df.groupby(by=self.x_col_barplot)[self.y_col_barplot].median()
        elif agg == 'max':
            gdf = self.df.groupby(by=self.x_col_barplot)[self.y_col_barplot].max()
        elif agg == 'min':
            gdf = self.df.groupby(by=self.x_col_barplot)[self.y_col_barplot].min()
        elif agg == 'standard deviation':
            gdf = self.df.groupby(by=self.x_col_barplot)[self.y_col_barplot].std()
        elif agg == 'variance':
            gdf = self.df.groupby(by=self.x_col_barplot)[self.y_col_barplot].var()
        else:
            x = self.df[self.x_col_barplot]
            y = self.df[self.y_col_barplot]
            xl = len(self.x_col_barplot)
            yl = len(self.y_col_barplot)
            i1 = 1
            ii = xl*yl
            if plotname == 'barh': # For Horizontal BarPlot
                if ii > 1:
                    for i in self.x_col_barplot:
                        for j in self.y_col_barplot:
                            if i1<=ii:
                                plt.subplot(xl, yl, i1)
                                plt.barh(x[i], y[j])
                                plt.legend(loc='lower right')
                                plt.title(f"{i}x{j}")
                                plt.tight_layout()
                                i1 +=1
                else:
                    for i in self.x_col_barplot:
                        for j in self.y_col_barplot:
                            if i1<=ii:
                                plt.barh(x[i], y[j])
                                plt.legend(loc='lower right')
                                plt.title(f"{i}x{j}")
                                i1 +=1
            else: # For Vertical BarPlot
                if ii > 1:
                    for i in self.x_col_barplot:
                        for j in self.y_col_barplot:
                            if i1<=ii:
                                plt.subplot(xl, yl, i1)
                                plt.bar(x[i], y[j])
                                plt.legend(loc='best')
                                plt.title(f"{i}x{j}")
                                plt.tight_layout()
                                i1 +=1
                else:
                    for i in self.x_col_barplot:
                        for j in self.y_col_barplot:
                            if i1<=ii:
                                plt.bar(x[i], y[j])
                                plt.legend(loc='upper right')
                                plt.title(f"{i}x{j}")
                                i1 +=1
            plt.show()
            return None
        gdf.plot(kind=plotname, stacked=stack, subplots=subplt)
        plt.show()

    def destroyed(self):
        self.x_col_barplot = []
        self.y_col_barplot = []
        self.x_axis_barplot_label.destroy()
        self.x_axis_barplot_label.destroy()
  
  # Scatter Plot
    def scatter_plot_selected(self):
        subplotvar = tk.BooleanVar(value=0)
        scatter_plot_window = tk.Toplevel()
        scatter_plot_window.geometry("720x460")
        colname = [x for x in self.df.columns]

        tk.Label(scatter_plot_window, text="Scatter Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(scatter_plot_window, text="Select X-axis variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(scatter_plot_window, values=colname)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(scatter_plot_window, text="Select Y-axis variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(scatter_plot_window, values=colname)
        ybar_combo_box.grid(row=4, column=0, padx=10)
        
        tk.Checkbutton(scatter_plot_window, text="Sub-Plot", variable=subplotvar, onvalue=1, offvalue=0).grid(row=5, column=0, padx=10, sticky='W')
        ttk.Button(scatter_plot_window, text="Plot", command=lambda : self.Plot_ScatterPlot(subplotvar.get())).grid(row=6, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(scatter_plot_window, text="Variables selected for X axis are :")
        self.y_axis_barplot_label = tk.Label(scatter_plot_window, text="Variables selected for Y axis are :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xybarplot(xbar_combo_box.get(), 0))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xybarplot(ybar_combo_box.get(), 1))
        
        scatter_plot_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_ScatterPlot(self, subplt):
        x = self.x_col_barplot
        y = self.y_col_barplot
        q = x+y
        xl = len(x)
        yl = len(y)
        i1 = 1
        gdf = self.df[q]
        colors = itertools.cycle(['r','g','b'])
        if subplt == True:
            for e in x:
                for r in y:
                    plt.subplot(xl, yl, i1)
                    plt.scatter(x=gdf[e], y=gdf[r], s=3.0, c=next(colors), label=r)
                    plt.legend(loc="upper right")
                    plt.xlabel(e)
                    plt.ylabel(r)
                    i1 += 1
        else:
            for e in x:
                for r in y:
                    plt.scatter(x=gdf[e], y=gdf[r], s=3.0, c=next(colors), label=r)
                    plt.legend(loc="upper right")
            plt.xlabel(x)
            plt.ylabel(y)
        plt.tight_layout()
        plt.show()

  # Area Plot
    def area_plot_selected(self):
        area_plot_window = tk.Toplevel()
        area_plot_window.geometry("720x460")
        colname = [x for x in self.df.columns]

        tk.Label(area_plot_window, text="Area Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(area_plot_window, text="Select X-axis variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(area_plot_window, values=colname)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(area_plot_window, text="Select Y-axis variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(area_plot_window, values=colname)
        ybar_combo_box.grid(row=4, column=0, padx=10)
        
        ttk.Button(area_plot_window, text="Plot", command=lambda : self.Plot_AreaPlot()).grid(row=5, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(area_plot_window, text="Variables selected for X axis are :")
        self.y_axis_barplot_label = tk.Label(area_plot_window, text="Variables selected for Y axis are :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xybarplot(xbar_combo_box.get(), 0))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xybarplot(ybar_combo_box.get(), 1))
        
        area_plot_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_AreaPlot(self):
        x = self.x_col_barplot
        y = self.y_col_barplot
        xl = len(x)
        i1 = 1
        if xl == 1:
            for x1 in x:
                gdf = self.df.groupby(by=x1)[y].sum()
                gdf = gdf.sort_values(by=x1).reset_index()
                li = []
                for y1 in y:
                    li.append(gdf[y1])
                plt.stackplot(gdf[x1], li, labels=y)
                plt.legend(loc="upper left")
            plt.tight_layout()
            plt.show()
            return None
        elif xl == 2:
            sp1 = 1
            sp2 = 2
        elif xl == 3:
            sp1 = 1
            sp2 = 3
        elif xl == 4:
            sp1 = 2
            sp2 =2
        elif xl == 5:
            sp1 = 2
            sp2 = 3
        elif xl == 6:
            sp1 = 2
            sp2 = 3
        else:
            print("Too Many Columns and Rows")
        for x1 in x:
            plt.subplot(sp1, sp2, i1)
            i1 +=1
            gdf = self.df.groupby(by=x1)[y].sum()
            gdf = gdf.sort_values(by=x1).reset_index()
            li = []
            for y1 in y:
                li.append(gdf[y1])
            plt.stackplot(gdf[x1], li, labels=y)
            plt.legend(loc="upper left")
        plt.tight_layout()
        plt.show()

  # Pie Plot
    def pie_plot_selected(self):
        pie_plot_window = tk.Toplevel()
        pie_plot_window.geometry("720x460")
        colname = [x for x in self.df.columns]

        tk.Label(pie_plot_window, text="Pie Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(pie_plot_window, text="Select Categorical Variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(pie_plot_window, values=colname)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(pie_plot_window, text="Select Relative Measure Variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(pie_plot_window, values=colname)
        ybar_combo_box.grid(row=4, column=0, padx=10)
        
        ttk.Button(pie_plot_window, text="Plot", command=lambda : self.Plot_PiePlot()).grid(row=5, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(pie_plot_window, text="Variables selected for X axis are :")
        self.y_axis_barplot_label = tk.Label(pie_plot_window, text="Variables selected for Y axis are :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.x_axis_barplot_label.config(text=f"Variables selected for X axis are :\n{xbar_combo_box.get()}"))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.y_axis_barplot_label.config(text=f"Variables selected for Y axis are :\n{ybar_combo_box.get()}"))
        
        pie_plot_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_PiePlot(self):
        x = self.x_col_barplot
        y = self.y_col_barplot
        x = x[-1]
        y = y[-1]
        gdf = self.df.groupby(by=x)[y].sum()
        gdf = gdf.reset_index()
        print(gdf)
        plt.pie(gdf[y], labels=gdf[x], autopct='%1.1f%%')
        plt.show()

  # Histogram Plot
    def lbl_xyhistplot(self, colname, indicator):
        if indicator==0:
            if colname not in self.x_col_barplot:
                self.x_col_barplot.append(str(colname))
            else:
                self.x_col_barplot.remove(colname)
            x = "Variables selected are :"
            ctr = 0
            for i in self.x_col_barplot:
                x = x + f"\n{i}"
            self.x_axis_barplot_label.configure(text=x)
        else:
            if colname not in self.y_col_barplot:
                self.y_col_barplot.append(str(colname))
            else:
                self.y_col_barplot.remove(colname)
            x = "Variables selected for Relative Measure are :"
            ctr = 0
            for i in self.y_col_barplot:
                x = x + f"\n{i}"
            self.y_axis_barplot_label.configure(text=x)

    def histogram_plot_selected(self):
        subplotvar = tk.BooleanVar(value=0)
        logfunc = tk.BooleanVar(value=0)
        histplot_window = tk.Toplevel()
        histplot_window.geometry("720x460")
        colname = [x for x in self.df.columns]
        tk.Label(histplot_window, text="Histogram Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(histplot_window, text="Select Variable/Column").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(histplot_window, values=colname)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Checkbutton(histplot_window, text="Sub-Plot", variable=subplotvar, onvalue=1, offvalue=0).grid(row=3, column=0, padx=10, sticky='W')
        tk.Checkbutton(histplot_window, text="Use Log Function", variable=logfunc, onvalue=1, offvalue=0).grid(row=4, column=0, padx=10, sticky='W')

        ttk.Button(histplot_window, text="Plot", command=lambda : self.Plot_HistPlot(subplt=subplotvar.get(), logfun=logfunc.get())).grid(row=5, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(histplot_window, text="Variables selected are :")
        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xyhistplot(xbar_combo_box.get(), 0))

        histplot_window.bind("<Destroy>", lambda e:self.destroyed())
        pass
    
    def Plot_HistPlot(self, subplt, logfun):
        x = self.x_col_barplot
        xl = len(x)
        if xl == 1:
            for x1 in x:
                u = len(self.df[x1].unique())+1
            plt.hist(x = self.df[x], bins=u, log=logfun, edgecolor="black", label=x)
            plt.legend(loc="upper right")
            plt.show()
            return None
        elif xl == 2:
            sp1 = 1
            sp2 = 2
        elif xl == 3:
            sp1 = 1
            sp2 = 3
        elif xl == 4:
            sp1 = 2
            sp2 =2
        elif xl == 5:
            sp1 = 2
            sp2 = 3
        elif xl == 6:
            sp1 = 2
            sp2 = 3
        elif xl == 0:
            showwarning("Warning", "Atleast Select One Variable For Histogram")
            return None
        
        if subplt == True:
            i1 = 1
            for x1 in x:
                plt.subplot(sp1, sp2, i1)
                i1 +=1
                u = len(self.df[x1].unique())+1
                plt.hist(x=self.df[x1], bins=u, log=logfun, edgecolor="black", label=x1)
                plt.legend(loc="upper right")
        else:
            for x1 in x:
                u = len(self.df[x1].unique())+1
                plt.hist(x=self.df[x1], bins=u, log=logfun, edgecolor="black", label=x1)
                plt.legend(loc="upper right")
        plt.tight_layout()
        plt.show()

  # Line Plot
    def line_plot_selected(self):
        lineplot_window = tk.Toplevel()
        lineplot_window.geometry("720x460")
        colname = [x for x in self.df.columns]
        tk.Label(lineplot_window, text="Line Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(lineplot_window, text="Select X-axis variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(lineplot_window, values=colname)
        tk.Label(lineplot_window, text="Select Y-axis variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(lineplot_window, values=colname)
        tk.Label(lineplot_window, text="Measure/Aggregate").grid(row=5,column=0, padx=10, pady=10, sticky='W')
        aggregate_type = ttk.Combobox(lineplot_window, values=['sum', 'mean', 'median', 'max', 'min','none'])
        aggregate_type.set('none')
        xbar_combo_box.grid(row=2, column=0, padx=10)
        ybar_combo_box.grid(row=4, column=0, padx=10)
        aggregate_type.grid(row=6, column=0, padx=10)

        ttk.Button(lineplot_window, text="Plot", command=lambda : self.Plot_LinePlot(agg=aggregate_type.get())).grid(row=10, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(lineplot_window, text="Variables selected for X axis are :")
        self.y_axis_barplot_label = tk.Label(lineplot_window, text="Variables selected for Y axis are :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xybarplot(xbar_combo_box.get(), 0))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xybarplot(ybar_combo_box.get(), 1))

        lineplot_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_LinePlot(self, agg):
        x = self.x_col_barplot
        y = self.y_col_barplot
        xl = len(x)
        
        if xl == 1:
            for x1 in x:
                if agg == 'sum':
                    gdf = self.df.groupby(by=x1)[y].sum()
                elif agg == 'mean':
                    gdf = self.df.groupby(by=x1)[y].mean()
                elif agg == 'median':
                    gdf = self.df.groupby(by=x1)[y].median()
                elif agg == 'max':
                    gdf = self.df.groupby(by=x1)[y].max()
                elif agg == 'min':
                    gdf = self.df.groupby(by=x1)[y].min()
                else:
                    z = x+y
                    gdf = self.df[z]
                gdf = gdf.sort_values(by=x1).reset_index()
                plt.plot(gdf[x1], gdf[y], label=y)
                plt.legend(loc="upper right")
            plt.show()
            return None
        elif xl == 2:
            sp1 = 1
            sp2 = 2
        elif xl == 3:
            sp1 = 1
            sp2 = 3
        elif xl == 4:
            sp1 = 2
            sp2 =2
        elif xl == 5:
            sp1 = 2
            sp2 = 3
        elif xl == 6:
            sp1 = 2
            sp2 = 3
        else:
            print("Too Many Columns and Rows")
        
        i1 = 1
        for x1 in x:
            plt.subplot(sp1, sp2, i1)
            i1 +=1
            if agg == 'sum':
                gdf = self.df.groupby(by=x1)[y].sum()
            elif agg == 'mean':
                gdf = self.df.groupby(by=x1)[y].mean()
            elif agg == 'median':
                gdf = self.df.groupby(by=x1)[y].median()
            elif agg == 'max':
                gdf = self.df.groupby(by=x1)[y].max()
            elif agg == 'min':
                gdf = self.df.groupby(by=x1)[y].min()
            else:
                z = x+y
                gdf = self.df[z]
            
            gdf = gdf.sort_values(by=x1).reset_index()
            plt.plot(gdf[x1], gdf[y], label=y)
            plt.legend(loc="upper right")
        plt.tight_layout()
        plt.show()







        pass

  # Box Plot 
    def box_plot_selected(self):
        subplotvar = tk.BooleanVar(value=0)
        boxplot_window = tk.Toplevel()
        boxplot_window.geometry("720x460")
        colname = [x for x in self.df.columns]
        tk.Label(boxplot_window, text="Box Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(boxplot_window, text="Select Variable/Column").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(boxplot_window, values=colname)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Checkbutton(boxplot_window, text="Sub-Plot", variable=subplotvar, onvalue=1, offvalue=0).grid(row=3, column=0, padx=10, sticky='W')

        ttk.Button(boxplot_window, text="Plot", command=lambda : self.Plot_BoxPlot(subplt=subplotvar.get())).grid(row=5, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(boxplot_window, text="Variables selected are :")
        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xyhistplot(xbar_combo_box.get(), 0))
        boxplot_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_BoxPlot(self, subplt):
        x = self.x_col_barplot
        xl = len(x)
        if xl == 1:
            gdf = self.df[x].dropna()
            plt.boxplot(gdf)
            plt.show()
            return None
        elif xl == 2:
            sp1 = 1
            sp2 = 2
        elif xl == 3:
            sp1 = 1
            sp2 = 3
        elif xl == 4:
            sp1 = 2
            sp2 =2
        elif xl == 5:
            sp1 = 2
            sp2 = 3
        elif xl == 6:
            sp1 = 2
            sp2 = 3
        elif xl == 0:
            showwarning("Warning", "Atleast Select One Variable For Histogram")
            return None
        
        if subplt == True:
            i1 = 1
            for x1 in x:
                plt.subplot(sp1, sp2, i1)
                i1 +=1
                gdf = self.df[x1].dropna()
                plt.boxplot(gdf)
                plt.xlabel(x1)
            plt.tight_layout()
        else:
            gdf = self.df[x].dropna()
            gdf.plot.box()
        
        plt.show()

  # Tree Map Plot
    def lbl_xytreemapplot(self, colname, indicator):
        if indicator==0:
            if colname not in self.x_col_barplot:
                if len(self.x_col_barplot) < 2:
                    self.x_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of TreeMap\nWe Suggest You Keep Variable Limit Upto 2 Only")
            else:
                self.x_col_barplot.remove(colname)
            x = "Variables Selected For TreeMap :"
            ctr = 0
            for i in self.x_col_barplot:
                x = x + f"\n{i}"
            self.x_axis_barplot_label.configure(text=x)
        
        else:
            if colname not in self.y_col_barplot:
                if len(self.y_col_barplot) < 2:
                    self.y_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of TreeMap\nWe Suggest You Keep Variable Limit Upto 2 Only")
            else:
                self.y_col_barplot.remove(colname)
            y = "Variables Selected For Relative Measures :"
            for i in self.y_col_barplot:
                y = y + f"\n{i}"
            self.y_axis_barplot_label.configure(text=y)

    def treemap_plot_selected(self):
        treemap_plot_window = tk.Toplevel()
        treemap_plot_window.geometry("720x460")
        colname = [x for x in self.df.columns]

        tk.Label(treemap_plot_window, text="Tree Map Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(treemap_plot_window, text="Select Variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(treemap_plot_window, values=colname)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(treemap_plot_window, text="Select Relational Variable\n(optional)").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(treemap_plot_window, values=colname)
        ybar_combo_box.grid(row=4, column=0, padx=10)
        
        ttk.Button(treemap_plot_window, text="Plot", command=lambda : self.Plot_TreeMapPlot()).grid(row=5, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(treemap_plot_window, text="Variables Selected For TreeMap :")
        self.y_axis_barplot_label = tk.Label(treemap_plot_window, text="Variables Selected For Relative Measures :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xytreemapplot(xbar_combo_box.get(), 0))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xytreemapplot(ybar_combo_box.get(), 1))   

        treemap_plot_window.bind("<Destroy>", lambda e:self.destroyed())

        pass

    def Plot_TreeMapPlot(self):
        x = self.x_col_barplot
        xl = len(x)
        if xl == 0:
            showwarning("Warning", "Please Select Atleast One Variable")
            return None
        y = self.y_col_barplot
        yl = len(y)
        if yl == 0:
            if xl == 1:
                gdf = self.df[x].value_counts()
                index1 = [x2 for x2 in gdf.index]
                values1 = [x for x in gdf.values]
                squarify.plot(sizes=values1, label=index1)
                plt.axis('off')
                plt.title(x[0])
                plt.show()
            else:
                i1 = 1
                for x1 in x:
                    plt.subplot(1,2,i1)
                    i1+=1
                    gdf = self.df[x1].value_counts()
                    index1 = [x2 for x2 in gdf.index]
                    values1 = [x for x in gdf.values]
                    squarify.plot(sizes=values1, label=index1)
                    plt.axis('off')
                    plt.title(x1)
                plt.show()
        
        elif yl == 1:
            if xl == 1:
                gdf = self.df.groupby(by=x)[y].sum()
                gdf = gdf.sort_values(by=y).reset_index()
                index1 = [x2 for x2 in gdf[x[0]]]
                values1 = [x for x in gdf[y[0]]]
                squarify.plot(sizes=values1, label=index1)
                plt.axis('off')
                plt.title(f"{x[0]} w.r.t {y[0]}")
                plt.show()
            else:
                i1 = 1
                for x1 in x:
                    plt.subplot(1,2,i1)
                    i1+=1
                    gdf = self.df.groupby(by=x1)[y].sum()
                    gdf = gdf.sort_values(by=y).reset_index()
                    index1 = [x2 for x2 in gdf[x1]]
                    values1 = [x for x in gdf[y[0]]]
                    squarify.plot(sizes=values1, label=index1)
                    plt.axis('off')
                    plt.title(f"{x1} w.r.t {y[0]}")
                plt.tight_layout()
                plt.show()

        elif yl == 2:
            if xl == 1:
                i1 = 1
                for y1 in y:
                    plt.subplot(1,2,i1)
                    i1+=1
                    gdf = self.df.groupby(by=x)[y1].sum()
                    gdf = gdf.reset_index()
                    print(gdf)
                    index1 = gdf[x[0]]
                    squarify.plot(sizes=gdf[y1], label=index1)
                    plt.axis('off')
                    plt.title(f"{x[0]} w.r.t {y1}")
                plt.tight_layout()
                plt.show()
            else:
                i1 = 1
                for x1 in x:
                    for y1 in y:
                        plt.subplot(2,2,i1)
                        i1+=1
                        gdf = self.df.groupby(by=x1)[y1].sum()
                        gdf = gdf.reset_index()
                        print(gdf)
                        squarify.plot(sizes=gdf[y1], label=gdf[x1])
                        plt.axis('off')
                        plt.title(f"{x1} w.r.t {y1}")
                plt.tight_layout()
                plt.show()
        
  # Heat Map Plot
    def heatmap_plot_selected(self):
        heat_plot_window = tk.Toplevel()
        heat_plot_window.geometry("720x460")
        colname = [x for x in self.df.columns]

        tk.Label(heat_plot_window, text="Heat Map Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(heat_plot_window, text="Select Categorical Variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(heat_plot_window, values=colname)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(heat_plot_window, text="Select Relative Measure Variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(heat_plot_window, values=colname)
        ybar_combo_box.grid(row=4, column=0, padx=10)
        
        ttk.Button(heat_plot_window, text="Plot", command=lambda : self.Plot_HeatMapPlot(x=xbar_combo_box.get(), y=ybar_combo_box.get())).grid(row=5, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(heat_plot_window, text="Variables selected for X axis are :")
        self.y_axis_barplot_label = tk.Label(heat_plot_window, text="Variables selected for Y axis are :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.x_axis_barplot_label.config(text=f"Variables selected for X axis are :\n{xbar_combo_box.get()}"))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.y_axis_barplot_label.config(text=f"Variables selected for Y axis are :\n{ybar_combo_box.get()}"))
        
        heat_plot_window.bind("<Destroy>", lambda e:self.destroyed())

        pass

    def Plot_HeatMapPlot(self, x, y):
        result = self.df.groupby(by=x)[y].value_counts().unstack()
        result = result.fillna(0)
        sns.heatmap(result)
        plt.show()

  # Donut Plot
    def lbl_xydonutmapplot(self, colname, indicator):
        if indicator==0:
            if colname not in self.x_col_barplot:
                if len(self.x_col_barplot) < 2:
                    self.x_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of Donut Plot\nWe Suggest You Keep Variable Limit Upto 2 Only")
            else:
                self.x_col_barplot.remove(colname)
            x = "Variables Selected For TreeMap :"
            ctr = 0
            for i in self.x_col_barplot:
                x = x + f"\n{i}"
            self.x_axis_barplot_label.configure(text=x)
        
        else:
            if colname not in self.y_col_barplot:
                if len(self.y_col_barplot) < 2:
                    self.y_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of Donut Plot\nWe Suggest You Keep Variable Limit Upto 2 Only")
            else:
                self.y_col_barplot.remove(colname)
            y = "Variables Selected For Relative Measures :"
            for i in self.y_col_barplot:
                y = y + f"\n{i}"
            self.y_axis_barplot_label.configure(text=y)

    def donut_plot_selected(self):
        heat_plot_window = tk.Toplevel()
        heat_plot_window.geometry("760x460")
        colname = [x for x in self.df.columns]

        tk.Label(heat_plot_window, text="Donut Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(heat_plot_window, text="Select Categorical Variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(heat_plot_window, values=colname)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(heat_plot_window, text="Select Relative Measure Variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(heat_plot_window, values=colname)
        ybar_combo_box.grid(row=4, column=0, padx=10)
        
        ttk.Button(heat_plot_window, text="Plot", command=lambda : self.Plot_DonutPlot()).grid(row=5, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(heat_plot_window, text="Variables selected are :")
        self.y_axis_barplot_label = tk.Label(heat_plot_window, text="Variables selected for Relative Measure are :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xydonutmapplot(xbar_combo_box.get(), 0))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xydonutmapplot(ybar_combo_box.get(), 1))
        
        heat_plot_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_DonutPlot(self):
        x = self.x_col_barplot
        xl = len(x)
        if xl == 0:
            showwarning("Warning", "Please Select Atleast One Variable")
            return None
        y = self.y_col_barplot
        yl = len(y)
        if yl == 0:
            if xl == 1:
                result = self.df[x].value_counts().reset_index()
                                
                ex = []
                for i in range(len(result[x[0]])):
                    if i%2==0:
                        ex.append(0)
                    else:
                        ex.append(0.05)
                        
                plt.pie(result[0], labels=result[x[0]], explode=ex, autopct='%1.1f%%', pctdistance=0.85)
                my_circle=plt.Circle( (0,0), 0.7, color='white')
                p=plt.gcf()
                p.gca().add_artist(my_circle)
                plt.show()
            else:
                i1 = 1
                for x1 in x:
                    plt.subplot(1,2,i1)
                    i1+=1
                    result = self.df[x1].value_counts().reset_index()
                    ex = []
                    for i in range(len(result[x1])):
                        if i%2==0:
                            ex.append(0)
                        else:
                            ex.append(0.05)
                            
                    plt.pie(result[x1], labels=result.index, explode=ex, autopct='%1.1f%%', pctdistance=0.85)

                    my_circle=plt.Circle( (0,0), 0.7, color='white')
                    p=plt.gcf()
                    p.gca().add_artist(my_circle)
                plt.tight_layout()
                plt.show()
        
        elif yl == 1:
            if xl == 1:
                gdf = self.df.groupby(by=x)[y].sum()
                gdf = gdf.sort_values(by=y).reset_index()
                ex = []
                for i in range(len(gdf[x[0]])):
                    if i%2==0:
                        ex.append(0)
                    else:
                        ex.append(0.05)
                        
                plt.pie(gdf[y[0]], labels=gdf[x[0]], explode=ex, autopct='%1.1f%%', pctdistance=0.85)
                my_circle=plt.Circle( (0,0), 0.7, color='white')
                p=plt.gcf()
                p.gca().add_artist(my_circle)
                plt.show()
            else:
                i1 = 1
                for x1 in x:
                    plt.subplot(1,2,i1)
                    i1+=1
                    gdf = self.df.groupby(by=x1)[y].sum()
                    gdf = gdf.sort_values(by=y).reset_index()
                    ex = []
                    for i in range(len(gdf[x1])):
                        if i%2==0:
                            ex.append(0)
                        else:
                            ex.append(0.05)
                            
                    plt.pie(gdf[y[0]], labels=gdf[x1], explode=ex, autopct='%1.1f%%', pctdistance=0.85)

                    my_circle=plt.Circle( (0,0), 0.7, color='white')
                    p=plt.gcf()
                    p.gca().add_artist(my_circle)
                plt.tight_layout()
                plt.show()
        
        elif yl == 2:
            if xl == 1:
                for x1 in x:
                    i1 = 1
                    for y1 in y:
                        plt.subplot(1,2,i1)
                        i1+=1
                        print(x1)
                        print(y1)
                        gdf = self.df.groupby(by=x1)[y1].sum()
                        gdf = gdf.reset_index()
                        ex = []
                        for i in range(len(gdf[x1])):
                            if i%2==0:
                                ex.append(0)
                            else:
                                ex.append(0.05)
                                
                        plt.pie(gdf[y1], labels=gdf[x1], explode=ex, autopct='%1.1f%%', pctdistance=0.85)

                        my_circle=plt.Circle( (0,0), 0.7, color='white')
                        p=plt.gcf()
                        p.gca().add_artist(my_circle)
                plt.tight_layout()
                plt.show()
            else:
                i1 = 1
                for x1 in x:
                    for y1 in y:
                        plt.subplot(2,2,i1)
                        i1+=1
                        gdf = self.df.groupby(by=x1)[y1].sum()
                        gdf = gdf.reset_index()
                        ex = []
                        for i in range(len(gdf[x1])):
                            if i%2==0:
                                ex.append(0)
                            else:
                                ex.append(0.05)
                                
                        plt.pie(gdf[y1], labels=gdf[x1], explode=ex, autopct='%1.1f%%', pctdistance=0.85)

                        my_circle=plt.Circle( (0,0), 0.7, color='white')
                        p=plt.gcf()
                        p.gca().add_artist(my_circle)
                plt.tight_layout()
                plt.show()
        
  # Lollipop Plot
    def lbl_xylollipopplot(self, colname, indicator):
        if indicator==0:
            if colname not in self.x_col_barplot:
                if len(self.x_col_barplot) < 3:
                    self.x_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of Lollipop\nWe Suggest You Keep Variable Limit Upto 3 Only")
            else:
                self.x_col_barplot.remove(colname)
            x = "Variables selected for X axis are :"
            ctr = 0
            for i in self.x_col_barplot:
                x = x + f"\n{i}"
            self.x_axis_barplot_label.configure(text=x)
        
        else:
            if colname not in self.y_col_barplot:
                if len(self.y_col_barplot) < 3:
                    self.y_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of Lollipop\nWe Suggest You Keep Variable Limit Upto 3 Only")
            else:
                self.y_col_barplot.remove(colname)
            y = "Variables selected for Y axis are :"
            for i in self.y_col_barplot:
                y = y + f"\n{i}"
            self.y_axis_barplot_label.configure(text=y)

    def lollipop_plot_selected(self):
        subplotvar = tk.BooleanVar(value=0)
        lollipopplot_window = tk.Toplevel()
        lollipopplot_window.geometry("720x460")
        colname = [x for x in self.df.columns]
        tk.Label(lollipopplot_window, text="Lollipop Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(lollipopplot_window, text="Select X-axis variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(lollipopplot_window, values=colname)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(lollipopplot_window, text="Select Y-axis variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(lollipopplot_window, values=colname)
        ybar_combo_box.grid(row=4, column=0, padx=10)

        tk.Checkbutton(lollipopplot_window, text="Sub-Plot", variable=subplotvar, onvalue=1, offvalue=0).grid(row=5, column=0, padx=10,sticky='W')
        ttk.Button(lollipopplot_window, text="Plot", command=lambda : self.Plot_LollipopPlot(subplt=subplotvar.get())).grid(row=6, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(lollipopplot_window, text="Variables selected for X axis are :")
        self.y_axis_barplot_label = tk.Label(lollipopplot_window, text="Variables selected for Y axis are :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xylollipopplot(xbar_combo_box.get(), 0))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xylollipopplot(ybar_combo_box.get(), 1))

        lollipopplot_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_LollipopPlot(self, subplt):
        print(subplt)
        x = self.x_col_barplot
        y = self.y_col_barplot
        xl = len(self.x_col_barplot)
        yl = len(self.y_col_barplot)
        if yl == 0:
            if xl == 1:
                gdf = self.df[x].value_counts().reset_index()
                print(gdf[x])
                plt.stem(gdf[x], gdf[0])
                plt.show()
            else:
                i1 = 1
                for x in self.x_col_barplot:
                    plt.subplot(1, xl, i1)
                    i1 +=1
                    gdf = self.df[x].value_counts().reset_index()
                    print(gdf[x])
                    plt.stem(gdf[x], gdf[0])
                plt.show()

        elif yl == 1:
            if xl == 1:
                gdf = self.df.groupby(by=x)[y].sum()
                plt.stem(gdf.index, gdf)
                plt.show()
            else:
                i1 = 1
                for i in x:
                    for j in y:
                        plt.subplot(1,xl,i1)
                        i1+=1
                        gdf = self.df.groupby(by=i)[j].sum()
                        plt.stem(gdf.index, gdf)
                plt.show()

        else:
            if xl == 1:
                i1 = 1
                for y1 in y:
                    plt.subplot(1,yl,i1)
                    i1+=1
                    gdf = self.df.groupby(by=x)[y].sum()
                    plt.stem(gdf.index, gdf)
                plt.show()
            else:
                i1 = 1
                for i in x:
                    for j in y:
                        plt.subplot(yl,xl,i1)
                        i1+=1
                        gdf = self.df.groupby(by=i)[j].sum()
                        plt.stem(gdf.index, gdf)
                plt.show()

  # Violin Plot
    def lbl_xyviolinplot(self, colname, indicator):
        if indicator==0:
            if colname not in self.x_col_barplot:
                if len(self.x_col_barplot) < 3:
                    self.x_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of Violin\nWe Suggest You Keep Variable Limit Upto 3 Only")
            else:
                self.x_col_barplot.remove(colname)
            x = "Selected Categorical Variable are :"
            ctr = 0
            for i in self.x_col_barplot:
                x = x + f"\n{i}"
            self.x_axis_barplot_label.configure(text=x)
        
        else:
            if colname not in self.y_col_barplot:
                if len(self.y_col_barplot) < 3:
                    self.y_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of Violin\nWe Suggest You Keep Variable Limit Upto 3 Only")
            else:
                self.y_col_barplot.remove(colname)
            y = "Selected Relative Measures Variable are"
            for i in self.y_col_barplot:
                y = y + f"\n{i}"
            self.y_axis_barplot_label.configure(text=y)

    def violin_plot_selected(self):
        subplotvar = tk.BooleanVar(value=0)
        violinplot_window = tk.Toplevel()
        violinplot_window.geometry("720x460")
        colname = [x for x in self.df.columns]
        tk.Label(violinplot_window, text="Violin Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(violinplot_window, text="Select Categorical variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(violinplot_window, values=colname)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(violinplot_window, text="Select Measure variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(violinplot_window, values=colname)
        ybar_combo_box.grid(row=4, column=0, padx=10)

        tk.Checkbutton(violinplot_window, text="Sub-Plot", variable=subplotvar, onvalue=1, offvalue=0).grid(row=5, column=0, padx=10,sticky='W')
        ttk.Button(violinplot_window, text="Plot", command=lambda : self.Plot_ViolinPlot(subplt=subplotvar.get())).grid(row=6, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(violinplot_window, text="Selected Categorical Variable are :")
        self.y_axis_barplot_label = tk.Label(violinplot_window, text="Selected Relative Measures Variable are")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xyviolinplot(xbar_combo_box.get(), 0))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xyviolinplot(ybar_combo_box.get(), 1))

        violinplot_window.bind("<Destroy>", lambda e:self.destroyed())


        pass

    def Plot_ViolinPlot(self, subplt):
        print(subplt)
        x = self.x_col_barplot
        xl = len(x)
        if xl == 0:
            showwarning("Warning", "Please Atleast Select One Categorical Variable")
        y = self.y_col_barplot
        yl = len(y)
        if yl == 0:
            if xl >1:
                ll = self.df[x].reset_index()
                i1 = 1
                for i in x:
                    plt.subplot(1, xl, i1)
                    i1 +=1
                    sns.violinplot(x=ll[i], y=ll['index'])
                plt.tight_layout()
                plt.show()
            else:
                ll = self.df[x].reset_index()
                for i in x:
                    sns.violinplot(x=ll[i], y=ll['index'])
                plt.tight_layout()
                plt.show()
        else:
            z = x+y
            ll = self.df[z]
            i1 = 1
            for i in x:
                for j in y:
                    plt.subplot(yl, xl, i1)
                    i1+=1
                    sns.violinplot(x=ll[i], y=ll[j])
            plt.show()

  # Density Plot
    def lbl_xydensityplot(self, colname, indicator):
        if indicator==0:
            if colname not in self.x_col_barplot:
                if len(self.x_col_barplot) < 3:
                    self.x_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of Density\nWe Suggest You Keep Variable Limit Upto 3 Only")
            else:
                self.x_col_barplot.remove(colname)
            x = "Selected Measures Variable are :"
            ctr = 0
            for i in self.x_col_barplot:
                x = x + f"\n{i}"
            self.x_axis_barplot_label.configure(text=x)
        
        else:
            if colname not in self.y_col_barplot:
                if len(self.y_col_barplot) < 3:
                    self.y_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of Density\nWe Suggest You Keep Variable Limit Upto 3 Only")
            else:
                self.y_col_barplot.remove(colname)
            y = "Selected Relative Measures Variable are"
            for i in self.y_col_barplot:
                y = y + f"\n{i}"
            self.y_axis_barplot_label.configure(text=y)
    
    def density_plot_selected(self):
        subplotvar = tk.BooleanVar(value=0)
        densityplot_window = tk.Toplevel()
        densityplot_window.geometry("720x460")
        colname = [x for x in self.df.columns]
        tk.Label(densityplot_window, text="Violin Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(densityplot_window, text="Select Measures variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(densityplot_window, values=colname)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(densityplot_window, text="Select Relative Measure\nvariable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(densityplot_window, values=colname)
        ybar_combo_box.grid(row=4, column=0, padx=10)

        tk.Checkbutton(densityplot_window, text="Use Shades", variable=subplotvar, onvalue=1, offvalue=0).grid(row=5, column=0, padx=10,sticky='W')
        ttk.Button(densityplot_window, text="Plot", command=lambda : self.Plot_DensityPlot(subplt=subplotvar.get())).grid(row=6, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(densityplot_window, text="Selected Measures Variable are :")
        self.y_axis_barplot_label = tk.Label(densityplot_window, text="Selected Relative Measures Variable are")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xydensityplot(xbar_combo_box.get(), 0))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xydensityplot(ybar_combo_box.get(), 1))

        densityplot_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_DensityPlot(self, subplt):
        x = self.x_col_barplot
        xl = len(x)
        if xl == 0:
            showwarning("Warning", "Please Atleast Select One Categorical Variable")
        y = self.y_col_barplot
        yl = len(y)
        if yl == 0:
            if xl >1:
                ll = self.df[x].reset_index()
                i1 = 1
                for i in x:
                    plt.subplot(1, xl, i1)
                    i1 +=1
                    sns.kdeplot(x=ll[i], y=ll['index'], cmap="Blues", shade=subplt)
                plt.tight_layout()
                plt.show()
            else:
                ll = self.df[x].reset_index()
                for i in x:
                    sns.kdeplot(x=ll[i], y=ll['index'], cmap="Blues", shade=subplt)
                plt.tight_layout()
                plt.show()
        else:
            z = x+y
            ll = self.df[z]
            i1 = 1
            for i in x:
                for j in y:
                    plt.subplot(yl, xl, i1)
                    i1+=1
                    sns.kdeplot(x=ll[i], y=ll[j], cmap="Blues", shade=subplt)
            plt.show()


        
        pass

  # Paire Wise Plot
    def lbl_xypairwiseplot(self, colname, indicator):
        if indicator==0:
            if colname not in self.x_col_barplot:
                if len(self.x_col_barplot) < 3:
                    self.x_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of Pair-Wise Plot\nWe Suggest You Keep Variable Limit Upto 3 Only")
            else:
                self.x_col_barplot.remove(colname)
            x = "Selected Measures Variable are : Selected Categorical Variable are"
            ctr = 0
            for i in self.x_col_barplot:
                x = x + f"\n{i}"
            self.x_axis_barplot_label.configure(text=x)

    def pairwise_plot_selected(self):
        subplotvar = tk.StringVar(value='hist')
        violinplot_window = tk.Toplevel()
        violinplot_window.geometry("720x460")
        z = [x for x in self.df.columns]
        tk.Label(violinplot_window, text="Pair Wise Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        mc = []
        cc = []
        for colname in z:
            dt = self.df[colname].dtype
            if (dt == np.int64) or (dt == np.float64):
                mc.append(colname)
            else:
                cc.append(colname)

        tk.Label(violinplot_window, text="Select Measures Variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(violinplot_window, values=mc)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(violinplot_window, text="Select Categorical Variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(violinplot_window, values=cc)
        ybar_combo_box.grid(row=4, column=0, padx=10)

        tk.Checkbutton(violinplot_window, text="hist/kde", variable=subplotvar, onvalue='hist', offvalue='kde').grid(row=5, column=0, padx=10,sticky='W')
        ttk.Button(violinplot_window, text="Plot", command=lambda : self.Plot_PairWisePlot(subplt=subplotvar.get(), y=ybar_combo_box.get())).grid(row=6, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(violinplot_window, text="Selected Measures Variable are :")
        self.y_axis_barplot_label = tk.Label(violinplot_window, text="Selected Categorical Variable is")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=4, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xypairwiseplot(xbar_combo_box.get(), 0))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.y_axis_barplot_label.config(text=f"Selected Categorical Variable is\n{ybar_combo_box.get()}"))

        violinplot_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_PairWisePlot(self, subplt, y):
        if len(y) == 0:
            x = self.x_col_barplot
            gdf = self.df[x]
            pairplot_var = sns.pairplot(data=gdf, diag_kind=subplt, dropna=True)
            #pairplot_var.map(plt.bar/plt.scatter) <- to add bar or scatter plot to the diagonal subplots of pairplot
            plt.show()
        else:
            print(y)
            x = self.x_col_barplot
            y1 = x+[y]
            gdf = self.df[y1]
            pairplot_var = sns.pairplot(data=gdf, hue=y, diag_kind=subplt, dropna=True)
            #pairplot_var.map(plt.bar/plt.scatter) <- to add bar or scatter plot to the diagonal subplots of pairplot
            plt.show()
        """
        for more references about PairPlot goto this link :
            https://seaborn.pydata.org/generated/seaborn.pairplot.html
        """
  
  # WaterFall Plot
    def waterfall_plot_selected(self):
        waterfall_window = tk.Toplevel()
        waterfall_window.geometry("720x460")
        colname = [x for x in self.df.columns]
        tk.Label(waterfall_window, text="WaterFall Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        tk.Label(waterfall_window, text="Select X-axis variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(waterfall_window, values=colname)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(waterfall_window, text="Select Y-axis variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(waterfall_window, values=colname)
        ybar_combo_box.grid(row=4, column=0, padx=10)

        ttk.Button(waterfall_window, text="Plot", command=lambda : self.Plot_WaterFallPlot(x=xbar_combo_box.get(), y=ybar_combo_box.get())).grid(row=5, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(waterfall_window, text="Variables selected for X axis is :")
        self.y_axis_barplot_label = tk.Label(waterfall_window, text="Variables selected for Y axis is :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.x_axis_barplot_label.config(text=f"Variables selected for X axis are :\n{xbar_combo_box.get()}"))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.y_axis_barplot_label.config(text=f"Variables selected for Y axis are :\n{ybar_combo_box.get()}"))

        waterfall_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_WaterFallPlot(self, x, y):
        xl = len(x)
        if xl == 0:
            showwarning("Warning", "Please Atleast Select One Variable in X-Axis")
        yl = len(y)
        if yl == 0: 
            gdf = self.df[x].value_counts().reset_index()
            gdf = gdf.sort_values(by='index')
            for i in range(1, len(gdf['index'])):
                if gdf.iloc[i, 1] < gdf.iloc[(i-1), 1]:
                    gdf.iloc[i, 1] = -(gdf.iloc[i, 1])
                    print(gdf.iloc[i, 1])
            waterfall_chart.plot(gdf['index'], gdf[x])
            plt.show()
        else:
            z = [x]+[y]
            gdf = self.df[z]
            gdf = gdf.sort_values(by=x).reset_index(drop=True)
            for i in range(1, len(gdf[y])):
                if gdf.iloc[i, 1] < gdf.iloc[(i-1), 1]:
                    gdf.iloc[i, 1] = -(gdf.iloc[i, 1])
                    print(gdf.iloc[i, 1])
            waterfall_chart.plot(gdf[x], gdf[y])
            plt.show()
        pass

  # Cross Correlation Plot
    def lbl_xycrosscorrmapplot(self, colname, indicator):
        if indicator==0:
            if colname not in self.x_col_barplot:
                if len(self.x_col_barplot) < 3:
                    self.x_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of Cross Correlation\nWe Suggest You Keep Variable Limit Upto 3 Only")
            else:
                self.x_col_barplot.remove(colname)
            x = "Variables selected for X axis is :"
            ctr = 0
            for i in self.x_col_barplot:
                x = x + f"\n{i}"
            self.x_axis_barplot_label.configure(text=x)
        
        else:
            if colname not in self.y_col_barplot:
                if len(self.y_col_barplot) < 3:
                    self.y_col_barplot.append(str(colname))
                else:
                    showwarning("Info", "For Better Performance Of Cross Correlation\nWe Suggest You Keep Variable Limit Upto 3 Only")
            else:
                self.y_col_barplot.remove(colname)
            y = "Variables selected for Y axis is :"
            for i in self.y_col_barplot:
                y = y + f"\n{i}"
            self.y_axis_barplot_label.configure(text=y)

    def crosscorr_plot_selected(self):
        crosscorr_window = tk.Toplevel()
        crosscorr_window.geometry("720x460")
        colname1 = [x for x in self.df.columns]
        tk.Label(crosscorr_window, text="Cross Correlation Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')


        mc = []
        for colname in colname1:
            dt = self.df[colname].dtype
            if (dt == np.int64) or (dt == np.float64):
                mc.append(colname)

        tk.Label(crosscorr_window, text="Select X-axis variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(crosscorr_window, values=mc)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(crosscorr_window, text="Select Y-axis variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(crosscorr_window, values=mc)
        ybar_combo_box.grid(row=4, column=0, padx=10)

        ttk.Button(crosscorr_window, text="Plot", command=lambda : self.Plot_CrossCorrelationPlot()).grid(row=5, column=0, pady=10, padx=10,sticky='W')
        
        self.x_axis_barplot_label = tk.Label(crosscorr_window, text="Variables selected for X axis is :")
        self.y_axis_barplot_label = tk.Label(crosscorr_window, text="Variables selected for Y axis is :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xycrosscorrmapplot(xbar_combo_box.get(), 0))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.lbl_xycrosscorrmapplot(ybar_combo_box.get(), 1))   

        crosscorr_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_CrossCorrelationPlot(self):
        x = self.x_col_barplot
        y = self.y_col_barplot
        xl , yl = len(x), len(y)
        if yl ==0:
            showwarning("Warning", "Atleast Select One Variable for Y-Axis")
        elif xl ==0:
            showwarning("Warning", "Atleast Select One Variable for X-Axis")
        else:
            i1 = 1
            for i in x:
                for j in y:
                    plt.subplot(yl, xl, i1)
                    i1 += 1
                    z = [i]+[j]
                    z = self.df[z].dropna().reset_index(drop=True)
                    cross_corre = stattools.ccf(z[i], z[j])
                    nlags = len(cross_corre)
                    plt.hlines(0, xmin=-2, xmax=nlags, color='black')
                    plt.bar(x=np.arange(nlags), height=cross_corre, width=.3)
                    plt.xlim(-2,nlags)
            plt.show()

 #  3d Scatter plot

    def _3d_Scaterplot_selected(self):
        ThreeD_scater_window = tk.Toplevel()
        ThreeD_scater_window.geometry("720x460")
        colname1 = [x for x in self.df.columns]  
        tk.Label(ThreeD_scater_window, text="3D Scatter Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        val_3d = []
        for colname in colname1:
            dt = self.df[colname].dtype
            if (dt == np.int64) or (dt == np.float64):
                val_3d.append(colname)


        tk.Label(ThreeD_scater_window, text="Select X-axis variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(ThreeD_scater_window, values=val_3d)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(ThreeD_scater_window, text="Select Y-axis variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(ThreeD_scater_window, values=val_3d)
        ybar_combo_box.grid(row=4, column=0, padx=10)

        tk.Label(ThreeD_scater_window, text="Select Z-axis variable").grid(row=5,column=0, padx=10, pady=10, sticky='W')
        zbar_combo_box = ttk.Combobox(ThreeD_scater_window, values=val_3d)
        zbar_combo_box.grid(row=6, column=0, padx=10)

        ttk.Button(ThreeD_scater_window, text="Plot", command=lambda : self.Plot_3d_Scaterplot(x1 = xbar_combo_box.get(),y1=ybar_combo_box.get(),z1=zbar_combo_box.get())).grid(row=7, column=0, pady=10, padx=10,sticky='W')

        self.x_axis_barplot_label = tk.Label(ThreeD_scater_window, text="Variables selected for X axis is :")
        self.y_axis_barplot_label = tk.Label(ThreeD_scater_window, text="Variables selected for Y axis is :")
        self.z_axis_barplot_label = tk.Label(ThreeD_scater_window, text="Variables selected for Z axis is :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)
        self.z_axis_barplot_label.grid(row=1, column=3, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.x_axis_barplot_label.config(text=f"Variables selected for X axis are :\n{xbar_combo_box.get()}"))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.y_axis_barplot_label.config(text=f"Variables selected for Y axis are :\n{ybar_combo_box.get()}"))
        zbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.z_axis_barplot_label.config(text=f"Variables selected for Z axis are :\n{zbar_combo_box.get()}"))

        ThreeD_scater_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_3d_Scaterplot(self, x1, y1, z1):
        x = self.df[x1]
        y = self.df[y1]
        z = self.df[z1]

        print(x)
        print(y)
        print(z)

        fig_ThreeDimensional = plt.figure()
        ax = fig_ThreeDimensional.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c='skyblue', s=60)
        ax.view_init(30, 185)
        ax.set_xlabel(f"{x1}")
        ax.set_ylabel(f"{y1}")
        ax.set_zlabel(f"{z1}")

        plt.show()

        pass
 #  Surface plot

    def _3d_SurfacePlot_selected(self):
        ThreeD_SurfacePlot_window = tk.Toplevel()
        ThreeD_SurfacePlot_window.geometry("720x460")
        colname1 = [x for x in self.df.columns]  
        tk.Label(ThreeD_SurfacePlot_window, text="3D Scatter Plot").grid(row=0,column=0, padx=10, pady=10, sticky='W')

        val_3d = []
        for colname in colname1:
            dt = self.df[colname].dtype
            if (dt == np.int64) or (dt == np.float64):
                val_3d.append(colname)


        tk.Label(ThreeD_SurfacePlot_window, text="Select X-axis variable").grid(row=1,column=0, padx=10, pady=10, sticky='W')
        xbar_combo_box = ttk.Combobox(ThreeD_SurfacePlot_window, values=val_3d)
        xbar_combo_box.grid(row=2, column=0, padx=10)

        tk.Label(ThreeD_SurfacePlot_window, text="Select Y-axis variable").grid(row=3,column=0, padx=10, pady=10, sticky='W')
        ybar_combo_box = ttk.Combobox(ThreeD_SurfacePlot_window, values=val_3d)
        ybar_combo_box.grid(row=4, column=0, padx=10)

        ttk.Button(ThreeD_SurfacePlot_window, text="Plot", command=lambda : self.Plot_3d_Surfaceplot(x1 = xbar_combo_box.get(),y1=ybar_combo_box.get())).grid(row=7, column=0, pady=10, padx=10,sticky='W')

        self.x_axis_barplot_label = tk.Label(ThreeD_SurfacePlot_window, text="Variables selected for X axis is :")
        self.y_axis_barplot_label = tk.Label(ThreeD_SurfacePlot_window, text="Variables selected for Y axis is :")

        self.x_axis_barplot_label.grid(row=1, column=1, rowspan=5, sticky='N')
        self.y_axis_barplot_label.grid(row=1, column=2, rowspan=5, sticky='N', padx=10)

        xbar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.x_axis_barplot_label.config(text=f"Variables selected for X axis are :\n{xbar_combo_box.get()}"))
        ybar_combo_box.bind("<<ComboboxSelected>>", lambda e: self.y_axis_barplot_label.config(text=f"Variables selected for Y axis are :\n{ybar_combo_box.get()}"))
        
        ThreeD_SurfacePlot_window.bind("<Destroy>", lambda e:self.destroyed())

    def Plot_3d_Surfaceplot(self,x1,y1):
        x = self.df[x1]
        y = self.df[y1]
        z = (np.sin(x **2) + np.cos(y **2) )
        fig_SurfacePlt = plt.figure()
        ax = fig_SurfacePlt.add_subplot(111, projection='3d')
        surf = ax.plot_trisurf(x,y, z,cmap='plasma')
        ax.set_xlabel(f"{x1}")
        ax.set_ylabel(f"{y1}")

        plt.show()
        

 # Frame 3 Functionality Which Includes (Linear and Logistic Regression)
  # Linear Regression 
    def lr_lbl_Independent_Dependent(self, colname, indicator):
        if indicator==0:
            if colname not in self.x_col_barplot:
                self.x_col_barplot.append(str(colname))
            else:
                self.x_col_barplot.remove(colname)
            x = "Independent Variable :"
            ctr = 0
            for i in self.x_col_barplot:
                x = x + f"\n{i}"
            self.Independent_lbl.configure(text=x)
        else:
            if colname not in self.y_col_barplot:
                if len(self.y_col_barplot) == 1:
                    self.y_col_barplot[0] = str(colname)
                else:
                    self.y_col_barplot.append(str(colname))
            else:
                self.y_col_barplot.remove(colname)
            y = "Dependent Variable :"
            for i in self.y_col_barplot:
                y = y + f"\n{i}"
            self.Dependent_lbl.configure(text=y)  

    def LinearRegression_Window(self):#Complete
        self.PropertiesMachineLearningAlgorithm_Frame.config(text="Linear Regression")
        self.LR_IndependentVariable_lbl = tk.Label(self.PropertiesMachineLearningAlgorithm_Frame, text="Select Independent Variabel")
        self.LR_IndependentVariable_lbl.grid(row=0, column=0, padx=10, pady=10)
        self.LR_DependentVariable_lbl = tk.Label(self.PropertiesMachineLearningAlgorithm_Frame, text="Select Dependent Variabel")
        self.LR_DependentVariable_lbl.grid(row=0, column=1, pady=10)
        self.LR_TrainingDataset_lbl = tk.Label(self.PropertiesMachineLearningAlgorithm_Frame, text="Enter Training Dataset Value in Range of 1-99")
        self.LR_TrainingDataset_lbl.grid(row=0, column=2, padx=10, pady=10)
        
        c = [x for x in self.df.columns]
        self.column_of_independent_var = ttk.Combobox(self.PropertiesMachineLearningAlgorithm_Frame, values=c, state='readonly')
        self.column_of_dependent_var = ttk.Combobox(self.PropertiesMachineLearningAlgorithm_Frame, values=c, state='readonly')
        self.column_of_independent_var.grid(row=1, column=0)
        self.column_of_dependent_var.grid(row=1, column=1)

        self.train_percentage_linearReg_entry = tk.Entry(self.PropertiesMachineLearningAlgorithm_Frame, textvariable=self.train_percentage)
        self.train_percentage_linearReg_entry.grid(row=1, column=2, sticky="W", padx=15)

        self.submit_ml_btn = ttk.Button(self.PropertiesMachineLearningAlgorithm_Frame, text='Submit', command=self.LinearRegression_Algo)
        self.submit_ml_btn.grid(row=2, column=0, padx=10, pady=10)

        self.Independent_lbl = tk.Label(self.PropertiesMachineLearningAlgorithm_Frame, text="Independent Variable :")
        self.Independent_lbl.grid(row=3, column=0, padx=10, sticky="N")

        self.Dependent_lbl = tk.Label(self.PropertiesMachineLearningAlgorithm_Frame, text="Dependent Variable :")
        self.Dependent_lbl.grid(row=3, column=1, padx=10, sticky="N")
        
        self.column_of_independent_var.bind("<<ComboboxSelected>>", lambda e: self.lr_lbl_Independent_Dependent(self.column_of_independent_var.get(), 0))
        self.column_of_dependent_var.bind("<<ComboboxSelected>>", lambda e: self.lr_lbl_Independent_Dependent(self.column_of_dependent_var.get(), 1))
        
        self.Linear_Regression_Score_Lable = tk.Label(self.PropertiesMachineLearningAlgorithm_Frame, text="Evaluation")
        self.Linear_Regression_Score_Lable.grid(row=4, column=0, padx=10, pady=20, columnspan=2, rowspan=1)

        pass

    def LinearRegression_Algo(self):
        print(f"Linear Regression Algo :\n{self.train_percentage.get()}")
        print(self.x_col_barplot)
        print(self.y_col_barplot)
        dep = self.y_col_barplot[0]
        Indep = self.x_col_barplot[0]

        # Fetching Independ Variable Data
        x1 = self.df[Indep]
        # Fetching Depend Variable Data 
        y1 = self.df[dep]

        # Filling The Nan Values By Forward Fill Method
        x1.fillna(method ='ffill', inplace = True)
        y1.fillna(method ='ffill', inplace = True)
        
        plt.scatter(x1,y1)
        plt.show()

        # Here We Are Handling The Categorical Data If Is Present by Using One Hot Encoding
        #x1 = pd.get_dummies(data=x1, drop_first=True)

        # Training Size of Data
        training_value_of_data = self.train_percentage.get()
        self.train_percentage.set(0)
        training_value_of_data = 100 - training_value_of_data
        training_value_of_data *= 0.01

        # Spliting The Data of x1 & y1 by given training size and randomizing it by state of 101(you can give any number does't affect much).
        X_train, X_test, y_train, y_test = train_test_split(x1, y1, test_size=training_value_of_data, random_state=101)
        
        # Optional Print Stmts
                
        print(X_train.shape) 
        print(X_test.shape)
        print(y_train.shape)
        print(y_test.shape)

        # Creating Object / Instance of Class -> LinearRegression
        regr = LinearRegression()

        # Training the Regression Model on X_train & y_train data
        regr.fit(X_train.values.reshape(-1,1), y_train)
        p = regr.predict(X_test.values.reshape(-1,1))
        print("P = ", p)
        # Calculating the Score / Accuracy of Regression Model Based on Training of X_train & y_train data
        reg_score_var = regr.score(X_test.values.reshape(-1,1), y_test)

        # Showing The Output in Lable
        self.Linear_Regression_Score_Lable.config(text=f"Percentage of Training : {1.0 - training_value_of_data} \nPercentage of Test : {training_value_of_data} \nScore : {reg_score_var}")
        

        pass

if __name__ == '__main__':
    app = App()
    app.mainloop()
