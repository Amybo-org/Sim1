import csv
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

    # Run the fermentation simulation with just the good strains
    print('Running fermentation with good strains...')
    good_OD = simulate_fermentation(good_strains)

    # Run the fermentation simulation with all strains
    print('Running fermentation with all strains...')
    all_OD = simulate_fermentation(all_strains)

    # Plot the results
    print('Plotting results...')
    plot_total_OD([good_OD, all_OD], ['Good Strains', 'All Strains'])

    # Ask the user to identify the contaminated fermentation
    print('Please identify the contaminated fermentation:')
    print('1: Good Strains')
    print('2: All Strains')
    answer = input('Enter the number of the contaminated fermentation: ')
    if answer == '2':
        print('Correct! The fermentation with all strains is contaminated.')
    else:
        print('Incorrect. The fermentation with all strains is contaminated.')

if __name__ == '__main__':
    main()