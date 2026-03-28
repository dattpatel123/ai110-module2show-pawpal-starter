from datetime import time
from pawpal_system import Task, Pet, Owner, Scheduler

# --- Owner setup ---
owner = Owner(
    name="Jordan"
    
)

# --- Pets ---
buddy = Pet(name="Buddy", age=5, species="dog")
mochi = Pet(name="Mochi", age=3, species="cat")

# --- Tasks for Buddy (dog) ---
buddy.add_task(Task(
    task_type="Morning Walk",
    duration=30,
    priority=5,
    scheduled_time=time(7, 0),
))
buddy.add_task(Task(
    task_type="Breakfast",
    duration=60,
    priority=4,
    scheduled_time=time(8, 0),
))
buddy.add_task(Task(
    task_type="Grooming",
    duration=20,
    priority=2,
    scheduled_time=time(10, 0),
))

# --- Tasks for Mochi (cat) ---
mochi.add_task(Task(
    task_type="Breakfast",
    duration=5,
    priority=4,
    scheduled_time=time(8, 0),
))
mochi.add_task(Task(
    task_type="Litter Box Clean",
    duration=10,
    priority=3,
    scheduled_time=time(9, 0),
))
mochi.add_task(Task(
    task_type="Playtime",
    duration=15,
    priority=2,
    scheduled_time=time(11, 0),
))

mochi.add_task(Task(
    task_type="Conflict with playtime",
    duration=15,
    priority=2,
    scheduled_time=time(11, 0),
))

# --- Register pets with owner ---
owner.add_pet(buddy)
owner.add_pet(mochi)

# --- Generate and display schedule ---
scheduler = Scheduler(owner)
for task, pet, task.scheduled_time, reason in scheduler.generate_schedule():
    print(f"{task.scheduled_time.strftime('%H:%M')}: {task.task_type} for {pet.name} (Reason: {reason})")
