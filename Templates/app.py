from flask import Flask, render_template, request

app = Flask(__name__)

# Store tasks
tasks = []

# Store study schedules
schedule_list = []


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- LOGIN PAGE ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        return render_template("dashboard.html")

    return render_template("login.html")


# ---------------- DASHBOARD PAGE ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# My Tasks
@app.route("/tasks", methods=["GET", "POST"])
def task_page():
    if request.method == "POST":
        task = request.form.get("task")

        if task:
            tasks.append({
                "name": task,
                "completed": False
            })

    return render_template("tasks.html", tasks=tasks)


# Complete Tasks
@app.route("/complete", methods=["POST"])
def complete_tasks():
    completed = request.form.getlist("completed")

    for i, task in enumerate(tasks):
        task["completed"] = str(i) in completed

    total = len(tasks)
    completed_count = sum(task["completed"] for task in tasks)
    pending_count = total - completed_count

    if total > 0:
        progress_percent = (completed_count / total) * 100
    else:
        progress_percent = 0

    return render_template(
        "progress.html",
        total_tasks=total,
        completed_tasks=completed_count,
        pending_tasks=pending_count,
        progress=progress_percent
    )
# ---------------- STUDY SCHEDULE PAGE ----------------
@app.route("/schedule", methods=["GET", "POST"])
def schedule_page():
    if request.method == "POST":
        time = request.form.get("time")
        subject = request.form.get("subject")

        if time and subject:
            schedule_list.append({
                "time": time,
                "subject": subject
            })

    return render_template(
        "schedule.html",
        schedule=schedule_list
    )


# ---------------- PROGRESS PAGE ----------------
@app.route("/progress")
def progress_page():
    total_tasks = len(tasks)
    completed_tasks = 0
    pending_tasks = total_tasks
    progress_percent = 0

    return render_template(
        "progress.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        progress=progress_percent
    )


# ---------------- RUN FLASK ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)