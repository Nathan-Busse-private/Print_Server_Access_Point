import cups
import socket
import threading
import time
import os
import pickle
from zeroconf import ServiceInfo, Zeroconf
from smb.SMBHandler import SMBHandler  # Import SMBHandler for Samba integration

class PrintServer:
    def __init__(self, printer_queue_name, port):
        self.printer_queue_name = printer_queue_name
        self.port = port
        self.job_queue_file = "print_job_queue.pkl"
        self.conn = cups.Connection()

        # Zeroconf initialization
        self.zeroconf = Zeroconf()
        self.service_info = ServiceInfo(
            "_ipp._tcp.local.",
            f"{printer_queue_name}._ipp._tcp.local.",
            socket.inet_aton(socket.gethostbyname(socket.gethostname())),
            port,
            properties={"txtvers": "1", "rp": "printers/printqueue"},
        )
        self.zeroconf.register_service(self.service_info)

        # Samba initialization
        self.samba_handler = SMBHandler(printer_queue_name)

    def check_printer_status(self):
        try:
            status = self.conn.getPrinterAttributes(self.printer_queue_name)['printer-state']
            return status
        except Exception as e:
            print(f"Error checking printer status: {e}")
            return None

    def print_document(self, document_content):
        try:
            job_title = 'PrintJob'
            options = {'media': 'A4', 'fit-to-page': True}
            response = self.conn.printFile(self.printer_queue_name, document_content, job_title, options)
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

    def __del__(self):
        # Unregister Zeroconf service on object deletion
        self.zeroconf.unregister_service(self.service_info)
        self.zeroconf.close()

def client_handler(client_socket, server):
    try:
        document_content = client_socket.recv(4096)  # Adjust buffer size based on your needs
        if not document_content:
            return  # No more data, connection closed

        printer_status = server.check_printer_status()
        if printer_status == 'idle':
            job_id = server.print_document(document_content)

            if job_id is not None:
                # Simulate a print job by waiting for 10 seconds
                time.sleep(10)
                server.cancel_print_job(job_id)
        else:
            print(f"Printer is not idle. Current status: {printer_status}")
            server.save_to_queue({
                'document_content': document_content,
                'timestamp': time.time()
            })

    finally:
        client_socket.close()

def check_and_resume_jobs(server):
    jobs = server.load_from_queue()
    for job in jobs:
        printer_status = server.check_printer_status()
        if printer_status == 'idle':
            document_content = job['document_content']
            job_id = server.print_document(document_content)

            if job_id is not None:
                # Simulate a print job by waiting for 10 seconds
                time.sleep(10)
                server.cancel_print_job(job_id)

def main():
    printer_queue_name = "HP_Smart_Tank_580-590_series"
    port = 12345

    server = PrintServer(printer_queue_name, port)

    check_and_resume_jobs(server)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)

    print("Server is listening for incoming print job requests...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        threading.Thread(target=client_handler, args=(client_socket, server)).start()

if __name__ == "__main__":
    main()
