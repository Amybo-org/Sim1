import csv
import random
import pyperclip
import time  # Import the time module
from fermentation import simulate_fermentation
from visualisation import plot_total_OD
from fermentation import Strain
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

def main():
    # Read the strains from the CSV file
    strains = []
    with open('data/strains_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            strains.append(Strain(*row))

    # Separate the strains into good strains and pathogenic strains
    good_strains = [strain for strain in strains if strain.type == 'good']
    all_strains = strains

    # Run the fermentation simulation multiple times with just the good strains
    print('Running fermentation with good strains...')
    good_ODs = [simulate_fermentation(good_strains, [random.random() for _ in range(len(good_strains))]) for _ in range(5)]

    # Run the fermentation simulation once with all strains
    print('Running fermentation with all strains...')
    all_OD = simulate_fermentation(all_strains, [random.random() for _ in range(len(all_strains))])

    # Randomly insert the results of the fermentation with all strains into the list of results
    contaminated_index = random.randint(0, 5)
    good_ODs.insert(contaminated_index, all_OD)

    # Plot the results
    print('Plotting results...')
    def plot_data(good_ODs):
        fig, ax = plt.subplots()
        for i, od in enumerate(good_ODs, start=1):
            line, = ax.plot(od, label=str(i))
            line.set_picker(5)  # Enable picking on the line with 5 pixel tolerance
        ax.set_title('Click on the plot you think is contaminated')  # Add a title to the plot
        plt.legend(title='Fermentation Number')  # Show the legend with a title
        return fig, ax  # Ensure that a tuple is always returned

    # Ask the user to identify the contaminated fermentation
    contaminated_index += 1  # Adjust index to match 1-based numbering in labels
    print(f'The contaminated fermentation is at index {contaminated_index}')  # AI finds the contaminated fermentation

    def onpick(event):
        if isinstance(event.artist, Line2D):
            line = event.artist
            label = line.get_label()
            color = line.get_color()
            if label.isdigit():
                answer = int(label)
                if answer == contaminated_index:
                    text = f'Correct! Plot {label} with color {color} is contaminated.'
                else:
                    text = f'Incorrect. Plot {label} with color {color} is not contaminated.'
                fig.texts = []  # Remove previous texts
                fig.text(0.5, 0.01, text, ha='center')  # Add the new text
                fig.canvas.draw()  # Redraw the figure

    fig, ax = plot_data(good_ODs)
    fig.canvas.mpl_connect('pick_event', onpick)

    # Prepare the data and the instruction for the LLM
    instruction = "This is the optical density data from several fermentations. One of these contains a pathogenic strain. Please analyze the data and identify which fermentation is likely to be contaminated: "
    data_with_instruction = instruction + str(good_ODs)

    # Copy the data and the instruction to the clipboard
    pyperclip.copy(data_with_instruction)

    plt.show()

if __name__ == '__main__':
    main()