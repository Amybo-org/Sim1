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
    # Plot the total OD
    print('Sorry, this test was broken.')

if __name__ == '__main__':
    main()