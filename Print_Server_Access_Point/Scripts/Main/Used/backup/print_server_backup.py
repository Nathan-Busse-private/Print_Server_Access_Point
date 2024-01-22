

# The HP Smart Tank 580 - 590 series printers is able o distribute and execute 
# print jons from devices connected to the same network as the printer.
# This is achieved thanks to the printers utilizing I.P.P ( Internet Print Protocol ) 

# Why I went with Web Services on Devices (WSD) protocol, I have no clue....



# How I realized my HP Smart Tank 581 All-in-one printer utilizes I.P.P:
#-----------------------------------------------------------------------

# -It connects to our Routor and its IP and port csn be seen in the router's Gateway.
# -Any device connected to the same netwotk as the printer can access the printer.
# -A print server can be created by using a Raspberry Pi 1 model A running a custom 
#  Python script to manage and create the print server which transfers the print jobs to printer through the network.
# -The Raspberry Pi 1 model A is connected to the router via an ethernet connection.
# -The HP Smart Tank 581 All-in-one printer communicates with the Raspberry Pi 1 model A wirelessly because 
#  the printer is connected to the router's network.
# -To put it simply the Raspberry Pi 1 model A is essentialy an Access Point between 
#  devices and the printer that share the same network.

# Why I Am making this Raspberry Pi 1 model A print server:
#----------------------------------------------------------

# I can't install drivers
# for my HP Smart Tank 581 All-in-one printer as my windows installer v5.0 is malfunctioning. I know what's the problem
# and cannot be fixed without formatting the c drive completely as v5.0 has no redistributable
# file. This is just a work around. I don't want to format and install windows 7 again as there
# is a lot of sensitive data on the drive and it is nearly a 20 year old laptop. It would be
# pointless to reinstall the Windows 7 OS as vital parts of the OS such system32 begin to break
# as system files requiring important servers to function start to malfunction as the required
# servers are shutdown as time passes.

# The continuity of my printer setup on Windows should be maintained even if the Raspberry Pi
# experiences interruptions and restarts due to power loss.

# If the script is interrupted by any means it must cancel and ignore any print queues and
# cancel any active print job if the printer loses power in the middle of printing a page
# to avoid print jams and other hardware failure caused by power failure.

# IPv4 address: 192.168.0.102
# Hostname: printserver
# ping -c 4 printserver


# Packages
#----------

import cups
import socket
import threading
import time
import os
import pickle

class PrintServer:
    def __init__(self, printer_name):
        self.printer_name = printer_name
        self.job_queue_file = "print_job_queue.pkl"
        self.conn = cups.Connection()

    def check_printer_status(self):
        try:
            status = self.conn.getPrinterAttributes(self.printer_name)['printer-state']
            return status
        except Exception as e:
            print(f"Error checking printer status: {e}")
            return None

    def print_document(self, document_content):
        try:
            job_title = 'PrintJob'
            options = {'media': 'A4', 'fit-to-page': True}
            response = self.conn.printFile(self.printer_name, document_content, job_title, options)
            job_id = response.split()[1]
            print(f"Print job submitted successfully. Job ID: {job_id}")
            return job_id
        except Exception as e:
            print(f"Error printing document: {e}")
            return None

    def cancel_print_job(self, job_id):
        try:
            self.conn.cancelJob(int(job_id), purge=True)
            print(f"Print job {job_id} canceled successfully.")
        except Exception as e:
            print(f"Error canceling print job: {e}")

    def save_to_queue(self, job):
        try:
            with open(self.job_queue_file, 'ab') as f:
                pickle.dump(job, f)
            print("Print job saved to the queue.")
        except Exception as e:
            print(f"Error saving print job to queue: {e}")

    def load_from_queue(self):
        jobs = []
        try:
            with open(self.job_queue_file, 'rb') as f:
                while True:
                    try:
                        job = pickle.load(f)
                        jobs.append(job)
                    except EOFError:
                        break
            print("Print jobs loaded from the queue.")
        except Exception as e:
            print(f"Error loading print jobs from queue: {e}")
        return jobs

    def clear_queue(self):
        try:
            os.remove(self.job_queue_file)
            print("Print job queue cleared.")
        except FileNotFoundError:
            print("Print job queue not found.")
        except Exception as e:
            print(f"Error clearing print job queue: {e}")

def client_handler(client_socket, server):
    try:
        document_content = client_socket.recv(4096)  # Adjust buffer size based on your needs
        if not document_content:
            return  # No more data, connection closed

        # Check printer status and submit print job
        printer_status = server.check_printer_status()
        if printer_status == 'idle':
            job_id = server.print_document(document_content)

            if job_id is not None:
                # Simulate a print job by waiting for 10 seconds
                time.sleep(10)

                # Cancel the print job (this is just an example, you can remove it if not needed)
                server.cancel_print_job(job_id)
        else:
            print(f"Printer is not idle. Current status: {printer_status}")
            # Save the print job to the queue for later processing
            server.save_to_queue({
                'document_content': document_content,
                'timestamp': time.time()
            })

    finally:
        client_socket.close()

def check_and_resume_jobs(server):
    jobs = server.load_from_queue()
    for job in jobs:
        # Check if the printer is idle before attempting to print
        printer_status = server.check_printer_status()
        if printer_status == 'idle':
            document_content = job['document_content']
            job_id = server.print_document(document_content)

            if job_id is not None:
                # Simulate a print job by waiting for 10 seconds
                time.sleep(10)

                # Cancel the print job (this is just an example, you can remove it if not needed)
                server.cancel_print_job(job_id)

def main():
    printer_name = "HP_Smart_Tank_580-590_series_"  # Replace with your printer's name
    server = PrintServer(printer_name)

    # Check and resume any interrupted print jobs from the queue on startup
    check_and_resume_jobs(server)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Bind to any available network interface on port 12345
    server_socket.listen(1)

    print("Server is listening for incoming print job requests...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Start a new thread to handle the client
        threading.Thread(target=client_handler, args=(client_socket, server)).start()

if __name__ == "__main__":
    main()
