import csv
import random
from fermentation import simulate_fermentation
from visualisation import plot_total_OD
from fermentation import Strain
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
        ax.plot(od, label=str(i))
    ax.legend()

    # Ask the user to identify the contaminated fermentation
    contaminated_index += 1  # Adjust index to match 1-based numbering in labels
    def onclick(event):
        if event.inaxes is not None:
            answer = int(event.inaxes.get_title())
            if answer == contaminated_index:
                print(f'Correct! Fermentation number {contaminated_index} is contaminated.')
            else:
                print(f'Incorrect. Fermentation number {contaminated_index} is contaminated.')

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

if __name__ == '__main__':
    main()