from pawpal_system import Task, Pet, Owner, Scheduler

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
    