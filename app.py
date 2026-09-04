from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
template_folder="Templates"

tasks = []
schedule = []


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/tasks", methods=["GET", "POST"])
def task_page():
    if request.method == "POST":
        task_name = request.form.get("task")

        if task_name:
            tasks.append({
                "name": task_name,
                "completed": False
            })

        return redirect(url_for("task_page"))

    return render_template("tasks.html", tasks=tasks)


@app.route("/complete", methods=["POST"])
def complete():
    completed = request.form.getlist("completed")

    for i, task in enumerate(tasks):
        task["completed"] = str(i) in completed

    return redirect(url_for("task_page"))


@app.route("/schedule", methods=["GET", "POST"])
def schedule_page():
    if request.method == "POST":
        time = request.form.get("time")
        subject = request.form.get("subject")

        if time and subject:
            schedule.append({
                "time": time,
                "subject": subject
            })

        return redirect(url_for("schedule_page"))

    return render_template("schedule.html", schedule=schedule)


@app.route("/progress")
def progress():
    total_tasks = len(tasks)
    completed_tasks = sum(
        1 for task in tasks if task["completed"]
    )
    pending_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        percentage = (completed_tasks / total_tasks) * 100
    else:
        percentage = 0

    return render_template(
        "progress.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        progress=percentage
    )


if __name__ == "__main__":
    app.run()
