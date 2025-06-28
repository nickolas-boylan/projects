##########################################################################
# treatment_file_consumer.py
#
# Defines a consumer function (treatment_file_consumer) that continuously reads
# treatments from a queue (TreatmentFileQueue) and writes them to a CSV file.
# This implementation uses a StringIO object instead of a file to avoid
# issues with concurrently writing to a physical file in memory. This function
# writes the header row and then appends each treatment to the StringIO
#
# The producers are responsible for adding the treatments into the treatment
# queue. Then this thread will grab the treatments out of that queue. To finish
# this thread, the treatment queue must be signaled that the producers are done
#
##########################################################################

import logging
import csv
import io

def file_consumer(next_treatment_queue):
    """
    Continouously fetch treatments from next_treatment_queue and write them
    to path_of_file in CSV format.

    Arguments:
        next_treatment_queue: A TreatmentFileQueue providing treatments and
                              their corresponding information
    
    Notes:
        - This pattern allows threads to insert items into the queue, while the
          consumer writes rows in near-real-time.
        - The function itself doesn't return anything but will use one of the
          TreatmentFileQueue's functions to set the final data
    """
    # Write the CSV header row once
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Company","Treatment_Name", "Therapeutic_Area", 
                     "Indication", "Phase"])

    # Continuously fetch treatments and append them to the CSV file
    while True:
        next_treatment = next_treatment_queue.grab_next_treatment()
        if next_treatment is None:
            break

        next_treatment_row = [
            next_treatment.get("company", "N/A"),
            next_treatment.get("treatment_name", "N/A"),
            next_treatment.get("therapeutic_area", "N/A"),
            next_treatment.get("indication", "N/A"),
            next_treatment.get("phase", "N/A")
        ]
        
        writer.writerow(next_treatment_row)

    csv_data = output.getvalue()
    output.close()
    next_treatment_queue.set_final(csv_data)
    logging.info(f"Treatment File Consumer has finished")