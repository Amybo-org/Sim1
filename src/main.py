import csv
import random
from fermentation import simulate_fermentation
from visualisation import plot_total_OD
from fermentation import Strain

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
    initial_biomass = 0.1
    good_ODs = [simulate_fermentation(good_strains, initial_biomass) for _ in range(5)]

    # Run the fermentation simulation once with all strains
    print('Running fermentation with all strains...')
    all_OD = simulate_fermentation(all_strains, initial_biomass)

    # Randomly insert the results of the fermentation with all strains into the list of results
    contaminated_index = random.randint(0, 5)
    good_ODs.insert(contaminated_index, all_OD)

    # Plot the results
    print('Plotting results...')
    plot_total_OD(good_ODs, [str(i+1) for i in range(6)])

    # Ask the user to identify the contaminated fermentation
    print('Please identify the contaminated fermentation:')
    answer = input('Enter the number of the contaminated fermentation: ')
    if answer == str(contaminated_index + 1):
        print(f'Correct! Fermentation number {contaminated_index + 1} is contaminated.')
    else:
        print(f'Incorrect. Fermentation number {contaminated_index + 1} is contaminated.')

if __name__ == '__main__':
    main()