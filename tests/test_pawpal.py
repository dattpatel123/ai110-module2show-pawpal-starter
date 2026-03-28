from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import time, datetime, timedelta
def test_task_complete():
    task = Task(
        task_type="Morning Walk",
        duration=30,
        priority=5,
        window_start=None,
        window_end=None
    )
    assert task.complete == False
    task.set_complete()
    assert task.complete == True
def test_task_addition():
    pet = Pet(name="Buddy", age=5, species="dog")
    assert len(pet.tasks) == 0
    task = Task(
        task_type="Morning Walk",
        duration=30,
        priority=5,
        window_start=None,
        window_end=None
    )
    pet.add_task(task)
    assert len(pet.tasks) ==1
def test_add_pet_to_owner():
    owner = Owner(name="Jordan")
    pet = Pet(name="Buddy", age=5, species="dog")
    assert len(owner.pets) == 0
    owner.add_pet(pet)
    assert len(owner.pets) == 1
def test_scheduler():
    owner = Owner(name="Jordan")
    pet = Pet(name="Buddy", age=5, species="dog")
    task1 = Task(
        task_type="Morning Walk",
        duration=30,
        priority=5,
        window_start=None,
        window_end=None,
        scheduled_time=time(7, 0)
    )
    task2 = Task(
        task_type="Breakfast",
        duration=60,
        priority=4,
        window_start=None,
        window_end=None,
        scheduled_time=time(8, 0)
    )
    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)
    
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule()
    
    assert len(schedule) == 2
    assert schedule[0][0].task_type == "Morning Walk"
    assert schedule[1][0].task_type == "Breakfast"
def test_conflict():
    owner = Owner(name="Jordan")
    pet = Pet(name="Buddy", age=5, species="dog")
    task1 = Task(
        task_type="Morning Walk",
        duration=30,
        priority=5,
        window_start=None,
        window_end=None,
        scheduled_time=time(7, 0)
    )
    task2 = Task(
        task_type="Breakfast",
        duration=60,
        priority=4,
        window_start=None,
        window_end=None,
        scheduled_time=time(7, 0)  # Overlaps with Morning Walk
    )
    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)
    
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule()
    assert len(schedule) == 2
    assert "conflict" in schedule[1][3]
def test_recurrence():
    task = Task(
        task_type="Daily Walk",
        duration=30,
        priority=5,
        window_start=None,
        window_end=None,
        recurrence="daily"
    )
    assert task.is_due_today() == True
    task.set_complete()
    assert task.is_due_today() == False
    # Simulate next day
    task.last_completed -= timedelta(days=1)
    assert task.is_due_today() == True