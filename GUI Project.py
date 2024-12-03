import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import csv

class TimetableApp():

    def __init__(self, root):
        self.root = root
        self.root.title("Timetable Tool")

        #data path
        self.data_path = "C:\\Users\\PC\\Desktop\\sampledata.csv"

        # GUI elements
        self.create_widgets()

    def create_widgets(self):
        # File Path Entry
        self.file_path_label = Label(self.root, text="Data path:", bg="black", fg="white")
        self.file_path_label.grid(row=0, column=0, padx=(5, 10), pady=(20, 0), sticky=W)
        self.file_path_entry = Entry(self.root)
        self.file_path_entry.insert(END, self.data_path)  # Set default data path
        self.file_path_entry.grid(row=0, column=1, columnspan=2, padx=(0, 10), pady=(20, 0), sticky=W + E)
        self.browse_button = Button(self.root, text="Browse", bg="grey", fg="white", command=self.browse_file)
        self.browse_button.grid(row=0, column=3, padx=(0, 10), pady=(20, 0))

        # Year Selection
        self.year_label = Label(self.root, text="Year", bg="black", fg="white")
        self.year_label.grid(row=1, column=0, padx=(5, 10), pady=(20, 0), sticky=W)
        self.year_var = tk.StringVar()
        self.year_combobox = ttk.Combobox(self.root, width=5, textvariable=self.year_var)
        self.year_combobox['values'] = ('1', '2', '3', '4', '5', '')
        self.year_combobox.grid(row=1, column=1, padx=(5, 10), pady=(20, 0), sticky=W + E)

        # Department Entry
        self.department_label = Label(self.root, text="Department", bg="black", fg="white")
        self.department_label.grid(row=1, column=2, padx=(5, 10), pady=(20, 0), sticky=W)
        self.department_entry = Entry(self.root)
        self.department_entry.grid(row=1, column=3, padx=(5, 10), pady=(20, 0), sticky=W)

        # Buttons
        self.display_button = Button(self.root, text="Display", bg="green", fg="white", command=self.display_timetable)
        self.display_button.grid(row=2, column=0, padx=(5, 10), pady=(20, 0), sticky=W + E)
        self.clear_button = Button(self.root, text="Clear", bg="green",fg="white", command=self.clear_timetable)
        self.clear_button.grid(row=2, column=1, padx=(5, 10), pady=(20, 0), sticky=W + E)
        self.save_button = Button(self.root, text="Save", bg="green",fg="white", command=self.save_timetable)
        self.save_button.grid(row=2, column=2, padx=(5, 10), pady=(20, 0), sticky=W + E)

        # Selected Courses Listbox
        self.selected_courses_label = Label(self.root, text="Selected courses: ", bg="black", fg="white")
        self.selected_courses_label.grid(row=3, column=0, columnspan=5, padx=(5, 0), pady=(20, 0), sticky=W)
        self.selected_courses_listbox = Listbox(self.root, width=30)
        self.selected_courses_listbox.grid(row=4, column=0, columnspan=5, padx=(5, 0), pady=(5, 0), sticky=W)

        # Courses Listbox
        self.courses_label = Label(self.root, text="Courses: ", bg="black", fg="white")
        self.courses_label.grid(row=3, column=2, columnspan=50, padx=(70, 0), pady=(20, 0), sticky=W)
        self.courses_listbox = Listbox(self.root, width=50)
        self.courses_listbox.grid(row=4, column=2, columnspan=10, padx=(70, 0), pady=(5, 0), sticky=W)
        self.courses_listbox.bind("<<ListboxSelect>>", self.on_course_select)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_path_entry.delete(0, END)
            self.file_path_entry.insert(END, file_path)
            self.data_path = file_path

    def display_timetable(self):
        year = self.year_var.get()
        department = self.department_entry.get()

        if not self.data_path:
            messagebox.showwarning("Warning", "Please select a data file.")
            return

        if not year and not department:
            messagebox.showwarning("Warning", "Please select a year or department.")
            return

        selected_courses = []

        with open(self.data_path, "r", encoding="utf-8", errors="ignore") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            self.courses_listbox.delete(0, END)

            for row in reader:
                course_code = row[0]
                course_name = row[1]
                course_time = row[2]

                if department and not course_code.split()[0].startswith(department):
                    continue

                if year:
                    course_year = int(course_code.split()[1]) // 100  # Merni shifrën e parë të vitit
                    if course_year != int(year):
                        continue

                course_info = f"{course_code} - {course_name} ({course_time})"
                self.courses_listbox.insert(END, course_info)

                selected_courses.append(course_info)

        self.selected_courses = selected_courses

    def clear_timetable(self):
        self.selected_courses_listbox.delete(0, END)
        self.selected_courses = []
        self.courses_listbox.delete(0, END)

    def save_timetable(self):
        if not self.selected_courses:
            messagebox.showwarning("Warning", "No courses selected.")
            return

        file_path = "timetable.csv"
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Course Name", "Time"])
            for course in self.selected_courses:
                writer.writerow(course)

        messagebox.showinfo("Success", f"Timetable saved to {file_path}")

    def on_course_select(self, event):
        if (self.selected_courses_listbox.size() >= 6):
            messagebox.showwarning("Warning", "You have already selected 6 courses.")
            return
        course_info = self.courses_listbox.get(self.courses_listbox.curselection())
        course_time = course_info.split("(")[-1].strip(")")

        for selected_course_info in self.selected_courses_listbox.get(0, END):
            if course_info.split(" - ")[1].split(" (")[0] == selected_course_info.split(" - ")[1].split(" (")[0]:
                messagebox.showwarning("Warning", "Course already selected.")
                return

        self.selected_courses_listbox.insert(END, course_info)




if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()