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
        self.create_text_input()
        self.create_clear_button()
        self.create_filter_by_text_button()

    def create_grid(self):
        for i, champ in enumerate(self.champions):
            # Create a button with the champion's name
            button = tk.Button(self.frame, text=champ.name, command=lambda champ=champ: self.champion_click(champ), width=7, height =1)
            button.grid(row=i // 13, column=i % 13, sticky='w', padx=5)  # Arrange buttons in a grid
            self.buttons.append(button)

    def create_clear_button(self):
        clear_button = tk.Button(self.frame, text='Clear Team', command=self.clear_team)
        clear_button.grid(row=6, column=4)

    def champion_click(self, champ):
        self.team.append(champ)
        count, traits = logic.evaluate_team(self.team, activation_thresholds)
        header = f"Team has {len(self.team)} Units\n"
        current = format_team_info([self.team], count, header)
        update_current_team(current)

    def create_text_input(self):
        self.input_text = tk.Entry(self.frame)  # Create an Entry widget for text input
        self.input_text.grid(row=6, column =0, columnspan=13)
        self.input_text.bind("<Return>", self.filter_by_text)  # Bind the Enter key to the filter_by_text method

    def create_filter_by_text_button(self):
        filter_button = tk.Button(text = 'Filter', command = self.filter_by_text)
        filter_button.pack()
        
    def filter_by_text(self, event=None):
        inp = self.input_text.get()
        input_words = inp.split() if inp else []

    # Reset all buttons to original color if the text field is blank
        if inp.strip() == '':
            for button in self.buttons:
                button.config(bg='#f0f0f0')
            return  # Exit the function early

        for i, champ in enumerate(self.champions):
            match_found = False
            # Check if any input word matches the champion's name
            if any(word.lower() in champ.name.lower() for word in input_words):
                match_found = True

        # Check if any input word matches any of the champion's traits
            if not match_found:
                for trait in champ.traits:
                    if any(word.lower() in trait.lower() for word in input_words):
                        match_found = True
                        break

        # Update button color based on match found
            if match_found:
                self.buttons[i].config(bg='#f0f0f0')  # Set to original color if match is found
            else:
                self.buttons[i].config(bg='grey')  # Grey out if no match is found

    def clear_team(self):
        self.team = []
        update_current_team("")

def format_team_info(best_teams, max_activated, header):
    info_str = header
    for i, team in enumerate(best_teams):
        info_str +=  f'Team: {i+1} Activates: {max_activated} traits\n'
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
    header = f"There are {len(best_teams)} Teams that Activate {max_activated} Traits\n\n"
    info_str = format_team_info(best_teams, max_activated, header)
    update_output(info_str)



#GUI Layout
root = tk.Tk()
root.title("Team Builder")

#How many units are on the team
label = tk.Label(text='Set Max Team Size:')
label.pack()
team_size_slider = tk.Scale(root, from_=1, to=12, orient='horizontal', length =200)
team_size_slider.set(7)
team_size_slider.pack()

#Determines which unit costs to include
cost_label = tk.Label(text = 'Include Costs:')
cost_label.pack()
cost_vars = {i: tk.IntVar(value=1) for i in range(1, 6)}  # Create a dictionary of IntVar for costs 1-5

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






