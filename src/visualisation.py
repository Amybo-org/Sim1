import csv
import matplotlib.pyplot as plt

def plot_total_OD(OD_values, labels):
    # Plot each set of OD values in a different color
    for OD, label in zip(OD_values, labels):
        plt.plot(OD, label=label)

    # Add labels and a legend
    plt.xlabel('Time period')
    plt.ylabel('Total OD')
    plt.title('Total OD over time')
    plt.legend()

    # Show the plot
    plt.show()

def main():
    print('Plotting total OD...')
    plot_total_OD('data/total_OD.csv')
    print('Plotting complete')

if __name__ == '__main__':
    main()