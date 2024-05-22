import pandas as pd

import matplotlib.pyplot as plt

from tqdm.auto import tqdm



def read_data(file_path):

    data = pd.read_csv(file_path)

    data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%H:%M:%S.%f')

    return data



def compute_metrics(data, freq='S'):

    data.set_index('Timestamp', inplace=True)



    # Start counting the timestamp from 0

    data.index = data.index - data.index[0]

    throughput = data['Packet Size'].resample(freq).sum()  # Sum of packet sizes

    packet_counts = data['Packet Size'].resample(freq).count()  # Count of packets

    return throughput, packet_counts



def plot_metrics(throughput, packet_counts, freq, fontsize):

    fig, ax1 = plt.subplots(figsize=(12, 6))



    color = 'tab:red'

    ax1.set_xlabel('Tempo (segundos)', fontsize=fontsize, fontweight='bold')

    ax1.set_ylabel('Vazão (MB)', color=color, fontsize=fontsize, fontweight='bold')



    # Plot x axis as time

    ax1.plot(throughput.index/1000000000, throughput.values/(2**20), color=color)

    ax1.tick_params(axis='y', labelcolor=color)



    ax2 = ax1.twinx()  

    color = 'tab:blue'

    ax2.set_ylabel('Número de Pacotes', color=color, fontsize=fontsize, fontweight='bold')

    ax2.plot(packet_counts.index/1000000000, packet_counts.values, color=color)

    ax2.tick_params(axis='y', labelcolor=color)



    # Avoid using scientific notation

    ax1.get_xaxis().get_major_formatter().set_scientific(False)

    ax1.get_yaxis().get_major_formatter().set_scientific(False)

    ax2.get_yaxis().get_major_formatter().set_scientific(False)



    # Set font size

    ax1.tick_params(axis='both', which='major', labelsize=fontsize)

    ax2.tick_params(axis='both', which='major', labelsize=fontsize)



    plt.show()



def main():



    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--input_file', dest='input_file', required=True)

    parser.add_argument('-s', '--fontsize', dest='fontsize', type=int, default=12, help='Font size for the plot')

    args = parser.parse_args()



    file_path = args.input_file

    # freq_options = {'S': 'Second', 'T': 'Minute', 'H': 'Hour', 'D': 'Day', 'M': 'Month', 'Y': 'Year'}

    freq_options = {'S': 'Second'}

    

    data = read_data(file_path)

    

    for freq, label in tqdm(freq_options.items(), desc="Computing and plotting metrics"):

        throughput, packet_counts = compute_metrics(data, freq=freq)

        plot_metrics(throughput, packet_counts, label, args.fontsize)



if __name__ == '__main__':

    main()