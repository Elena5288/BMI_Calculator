import tkinter
import csv
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window=tkinter.Tk()
window.title("BMI Calculator")
window.config(bg="#b88c8c")
window.geometry("400x800")
frame=tkinter.Frame(window)
frame.pack()

#Variables
button_on=True
bmi_value=0
name=""
height=0.0
weight=0.0
category=""
last_saved_category=None

# Images for the switch button
metric=PhotoImage(file=r"C:\Users\elena\PycharmProjects\Projct_BMI_calculator\on.png")
imperial=PhotoImage(file=r"C:\Users\elena\PycharmProjects\Projct_BMI_calculator\off.png")

#Define switch function
def switch():
    global button_on
    if button_on:
        units_button.config(image=imperial)
        user_height_unit_label.config(text="in")
        user_weight_unit_label.config(text="lb")
        button_on=False
    else:
        units_button.config(image=metric)
        user_height_unit_label.config(text="cm")
        user_weight_unit_label.config(text="kg")
        button_on=True

# Calculates the BMI value
def calculate():
    global name, height, weight, bmi_value, category, button_on
    name=user_name_txt.get()
    try:
        height=float(user_height_txt.get())
        weight=float(user_weight_txt.get())
    except ValueError:
        tkinter.messagebox.showwarning(title="Error!", message="Please enter valid numerical values for Height and Weight.")
        return
    if button_on:
        height=height/100
        bmi_value=weight / (height*height)
        print(bmi_value)
    else:
        bmi_value=703 * weight / (height * height)
        print(bmi_value)
    if bmi_value<18.5:
        category="Underweight"
    elif bmi_value<25:
        category="Normal weight"
    elif bmi_value<30:
        category="Overweight"
    else:
        category="Obese"

    if category=="Underweight":
        result_font_color="#266ef0"
    elif category=="Normal weight":
        result_font_color="#388638"
    elif category=="Overweight":
        result_font_color="#9a7300"
    else:
        result_font_color="#ff1a1a"

    user_name_label.config(text=f"\tName: {name}", fg=result_font_color)
    bmi_result_label.config(text=f"\tBMI value: {bmi_value:.2f}", fg=result_font_color)
    category_label.config(text=f"\tBMI category: {category}", fg=result_font_color)

# Save info to csv file
def save():
    global last_saved_category
    with open("BMI_records.csv", "a") as bmi_info:
        content = csv.writer(bmi_info)
        content.writerow([name, height, weight, bmi_value, category])

    last_saved_category=category
    tkinter.messagebox.showwarning(title="Saved", message="Your info has been saved!")

    # Reset input fields
    user_name_txt.delete(0, "end")
    user_height_txt.delete(0, "end")
    user_weight_txt.delete(0, "end")

category_counts = {"Underweight":0, "Normal weight":0, "Overweight":0, "Obese":0}

def update_category_count(category):
    category_counts[category]+=1

def display_category_counts():
    for category, count in category_counts.items():
        print(f"{category}: {count}")

# Read CSV file
with open("BMI_records.csv", "r") as readfile:
    csvread = csv.reader(readfile)
    data_rows = list(csvread)

# Display category counts after reading the CSV file
if not data_rows:
    print("CSV file is empty")
else:
    for row in data_rows:
        if len(row) >= 5:  # Check if row has at least 5 elements
            update_category_count(row[4])
        else:
            continue

color_code=["#266ef0", "#388638", "#e6ac00", "#ff1a1a"]
label_code=category_counts.keys()

#Pie chart
def pie_chart():
    global last_saved_category
    # Clear existing pie chart
    for widget in bmi_chart_frame.winfo_children():
        widget.destroy()

    fig, ax1 = plt.subplots(figsize=(3, 3), facecolor="#aec8ce")
    if last_saved_category is None:
        explode = [0] * len(category_counts)
    else:
        explode = [0.2 if cat == last_saved_category else 0 for cat in category_counts.keys()]

    wedges, labels, pcts=ax1.pie(category_counts.values(), labels=label_code, autopct="%1.1f%%", startangle=110,
                                 colors=color_code, textprops={"fontsize":7},
                                 wedgeprops={"linewidth":2.0, "edgecolor":"white"}, explode=explode)
    ax1.axis("equal")
    plt.title(f"BMI Chart and {name}'s placement", color="#3b5b62", fontsize=10)
    plt.setp(pcts, color="#fff")
    plt.setp(labels, fontweight=700)
    plt.tight_layout()
    for i, wedge in enumerate(wedges):
        if explode[i]==0:
            labels[i].set_color(wedge.get_facecolor())
        else:
            labels[i].set_color("#fff")

    # Embed the plot in tkinter
    canvas=FigureCanvasTkAgg(fig, master=bmi_chart_frame)
    canvas_widget=canvas.get_tk_widget()
    canvas_widget.pack()


def initial_pie_chart():
    global last_saved_category
    fig, ax1 = plt.subplots(figsize=(3, 3), facecolor="#aec8ce")

    if last_saved_category is None:
        explode = [0] * len(category_counts)
    else:
        explode = [0.2 if cat == last_saved_category else 0 for cat in category_counts.keys()]

    wedges, labels, pcts = ax1.pie(category_counts.values(), labels=label_code, autopct="%1.1f%%", startangle=110,
                                   colors=color_code, textprops={"fontsize": 7},
                                   wedgeprops={"linewidth": 2.0, "edgecolor": "white"}, explode=explode)
    ax1.axis("equal")
    plt.title("BMI Distribution", color="#3b5b62")
    plt.setp(pcts, color="#fff")
    plt.setp(labels, fontweight=700)
    plt.tight_layout()

    for i, wedge in enumerate(wedges):
        if explode[i] == 0:
            labels[i].set_color(wedge.get_facecolor())
        else:
            labels[i].set_color("white")

    # Embed the plot in tkinter
    canvas = FigureCanvasTkAgg(fig, master=bmi_chart_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

# Display category counts after reading the CSV file
if not data_rows:
    print("CSV file is empty")
else:
    for row in data_rows:
        if len(row) >= 5:
            update_category_count(row[4])
        else:
            continue

# Frame BMI Input & Calculator
bmi_info=tkinter.LabelFrame(frame, text="BMI Calculator", border=5, background="#aec8ce", font=10, fg="#3b5b62")
bmi_info.grid(row=0, column=0, sticky="news")
bmi_info.columnconfigure(0, weight=1)

# Switch button
imperial_units_button_label = tkinter.Label(bmi_info, text="Imperial", fg="#3b5b62", background="#aec8ce")
imperial_units_button_label.grid(row=0, column=0, padx=5, pady=5)
metrics_units_button_label = tkinter.Label(bmi_info, text="Metric", fg="#3b5b62", background="#aec8ce")
metrics_units_button_label.grid(row=0, column=2, padx=20, pady=5)
units_button= Button(bmi_info, image=metric, bd=0, bg="#aec8ce", activebackground="#aec8ce", command=switch)
units_button.grid(row=0, column=1, padx=5, pady=5)

# Name label & text
user_name_label=tkinter.Label(bmi_info, text="\tName", fg="#3b5b62", background="#aec8ce")
user_name_label.grid(row=1, column=0, pady=5, sticky="w")
user_name_txt=tkinter.Entry(bmi_info)
user_name_txt.grid(row=1, column=1, pady=5)

# Height label & text
user_height_label=tkinter.Label(bmi_info, text="\tHeight", fg="#3b5b62", background="#aec8ce")
user_height_label.grid(row=2, column=0, pady=5, sticky="w")
user_height_txt=tkinter.Entry(bmi_info)
user_height_txt.grid(row=2, column=1, pady=5)
user_height_unit_label=tkinter.Label(bmi_info, text="cm", fg="#3b5b62", background="#aec8ce")
user_height_unit_label.grid(row=2, column=2, pady=5)

# Weight label & text
user_weight_label=tkinter.Label(bmi_info, text="\tWeight", fg="#3b5b62", background="#aec8ce")
user_weight_label.grid(row=3, column=0, pady=5, sticky="w")
user_weight_txt=tkinter.Entry(bmi_info)
user_weight_txt.grid(row=3, column=1, pady=5)
user_weight_unit_label=tkinter.Label(bmi_info, text="kg", fg="#3b5b62", background="#aec8ce")
user_weight_unit_label.grid(row=3, column=2, pady=5)

calculate_button=tkinter.Button(bmi_info, text="Calculate", command=calculate, bg="#d6c7c7", fg="#6e5656")
calculate_button.grid(row=4, column=0, pady=10, sticky="nsew", columnspan=3)

# Frame BMI Result
results_frame=tkinter.LabelFrame(frame, text="BMI Results", border=5, background="#aec8ce", font=10, fg="#3b5b62")
results_frame.grid(row=1, column=0, sticky="nsew")
results_frame.columnconfigure(0, weight=1)

user_name_label=tkinter.Label(results_frame, text="\tName: ", fg="#3b5b62", background="#aec8ce")
user_name_label.grid(row=0, column=0, pady=5, sticky="w")
bmi_result_label=tkinter.Label(results_frame, text="\tBMI value: ", fg="#3b5b62", background="#aec8ce")
bmi_result_label.grid(row=1, column=0, pady=5, sticky="w")
category_label=tkinter.Label(results_frame, text="\tBMI category: ", fg="#3b5b62", background="#aec8ce")
category_label.grid(row=2, column=0, pady=5, sticky="w")

save_button=tkinter.Button(results_frame, text="Save", command=save, bg="#d6c7c7", fg="#6e5656", width=37)
save_button.grid(row=3, column=0, pady=10, sticky="nsew")

# Frame BMI Chart
bmi_chart_frame=tkinter.LabelFrame(frame, text="BMI Chart", border=5, background="#aec8ce", font=10, fg="#3b5b62")
bmi_chart_frame.grid(row=2, column=0, sticky="nsew")
bmi_chart_frame.columnconfigure(0, weight=1)

pie_chart_button=tkinter.Button(bmi_chart_frame, text="See your chart placement", command=pie_chart, bg="#d6c7c7", fg="#6e5656", width=42)
pie_chart_button.pack(pady=10)

# Generate and display the initial pie chart
initial_pie_chart()

display_category_counts()

window.mainloop()
