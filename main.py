import tkinter as tk
from tkinter import ttk
import json



class Subject:
    def __init__(self, name):
        self.name = name
        self.sections = []

    def add_section(self, section_name, chapters):
        section = {"name": section_name, "chapters": chapters}
        self.sections.append(section)

    def add_question(self, section_index, chapter_index, question, answer):
        if 0 <= section_index < len(self.sections) and 0 <= chapter_index < len(self.sections[section_index]['chapters']):
            self.sections[section_index]['chapters'][chapter_index]['questions'].append({"question": question, "answer": answer})

    def display_subject_info(self):
        info = f"Subject: {self.name}\n\nSections:\n"
        for section in self.sections:
            info += f"  - {section['name']}\n"
            info += "    Chapters:\n"
            for chapter in section['chapters']:
                info += f"      - {chapter['name']}\n"
        return info

    def get_questions_by_chapter(self, section_index, chapter_index):
        if 0 <= section_index < len(self.sections) and 0 <= chapter_index < len(self.sections[section_index]['chapters']):
            return self.sections[section_index]['chapters'][chapter_index]['questions']
        else:
            return None
        
    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.sections, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.sections = json.load(file)
        except FileNotFoundError:
            pass  # Ignore if the file doesn't exist

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Subject Explorer")

        # Set the font size for the Text widget
        text_font = ('Helvetica', 20)

        # Initialize subjects dictionary
        self.subjects = {}

        # Styling
        style = ttk.Style()
        style.configure("TButton", font=('Helvetica', 12))
        style.configure("TCombobox", font=('Helvetica', 12))
        style.configure("TLabel", font=('Helvetica', 12))

        # Add padding and spacing
        padx = 10
        pady = 5

        # Initialize info_text
        self.info_text = tk.Text(root, height=20, width=120, font=text_font, wrap=tk.WORD)
        self.info_text.grid(row=10, column=0, columnspan=2, padx=padx, pady=pady)

        # Add subject
        self.add_subject_button = ttk.Button(root, text="Add a new subject", command=self.dummy_function)
        self.add_subject_button.grid(row=0, column=1, padx=padx, pady=pady)

        # subject
        self.subject_label = ttk.Label(root, text="Subjects:")
        self.subject_label.grid(row=1, column=0, sticky=tk.W, padx=padx, pady=pady)

        self.subject_combobox = ttk.Combobox(root, values=["Governance Systems"], width=30, state="readonly")
        self.subject_combobox.grid(row=1, column=1, padx=padx, pady=pady)
        self.subject_combobox.bind("<<ComboboxSelected>>", self.load_subject_info)

        # section
        self.section_label = ttk.Label(root, text="Sections:")
        self.section_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self.section_combobox = ttk.Combobox(root, values=[], width=40)
        self.section_combobox.grid(row=2, column=1, padx=10, pady=5)
        self.section_combobox.bind("<<ComboboxSelected>>", self.load_section_info)

        # chapter
        self.chapter_label = ttk.Label(root, text="Chapters:")
        self.chapter_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

        self.chapter_combobox = ttk.Combobox(root, values=[], width=40)
        self.chapter_combobox.grid(row=3, column=1, padx=10, pady=5)
        self.chapter_combobox.bind("<<ComboboxSelected>>", self.display_selected_chapter)


        # Load questions and answers from file
        self.load_questions_and_answers()
        # Create the subject
        self.create_governance_systems_subject()

        # queston
        self.select_question_label = ttk.Label(root, text="Select Question:")
        self.select_question_label.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)

        self.select_question_combobox = ttk.Combobox(root, values=[], width=50)
        self.select_question_combobox.grid(row=4, column=1, padx=10, pady=5)
        self.select_question_combobox.bind("<<ComboboxSelected>>", self.display_selected_question)

        self.empty_label = ttk.Label(root, text="")
        self.empty_label.grid(row=5, column=0)

        self.question_label = ttk.Label(root, text="Question:")
        self.question_label.grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)

        self.question_entry = ttk.Entry(root, width=50)
        self.question_entry.grid(row=6, column=1, padx=10, pady=5)

        self.answer_label = ttk.Label(root, text="Answer:")
        self.answer_label.grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)

        self.answer_entry = ttk.Entry(root, width=50)
        self.answer_entry.grid(row=7, column=1, padx=10, pady=5)

        self.add_question_button = ttk.Button(root, text="Add or Edit an Entry", command=self.add_question)
        self.add_question_button.grid(row=8, column=1, padx=padx, pady=pady)

        self.delete_button = ttk.Button(root, text="Delete an Entry", command=self.delete_question)
        self.delete_button.grid(row=9, column=1, padx=padx, pady=pady)


        # Add horizontal and vertical scrollbars to the Text widget
        scroll_y = ttk.Scrollbar(root, command=self.info_text.yview)
        scroll_y.grid(row=9, column=2, sticky='nsew')
        self.info_text['yscrollcommand'] = scroll_y.set


        self.info_text.tag_configure("orange", foreground="orange")
        self.info_text.tag_configure("green", foreground="green")


    def dummy_function(self):
        print("Button clicked but does nothing.")


    def create_governance_systems_subject(self):
        # Load subjects data from JSON
        with open("subjects_data.json", 'r') as file:
            subjects_data = json.load(file)

        for subject_name, subject_data in subjects_data["subjects"].items():
            subject_instance = Subject(subject_name)

            for section_name, section_data in subject_data["sections"].items():
                section_chapters = section_data["chapters"]
                subject_instance.add_section(section_name, section_chapters)

            self.subjects[subject_name] = subject_instance

        # Add the new subject "Contemporary Issues" to the subjects dictionary
        if "Contemporary Issues" not in self.subjects:
            contemporary_issues_instance = Subject("Contemporary Issues")
            self.subjects["Contemporary Issues"] = contemporary_issues_instance

        # Load questions and answers for both subjects
        self.load_questions_and_answers()

        # Set the initial subject in the combobox
        self.subject_combobox['values'] = list(self.subjects.keys())
        self.subject_combobox.set("Governance Systems")
        self.load_subject_info(None)  # Load initial subject info


    def load_subject_info(self, event):
        selected_subject = self.subject_combobox.get()
        if selected_subject in self.subjects:
            subject_instance = self.subjects[selected_subject]
            if subject_instance:
                sections = [section['name'] for section in subject_instance.sections]
                self.section_combobox['values'] = sections
                self.section_combobox.set(sections[0] if sections else "")
                self.load_section_info(None)  # Load initial section info

                # Load questions and answers for the selected subject
                self.load_questions_and_answers()
            else:
                self.info_text.delete(1.0, tk.END)
                self.info_text.insert(tk.END, "No information available for this subject.")


    def load_section_info(self, event):
        selected_subject = self.subject_combobox.get()
        selected_section = self.section_combobox.get()
        selected_chapter = self.chapter_combobox.get()  # Store the currently selected chapter
        if selected_subject in self.subjects:
            subject_instance = self.subjects[selected_subject]
            if subject_instance:
                for section in subject_instance.sections:
                    if section['name'] == selected_section:
                        chapters = [chapter['name'] for chapter in section['chapters']]
                        self.chapter_combobox['values'] = chapters
                        # Set the chapter_combobox to the previously selected chapter if available
                        if selected_chapter in chapters:
                            self.chapter_combobox.set(selected_chapter)
                        else:
                            self.chapter_combobox.set(chapters[0] if chapters else "")
                        self.display_selected_chapter(None)  # Load initial chapter info
                        break

    def display_selected_chapter(self, event):
            selected_subject = self.subject_combobox.get()
            selected_section = self.section_combobox.get()
            selected_chapter = self.chapter_combobox.get()
            if selected_subject in self.subjects:
                subject_instance = self.subjects[selected_subject]
                if subject_instance:
                    for section in subject_instance.sections:
                        if section['name'] == selected_section:
                            for chapter in section['chapters']:
                                if chapter['name'] == selected_chapter:
                                    self.info_text.delete(1.0, tk.END)
                                    self.info_text.insert(tk.END, f"{selected_chapter}\n\n")
                                    questions = subject_instance.get_questions_by_chapter(
                                        subject_instance.sections.index(section), section['chapters'].index(chapter)
                                    )
                                    if questions:
                                        question_names = [q['question'] for q in questions]
                                        self.select_question_combobox['values'] = question_names
                                        self.select_question_combobox.set(question_names[0] if question_names else "")
                                        self.display_selected_question(None)  # Load initial selected question info
                                    else:
                                        self.info_text.insert(tk.END, "No questions available for this chapter.")
                                    # Adjust the width of the Text widget
                                    new_width = 120  # Adjust this value according to your needs
                                    self.info_text.config(width=new_width)
                                    break

    def display_selected_question(self, event):
        selected_subject = self.subject_combobox.get()
        selected_section = self.section_combobox.get()
        selected_chapter = self.chapter_combobox.get()
        selected_question = self.select_question_combobox.get()

        if selected_subject in self.subjects:
            subject_instance = self.subjects[selected_subject]
            if subject_instance:
                for section in subject_instance.sections:
                    if section['name'] == selected_section:
                        for chapter in section['chapters']:
                            if chapter['name'] == selected_chapter:
                                for q in chapter['questions']:
                                    if q['question'] == selected_question:
                                        # Pre-fill question and answer entry boxes
                                        self.question_entry.delete(0, tk.END)
                                        self.question_entry.insert(0, q['question'])
                                        self.answer_entry.delete(0, tk.END)
                                        self.answer_entry.insert(0, q['answer'])

                                        self.info_text.delete(1.0, tk.END)
                                        self.info_text.insert(tk.END, f"{selected_chapter}\n\n")
                                        self.info_text.insert(tk.END, f"Question: ", "orange")
                                        self.info_text.insert(tk.END, f"{q['question']}\n", "normal")
                                        self.info_text.insert(tk.END, f"Answer: ", "green")
                                        self.info_text.insert(tk.END, f"{q['answer']}\n\n", "normal")



    def delete_question(self):
        # Get selected values
        selected_subject = self.subject_combobox.get()
        selected_section = self.section_combobox.get()
        selected_chapter = self.chapter_combobox.get()
        selected_question = self.select_question_combobox.get()

        if selected_subject in self.subjects:
            subject_instance = self.subjects[selected_subject]
            if subject_instance:
                for section_index, section in enumerate(subject_instance.sections):
                    if section['name'] == selected_section:
                        for chapter_index, chapter in enumerate(section['chapters']):
                            if chapter['name'] == selected_chapter:
                                for q_index, q in enumerate(chapter['questions']):
                                    if q['question'] == selected_question:
                                        # Remove the selected question/answer
                                        del chapter['questions'][q_index]

                                        # Reload section info to update questions
                                        self.load_section_info(None)

                                        # Save questions and answers after deleting a question
                                        self.save_questions_and_answers()
                                        break

        # Clear the question and answer entry fields
        self.question_entry.delete(0, tk.END)
        self.answer_entry.delete(0, tk.END)

    def load_questions_and_answers(self):
        selected_subject = self.subject_combobox.get()
        if selected_subject in self.subjects:
            subject_instance = self.subjects[selected_subject]
            if subject_instance:
                # Assuming the filename is based on the subject name
                filename = f"{selected_subject.replace(' ', '_')}_data.json"
                subject_instance.load_from_file(filename)

    def save_questions_and_answers(self):
        selected_subject = self.subject_combobox.get()
        if selected_subject in self.subjects:
            subject_instance = self.subjects[selected_subject]
            if subject_instance:
                # Assuming the filename is based on the subject name
                filename = f"{selected_subject.replace(' ', '_')}_data.json"
                subject_instance.save_to_file(filename)

    def add_question(self):
        selected_subject = self.subject_combobox.get()
        selected_section = self.section_combobox.get()
        selected_chapter = self.chapter_combobox.get()
        question = self.question_entry.get()
        answer = self.answer_entry.get()

        if selected_subject in self.subjects:
            subject_instance = self.subjects[selected_subject]
            if subject_instance:
                for section_index, section in enumerate(subject_instance.sections):
                    if section['name'] == selected_section:
                        for chapter_index, chapter in enumerate(section['chapters']):
                            if chapter['name'] == selected_chapter:
                                # Remove the old question-answer set with the same question
                                old_question_set = [q for q in chapter['questions'] if q['question'] == question]
                                if old_question_set:
                                    chapter['questions'].remove(old_question_set[0])

                                # Add the new question-answer set
                                subject_instance.add_question(section_index, chapter_index, question, answer)
                                self.load_section_info(None)  # Reload section info to update questions
                                break

        # Save questions and answers after adding a new question
        self.save_questions_and_answers()

        # Clear the question and answer entry fields
        self.question_entry.delete(0, tk.END)
        self.answer_entry.delete(0, tk.END)

    def edit_question(self):
        # Get selected values
        selected_subject = self.subject_combobox.get()
        selected_section = self.section_combobox.get()
        selected_chapter = self.chapter_combobox.get()
        selected_question = self.select_question_combobox.get()
        new_answer = self.answer_entry.get()

        if selected_subject in self.subjects:
            subject_instance = self.subjects[selected_subject]
            if subject_instance:
                for section_index, section in enumerate(subject_instance.sections):
                    if section['name'] == selected_section:
                        for chapter_index, chapter in enumerate(section['chapters']):
                            if chapter['name'] == selected_chapter:
                                for q_index, q in enumerate(chapter['questions']):
                                    if q['question'] == selected_question:
                                        # Keep the question unchanged but update the answer
                                        q['answer'] = new_answer

                                        # Reload section info to update questions
                                        self.load_section_info(None)

                                        # Save questions and answers after editing a question
                                        self.save_questions_and_answers()
                                        break


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()