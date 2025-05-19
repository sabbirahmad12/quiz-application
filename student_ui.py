import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from excel_db import get_all_quizzes, get_quiz_questions, get_leaderboard_data, save_score

class StudentDashboard(tk.Toplevel):
    def __init__(self, master, user_id, user_name=None):
        super().__init__(master)
        self.title("Student Dashboard")
        self.geometry("1200x650")
        self.user_id = user_id
        self.user_name = user_name or f"Student_{user_id}"
        self._setup_ui()
        
    def _setup_ui(self):
        self.notebook = ttk.Notebook(self)
        
        # Tab Create
        self.quiz_tab = ttk.Frame(self.notebook)
        self.leaderboard_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.quiz_tab, text="Available Quizzes")
        self.notebook.add(self.leaderboard_tab, text="Leaderboard")
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # UI Setup
        self._setup_quiz_tab()
        self._setup_leaderboard_tab()
        self._load_data()
    
    def _setup_quiz_tab(self):
        # Quiz List UI
        ttk.Label(self.quiz_tab, 
                text="Available Quizzes", 
                style='Title.TLabel').pack(pady=20)
        
        # Treeview
        self.quiz_tree = ttk.Treeview(self.quiz_tab, 
                                    columns=('ID', 'Subject', 'Title', 'Description'), 
                                    show='headings',
                                    height=15)
        
        # Column Heading
        self.quiz_tree.heading('ID', text='ID')
        self.quiz_tree.heading('Subject', text='Subject')
        self.quiz_tree.heading('Title', text='Title')
        self.quiz_tree.heading('Description', text='Description')
        
        # column width
        self.quiz_tree.column('ID', width=50, anchor='center')
        self.quiz_tree.column('Subject', width=150)
        self.quiz_tree.column('Title', width=200)
        self.quiz_tree.column('Description', width=300)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.quiz_tab, orient="vertical", command=self.quiz_tree.yview)
        self.quiz_tree.configure(yscrollcommand=scrollbar.set)
        
        self.quiz_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        # Button Frame
        btn_frame = ttk.Frame(self.quiz_tab)
        btn_frame.pack(pady=10)
        
        # Start Quiz Button
        ttk.Button(btn_frame, 
                text="Start Selected Quiz", 
                command=self._start_quiz).pack(side='left', padx=10, ipadx=20)
        
        # Refresh Button
        ttk.Button(btn_frame,
                text="Refresh Quizzes",
                command=self._load_quizzes).pack(side='left', padx=10, ipadx=20)
    
    def _start_quiz(self):
        """নির্বাচিত কুইজ শুরু করুন"""
        selected_item = self.quiz_tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a quiz first!")
            return
        
        item_data = self.quiz_tree.item(selected_item)
        quiz_id, subject, title, description = item_data['values']
        
        # New Quiz Window Create
        quiz_window = tk.Toplevel(self)
        quiz_window.title(f"{subject}: {title}")
        quiz_window.geometry("900x700")
        
        questions = get_quiz_questions(quiz_id)
        
        if not questions:
            messagebox.showerror("Error", "No questions found for this quiz!")
            quiz_window.destroy()
            return
        
        # Create a class to hold quiz state
        class QuizState:
            def __init__(self):
                self.current_question = 0
                self.score = 0
                self.time_left = 30
                self.timer = None
                self.start_time = datetime.now()
                self.answered_questions = 0
        
        state = QuizState()
        
        # Main Frame
        main_frame = ttk.Frame(quiz_window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        def show_question():
            # Clear previous widgets
            for widget in main_frame.winfo_children():
                widget.destroy()
            
            if state.current_question >= len(questions):
                show_results()
                return
            
            question = questions[state.current_question]
            
            # Header Frame
            header_frame = ttk.Frame(main_frame)
            header_frame.pack(fill='x', pady=10)
            
            ttk.Label(header_frame, 
                    text=f"Question {state.current_question+1}/{len(questions)} | {question.get('category', 'General')}",
                    font=('Helvetica', 12)).pack(side='left')
            
            # Timer label
            time_label = ttk.Label(header_frame, 
                                text=f"Time left: {state.time_left}s",
                                font=('Helvetica', 12, 'bold'),
                                foreground='red')
            time_label.pack(side='right')
            
            # Question Text
            ttk.Label(main_frame,
                    text=question["question_text"],
                    font=('Helvetica', 16, 'bold'),
                    wraplength=800).pack(pady=20)
            
            # Option Frame
            options_frame = ttk.Frame(main_frame)
            options_frame.pack(pady=20)
            
            # Check if this is a previous question
            is_previous_question = state.current_question < state.answered_questions
            
            for idx, option in enumerate(question["options"], start=1):
                btn = ttk.Button(options_frame,
                                text=f"{idx}. {option}",
                                width=40,
                                command=lambda selected=idx: check_answer(selected, question["correct_answer"]))
                btn.pack(pady=5)
                
                # Disable button if it's a previous question
                if is_previous_question:
                    btn.configure(state='disabled')

            # Navigation Button
            nav_frame = ttk.Frame(main_frame)
            nav_frame.pack(pady=20)
            
            if state.current_question > 0:
                ttk.Button(nav_frame,
                        text="<< Previous",
                        command=lambda: go_to_question(-1)).pack(side='left', padx=10)
            
            ttk.Button(nav_frame,
                    text="Next >>",
                    command=lambda: go_to_question(1)).pack(side='right', padx=10)
            
            if state.timer:
                quiz_window.after_cancel(state.timer)
            start_timer(time_label)
        
        def start_timer(label):
            state.time_left = 30
            
            def update():
                state.time_left -= 1
                label.config(text=f"Time left: {state.time_left}s")
                
                if state.time_left <= 0:
                    go_to_question(1)
                else:
                    state.timer = quiz_window.after(1000, update)
            
            state.timer = quiz_window.after(1000, update)
        
        def check_answer(selected_index, correct_index):
            if state.timer:
                quiz_window.after_cancel(state.timer)

            if selected_index == correct_index + 1:
                state.score += 1
                messagebox.showinfo("Correct!", "Your answer is correct!")
            else:
                messagebox.showinfo("Incorrect", f"Correct answer was: Option {correct_index + 1}")

            # Update answered questions count
            state.answered_questions = max(state.answered_questions, state.current_question + 1)
            go_to_question(1)

        def go_to_question(step):
            state.current_question += step
            show_question()
        
        def show_results():
            for widget in main_frame.winfo_children():
                widget.destroy()
            
            # Result Calculate
            time_taken = (datetime.now() - state.start_time).seconds
            percentage = int((state.score / len(questions)) * 100)

            ttk.Label(main_frame,
                    text="Quiz Completed!",
                    font=('Helvetica', 24, 'bold')).pack(pady=20)
            
            ttk.Label(main_frame,
                    text=f"Your Score: {state.score}/{len(questions)} ({percentage}%)",
                    font=('Helvetica', 18)).pack(pady=10)
            
            ttk.Label(main_frame,
                    text=f"Time Taken: {time_taken} seconds",
                    font=('Helvetica', 14)).pack(pady=10)
            
            # btn Frame
            btn_frame = ttk.Frame(main_frame)
            btn_frame.pack(pady=30)
            
            ttk.Button(btn_frame,
                    text="View Leaderboard",
                    command=lambda: [self.notebook.select(self.leaderboard_tab), quiz_window.destroy()]).pack(side=tk.LEFT, padx=10)
            
            ttk.Button(btn_frame,
                    text="Close",
                    command=quiz_window.destroy).pack(side=tk.LEFT, padx=10)
            
            # Ledaer Board score Save
            save_score(self.user_id, self.user_name, quiz_id, percentage, time_taken)
    
        show_question()
    
    def _setup_leaderboard_tab(self):
        # Leaderboard UI
        ttk.Label(self.leaderboard_tab, 
                text="Quiz Leaderboard", 
                style='Title.TLabel').pack(pady=20)
        
        self.leaderboard_tree = ttk.Treeview(self.leaderboard_tab, 
                                           columns=('Rank', 'Student', 'Quiz', 'Score'), 
                                           show='headings',
                                           height=15)
        
        self.leaderboard_tree.heading('Rank', text='Rank')
        self.leaderboard_tree.heading('Student', text='Student')
        self.leaderboard_tree.heading('Quiz', text='Quiz')
        self.leaderboard_tree.heading('Score', text='Score (%)')
        
        self.leaderboard_tree.column('Rank', width=50, anchor='center')
        self.leaderboard_tree.column('Student', width=150)
        self.leaderboard_tree.column('Quiz', width=200)
        self.leaderboard_tree.column('Score', width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(self.leaderboard_tab, orient="vertical", command=self.leaderboard_tree.yview)
        self.leaderboard_tree.configure(yscrollcommand=scrollbar.set)
        
        self.leaderboard_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
    
        btn_frame = ttk.Frame(self.leaderboard_tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame,
                text="Refresh Leaderboard",
                command=self._load_leaderboard).pack(ipadx=20, pady=5)

    def _load_data(self):
        """সমস্ত ডাটা লোড করুন"""
        self._load_quizzes()
        self._load_leaderboard()
    
    def _load_quizzes(self):
        for item in self.quiz_tree.get_children():
            self.quiz_tree.delete(item)
        
        # Load Quiz from excel
        quizzes = get_all_quizzes()

        for i, quiz in enumerate(quizzes, 1):  # Start from 1
            if ':' in quiz['title']:
                subject, title = quiz['title'].split(':', 1)
                subject = subject.strip()
                title = title.strip()
            else:
                subject = "General"
                title = quiz['title']
            
            self.quiz_tree.insert('', 'end', 
                                values=(i,  # Use i instead of quiz['id']
                                    subject,
                                    title,
                                    quiz.get('description', '')))
    
    def _load_leaderboard(self):
        for item in self.leaderboard_tree.get_children():
            self.leaderboard_tree.delete(item)
        
        # Load Leaderboard data from excel
        leaderboard = get_leaderboard_data()
        
        for i, entry in enumerate(leaderboard[:20], 1):
            self.leaderboard_tree.insert('', 'end', 
                                       values=(i, entry['student_name'], 
                                              entry['quiz_title'], entry['score']))