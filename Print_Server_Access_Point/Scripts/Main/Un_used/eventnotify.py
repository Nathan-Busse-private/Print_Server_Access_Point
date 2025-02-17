import ipp
import socket
import threading
import time
import os
import pickle
# from plyer import notification


class PrintServer:
    def __init__(self, printer_ip, printer_port=9211):
        self.printer_uri = f'http://{printer_ip}:{printer_port}/ipp/print'
        self.printer = ipp.Printer(self.printer_uri)
        self.job_queue_file = "print_job_queue.pkl"

    def check_printer_status(self):
        try:
            status = self.printer.get_printer_attributes()['printer-state']
            return status
        except Exception as e:
            print(f"Error checking printer status: {e}")
            return None

    def print_document(self, document_content):
        try:
            job_attributes = {
                'job-name': 'PrintJob',
                'document-format': 'application/octet-stream'
            }
            response = self.printer.print_job(document_content, job_attributes)
            job_id = response.get('job-id')
            print(f"Print job submitted successfully. Job ID: {job_id}")
            
            # Send notification to client (commented out for now)
            # self.send_notification("Print Job Submitted", f"Print job submitted successfully. Job ID: {job_id}")
            
            return job_id
        except Exception as e:
            print(f"Error printing document: {e}")
            # Send error notification to client (commented out for now)
            # self.send_notification("Print Job Error", f"Error printing document: {e}")
            return None

    def cancel_print_job(self, job_id):
        try:
            self.printer.cancel_job(job_id)
            print(f"Print job {job_id} canceled successfully.")
            
            # Send notification to client (commented out for now)
            # self.send_notification("Print Job Canceled", f"Print job {job_id} canceled successfully.")
        except Exception as e:
            print(f"Error canceling print job: {e}")
            # Send error notification to client (commented out for now)
            # self.send_notification("Cancel Job Error", f"Error canceling print job: {e}")

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
    printer_ip = "192.168.0.102"  # Replace with your printer's IP address
    server = PrintServer(printer_ip)

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
