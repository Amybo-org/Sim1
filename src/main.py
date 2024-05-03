import csv
import random
from fermentation import simulate_fermentation
from visualisation import plot_total_OD
from fermentation import Strain
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

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
    good_ODs = [simulate_fermentation(good_strains, random.random()) for _ in range(5)]

    # Run the fermentation simulation once with all strains
    print('Running fermentation with all strains...')
    all_OD = simulate_fermentation(all_strains, random.random())

    # Randomly insert the results of the fermentation with all strains into the list of results
    contaminated_index = random.randint(0, 5)
    good_ODs.insert(contaminated_index, all_OD)

    # Plot the results
    print('Plotting results...')
    fig, ax = plt.subplots()
    for i, od in enumerate(good_ODs, start=1):
        line, = ax.plot(od, label=str(i))
        line.set_picker(5)  # Enable picking on the line with 5 pixel tolerance

    # Ask the user to identify the contaminated fermentation
    contaminated_index += 1  # Adjust index to match 1-based numbering in labels
    def onpick(event):
        if isinstance(event.artist, Line2D):
            line = event.artist
            label = line.get_label()
            if label.isdigit():
                answer = int(label)
                if answer == contaminated_index:
                    print(f'Correct! Fermentation number {contaminated_index} is contaminated.')
                else:
                    print(f'Incorrect. Fermentation number {contaminated_index} is contaminated.')

    fig.canvas.mpl_connect('pick_event', onpick)

    plt.show()

if __name__ == '__main__':
    main()