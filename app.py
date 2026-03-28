import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
# pet_name = st.text_input("Pet name", value="Mochi")
# species = st.selectbox("Species", ["dog", "cat", "other"])
if st.button("Submit Owner"):
    st.session_state.owner = Owner(name=owner_name)

    # Success
    st.success(f"Owner '{owner_name}' created!")


st.markdown("### Pets")
pet_name = st.text_input("Pet name", value="")
pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species")

if st.button("Add Pet"):
    if not st.session_state.get("owner"):
        st.error("Please create an owner first.")
    if pet_name in [pet.name for pet in st.session_state.owner.pets]:
        st.error("Pet name must be unique.")
    else:
        st.session_state.owner.add_pet(Pet(name=pet_name, species=pet_species))
        st.success(f"Pet '{pet_name}' added to owner '{st.session_state.owner.name}'!")




st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    scheduled_time = st.time_input("Preferred time")
with col5:
    recurrence = st.selectbox("Recurrence", ["one-time", "daily", "weekly", "monthly"])
with col6:
    pet_name = st.selectbox("Pet", [pet.name for pet in st.session_state.owner.pets] if st.session_state.get("owner") else ["—"])
if st.button("Add task"):
    owner = st.session_state.get("owner")
    if owner is None:
        st.error("Please create an owner first.")
    selected_pet = st.session_state.owner.get_pet_by_name(pet_name)
    if selected_pet and task_title in [task.task_type for task in selected_pet.tasks]:
        st.error("Task title must be unique.")
    else:
        recurrence_val = None if recurrence == "one-time" else recurrence
        task = Task(
            task_type=task_title,
            duration=int(duration),
            priority={"low": 1, "medium": 3, "high": 5}[priority],
            scheduled_time=scheduled_time,
            recurrence=recurrence_val,
        )
        st.session_state.owner.add_task(st.session_state.owner.get_pet_by_name(pet_name),task)
        

owner = st.session_state.get("owner")
if owner and any(pet.tasks for pet in owner.pets):
    st.write("Current tasks:")
    for pet in owner.pets:
        for task in pet.tasks:
            col_a, col_b = st.columns([4, 1])
            with col_a:
                recur_label = f" ({task.recurrence})" if task.recurrence else ""
                time_label = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "no time"
                st.write(f"**{task.task_type}** — {pet.name} | {time_label}{recur_label} | priority {task.priority}")
            with col_b:
                if st.button("Done" if not task.complete else "Undo", key=f"{pet.name}_{task.task_type}"):
                    task.set_complete(not task.complete)
                    st.rerun()
elif not st.session_state.tasks:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    
    scheduler = Scheduler(st.session_state.owner)  
    schedule = scheduler.generate_schedule()  # This should return a list of scheduled tasks with explanations
    st.write("Generated Schedule:")
    for task, pet, start, reason in schedule:
            time_str = start.strftime('%H:%M') if start else "No time"
            st.write(f"  {time_str:15}  {task.task_type:20} ({pet.name}) — {reason}")
            
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
