import csv
import matplotlib.pyplot as plt

def plot_total_OD(file_path):
    # Read the total OD from the file
    total_OD = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            total_OD.append(float(row[0]))

    # Plot the total OD over time
    plt.plot(total_OD)
    plt.xlabel('Time period')
    plt.ylabel('Total OD')
    plt.title('Total OD over time')
    plt.show()

def main():
    print('Plotting total OD...')
    plot_total_OD('data/total_OD.csv')
    print('Plotting complete')

if __name__ == '__main__':
    main()