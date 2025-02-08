import urwid
import datetime
import json
import pandas as pd
import numpy as np

header = urwid.Text("Press ':q!' to quit, ':wq' to save & quit, ':w' to save.")

# --- Pomodoro Logic (placeholder) ------------------------------------------ #
pomodoro_running = False
timer_text = urwid.Text("Time: 00:00:00")

def start_pomodoro(button):
    """Placeholder: starts a Pomodoro session."""
    global pomodoro_running
    if not pomodoro_running:
        pomodoro_running = True
        timer_text.set_text("Pomodoro started (placeholder).")

def stop_pomodoro(button):
    """Placeholder: stops a Pomodoro session."""
    global pomodoro_running
    if pomodoro_running:
        pomodoro_running = False
        timer_text.set_text("Pomodoro stopped.")

# --- Task Management ------------------------------------------------------- #

# 1) We need a custom Edit that adds a task on Enter.
class TaskInputEdit(urwid.Edit):
    def __init__(self, caption, on_submit):
        super().__init__(caption)
        self.on_submit = on_submit

    def keypress(self, size, key):
        # If user presses Enter, call the callback to add a new task
        if key == 'enter':
            self.on_submit(self.edit_text)
            self.set_edit_text("")
            return
        return super().keypress(size, key)

def add_task(text):
    """Callback to create a new CheckBox task when user presses Enter."""
    text = text.strip()
    if text:
        task_list_walker.append(urwid.CheckBox(text))

# Create a walker and ListBox to hold tasks
task_list_walker = urwid.SimpleFocusListWalker([])
task_list_box = urwid.ListBox(task_list_walker)

# Create input box for tasks
task_input = TaskInputEdit("Add a task:\n", on_submit=add_task)
task_input_box = urwid.LineBox(task_input)

# Combine task list and task input in a pile
task_pile = urwid.Pile([
    task_list_box,           # The scrollable list of tasks
    task_input_box           # Input box for adding new tasks
])
task_box = urwid.LineBox(task_pile, title="Tasks")

# --- Notes Section --------------------------------------------------------- #
# A multiline Edit for notes
notes_edit = urwid.Edit("Notes:\n", multiline=True)
notes_box = urwid.LineBox(notes_edit, title="Notes")

# --- Pomodoro Timer Section ----------------------------------------------- #
pomodoro_timer = urwid.LineBox(timer_text, title="Pomodoro Timer")
pomodoro_start = urwid.Padding(
    urwid.Button("Start Pomodoro", on_press=start_pomodoro),
    align="center",
    width=("relative", 50)
)
pomodoro_stop = urwid.Padding(
    urwid.Button("Stop Pomodoro", on_press=stop_pomodoro),
    align="center",
    width=("relative", 50)
)

pomodoro_box = urwid.Pile([
    pomodoro_timer,
    pomodoro_start,
    pomodoro_stop
])

# --- Layout (Columns + Frame) --------------------------------------------- #
columns = urwid.Columns([task_box, notes_box])
frame = urwid.Frame(body=columns, header=header, footer=pomodoro_box)


# --- MainLoop ------------------------------------------------------------- #
def handle_input(key):
    """Handle keyboard commands like :q!, :w, :wq."""
    if key == ':q!':
        raise urwid.ExitMainLoop()
    elif key == ':wq':
        # Placeholder for saving logic, then quit
        # save_tasks_and_notes()
        raise urwid.ExitMainLoop()
    elif key == ':w':
        # Placeholder for saving logic
        # save_tasks_and_notes()
        pass


loop = urwid.MainLoop(frame)
loop.run()
