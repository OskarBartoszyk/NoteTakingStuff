import urwid
import json


def main():
    # Task List
    tasks = urwid.SimpleFocusListWalker([])  # Start with an empty list
    task_list = urwid.ListBox(tasks)
    task_box = urwid.LineBox(task_list, title="Tasks")

    # Sub-tasks
    subtasks = [
        urwid.AttrMap(urwid.CheckBox("a high priority task"), 'high_priority'),
        urwid.AttrMap(urwid.CheckBox("a medium priority task"), 'medium_priority'),
        urwid.AttrMap(urwid.CheckBox("a low priority task"), 'low_priority'),
        urwid.AttrMap(urwid.CheckBox("a completed task", state=True), 'completed_task'),
    ]
    subtask_list = urwid.ListBox(urwid.SimpleFocusListWalker(subtasks))
    subtask_box = urwid.LineBox(subtask_list, title="Sub-tasks")

    selection_text = urwid.Edit("Add a task (e.g., 'Task Name: high'):\n", multiline=False)
    selection_box = urwid.LineBox(selection_text)

    columns = urwid.Columns([task_box, subtask_box])
    pile = urwid.Pile([columns, selection_box])

    palette = [
        ('high_priority', 'dark red', ''),
        ('medium_priority', 'brown', ''),
        ('low_priority', 'dark green', ''),
        ('completed_task', 'light gray', ''),
    ]

    def parse_priority(task_text):
        """Extract priority from task text."""
        if ':' in task_text:
            task, priority = task_text.rsplit(':', 1)
            return task.strip(), priority.strip().lower()
        return task_text.strip(), None

    def add_task(text):
        """Add a task with the given priority."""
        task, priority = parse_priority(text)
        if not task:
            return  # Ignore empty tasks

        # Map priority to a color
        if priority == 'high':
            tasks.append(urwid.AttrMap(urwid.CheckBox(task), 'high_priority'))
        elif priority == 'medium':
            tasks.append(urwid.AttrMap(urwid.CheckBox(task), 'medium_priority'))
        elif priority == 'low':
            tasks.append(urwid.AttrMap(urwid.CheckBox(task), 'low_priority'))
        else:
            tasks.append(urwid.CheckBox(task))  # Default without color

        # Append the task information to the secondary file as "not done" by default
        append_task_to_file(task, "not done", priority or "none")

    def handle_input(key):
        """Handle user input for commands and task addition."""
        if key == ':q!':  # Force quit
            raise urwid.ExitMainLoop()
        elif key == ':wq':  # Save and quit
            footer.set_text(save_tasks())
            raise urwid.ExitMainLoop()
        elif key == ':w':  # Save only
            footer.set_text(save_tasks())
        elif key == 'enter':  # Add a new task
            new_task = selection_text.get_edit_text().strip()
            if new_task.startswith(":"):  # Handle commands
                handle_input(new_task)
            elif new_task:  # Add task
                add_task(new_task)
                selection_text.set_edit_text("")
        else:
            footer.set_text("")

    def save_tasks():
        """Save tasks to a JSON file."""
        task_data = []
        for item in tasks:
            # If 'item' is an AttrMap, unwrap it to get the CheckBox.
            task_widget = item.original_widget if isinstance(item, urwid.AttrMap) else item
            # Check the state of the CheckBox correctly
            done_status = "done" if task_widget.state else "not done"

            # Determine priority based on the AttrMap attribute
            priority = (
                "high"   if item.attr == "high_priority"   else
                "medium" if item.attr == "medium_priority" else
                "low"    if item.attr == "low_priority"    else
                "none"
            )
            task_label = task_widget.get_label()
            task_data.append({
                "status": done_status,
                "task": task_label,
                "priority": priority
            })

        with open("tasks.json", "w") as f:
            json.dump(task_data, f, indent=4)
        return "Tasks saved."

    def append_task_to_file(task, status, priority):
        """Append task to a secondary JSON file."""
        task_entry = {
            "status": status,
            "task": task,
            "priority": priority
        }
        try:
            with open("all_tasks_log.json", "r") as f:
                all_tasks = json.load(f)
        except FileNotFoundError:
            all_tasks = []

        all_tasks.append(task_entry)

        with open("all_tasks_log.json", "w") as f:
            json.dump(all_tasks, f, indent=4)

    footer = urwid.Text("Press ':q!' to quit, ':wq' to save & quit, ':w' to save.")
    frame = urwid.Frame(body=pile, footer=footer)

    loop = urwid.MainLoop(frame, palette, unhandled_input=handle_input)
    loop.run()


if __name__ == "__main__":
    main()