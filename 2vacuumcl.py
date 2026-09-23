class VacuumEnvironment:
    def __init__(self, location_a="Dirty", location_b="Dirty"):
        self.locations = {"A": location_a, "B": location_b}
        self.agent_location = "A"

    def get_percept(self):
        """Returns current location and status."""
        return self.agent_location, self.locations[self.agent_location]

    def execute_action(self, action):
        """Updates the environment based on agent's action."""
        if action == "Suck":
            self.locations[self.agent_location] = "Clean"
        elif action == "Right":
            self.agent_location = "B"
        elif action == "Left":
            self.agent_location = "A"


def reflex_vacuum_agent(percept):
    """Reflex agent logic choosing an action based on percept."""
    location, status = percept
    if status == "Dirty":
        return "Suck"
    elif location == "A":
        return "Right"
    elif location == "B":
        return "Left"


# Run the agent in the environment
env = VacuumEnvironment(location_a="Dirty", location_b="Dirty")

print("Step-by-Step Execution:")
for step in range(1, 5):
    percept = env.get_percept()
    action = reflex_vacuum_agent(percept)
    print(f"Step {step}: Location={percept[0]} | Status={percept[1]} -> Action={action}")
    env.execute_action(action)