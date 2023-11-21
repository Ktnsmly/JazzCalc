import tkinter as tk
import logic
from traits import activation_thresholds

class ChampionGrid:
    def __init__(self, master, champions):
        self.master = master
        self.champions = champions
        self.team = []
        self.buttons = []
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.create_grid()
        self.create_clear_button()

    def create_grid(self):
        for i, champ in enumerate(self.champions):
            # Create a button with the champion's name
            button = tk.Button(self.frame, text=champ.name, command=lambda champ=champ: self.champion_click(champ), width=7, height =1)
            button.grid(row=i // 13, column=i % 13, sticky='w', padx=5)  # Arrange buttons in a grid
            self.buttons.append(button)

    def create_clear_button(self):
        clear_button = tk.Button(self.frame, text='Clear Team', command=self.clear_team)
        clear_button.grid(row=6, column=6)

    def champion_click(self, champ):
        self.team.append(champ)
        count, traits = logic.evaluate_team(self.team, activation_thresholds)
        current = format_team_info([self.team], count)
        update_current_team(current)

    def clear_team(self):
        self.team = []
        update_current_team("")

def format_team_info(best_teams, max_activated):
    info_str = f"There are {len(best_teams)} teams with {max_activated} traits activated\n\n"
    for i, team in enumerate(best_teams):
        info_str += f'Team: {i+1} Activates: {max_activated} traits\n'
        for champ in team:
            info_str += f"{champ.name:12} ({champ.cost}) (Traits: {', '.join(champ.traits)})\n"
        info_str += "\n"
    return info_str

def update_output(info):
	output_text.delete('1.0', 'end')
	output_text.insert(tk.END, info + "\n")
	output_text.see(tk.END)  # Auto-scrolls to the end

def update_current_team(info):
    current_team.delete('1.0', 'end')
    current_team.insert(tk.END, info + "\n")
    current_team.see(tk.END)

def get_team_size(champion_grid):
    team_size = team_size_slider.get()
    selected_costs = [cost for cost, var in cost_vars.items() if var.get() == 1]
    filtered_champions = logic.filter_by_cost(logic.champions, selected_costs)
    best_teams, traits, max_activated = logic.brute_force_solution2(
        filtered_champions, activation_thresholds, team_size, champion_grid.team)
    info_str = format_team_info(best_teams, max_activated)
    update_output(info_str)


#GUI Layout
root = tk.Tk()
root.title("Team Builder")

#How many units are on the team
label = tk.Label(text='Set Max Team Size:')
label.pack()
team_size_slider = tk.Scale(root, from_=3, to=10, orient='horizontal', length =200)
team_size_slider.pack()

#Determines which unit costs to include
cost_label = tk.Label(text = 'Include Costs:')
cost_label.pack()
cost_vars = {i: tk.IntVar() for i in range(1, 6)}  # Create a dictionary of IntVar for costs 1-5

cost_checkboxes_frame = tk.Frame(root)
cost_checkboxes_frame.pack()

for cost, var in cost_vars.items():
    checkbox = tk.Checkbutton(cost_checkboxes_frame, text=str(cost), variable=var)
    checkbox.pack(side=tk.LEFT)

button_frame = tk.Frame(root)
button_frame.pack()

app = ChampionGrid(root, logic.champions)
    
# Button to get the value from the slider
get_value_button = tk.Button(root, text="Calculate", command=lambda: get_team_size(app))
get_value_button.pack()

current_team = tk.Text(root, height=10, width = 65)
current_team.pack()

output_text = tk.Text(root, height=30, width=65)
output_text.pack()


root.mainloop()






