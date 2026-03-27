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
    window_start=time(7, 0), # 7-8am
    window_end=time(8, 0)
))
buddy.add_task(Task(
    task_type="Breakfast",
    duration=60, 
    priority=4,
    window_start =time(7, 0), # 8-9am
    window_end=time(8, 0)

))
buddy.add_task(Task(
    task_type="Grooming",
    duration=20,
    priority=2,
    window_start=time(10, 0), # 10-11am
    window_end=time(11, 0)
))

# --- Tasks for Mochi (cat) ---
mochi.add_task(Task(
    task_type="Breakfast",
    duration=5,
    priority=4,
    window_start=time(8, 0),
    window_end=time(9, 0)

))
mochi.add_task(Task(
    task_type="Litter Box Clean",
    duration=10,
    priority=3,
    window_start=time(9, 0),
    window_end=time(10, 0)

))
mochi.add_task(Task(
    task_type="Playtime",
    duration=15,
    priority=2,
    window_start=time(11, 0),
    window_end=time(12, 0)
))

# --- Register pets with owner ---
owner.add_pet(buddy)
owner.add_pet(mochi)

# --- Generate and display schedule ---
scheduler = Scheduler(owner)
scheduler.generate_schedule()
scheduler.display_schedule()