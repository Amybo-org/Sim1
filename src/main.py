from fermentation import simulate_fermentation
from visualisation import plot_total_OD
from strains import GoodStrain, PathogenicStrain

def main():
    # Define the strains
    good_strains = [GoodStrain() for _ in range(5)]
    all_strains = good_strains + [PathogenicStrain()]

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