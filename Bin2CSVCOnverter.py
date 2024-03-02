from logging import basicConfig, DEBUG, INFO, WARNING, ERROR, getLogger
from csv import DictWriter
from struct import unpack_from

# Configure logging for easier debugging
# log_level = DEBUG
log_level = INFO
# log_level = WARNING
basicConfig(format='{asctime}: {message}', datefmt="%H:%M:%S", style='{', level=log_level)
logger = getLogger(__name__)

# File paths for input and output
input_file = 'FPREIS_D381.BIN'
output_file = 'PRIJSXXX.csv'

# Unknown flags to be logged
unmatched_flags = set()

try:
    # Open the binary file for reading and the CSV file for writing
    with open(input_file, 'rb') as binary_file, open(output_file, 'w', newline='') as csv_file:
        csv_writer = DictWriter(csv_file, fieldnames=('name', 'discount', 'price'), delimiter=';')
        csv_writer.writeheader()
        binary_data = binary_file.read()

        # Initialize the current offset in the binary data
        current_offset = 0

        # Known flags for the records
        known_flags = [61441, 45057, 46081, 40961]

        # Loop through the binary data until the end
        while current_offset < len(binary_data):
            try:
                record_length, record_flag = unpack_from('<HH', binary_data, current_offset)  # Extract record header (length and flags)
                name_length = binary_data[current_offset + 4]  # Extract the length of the name field from the record

                # Debug logging for the current record's raw data
                logger.debug(binary_data[current_offset:current_offset + record_length + 2])

                if record_flag in known_flags:
                    # Discount and price in known location
                    if hex(record_flag) == '0xf001':
                        unpack_format = '<4xx{}s4x'.format(name_length)
                        if record_flag & 0x2000:  # Check if the price field is present in the record
                            unpack_format += 'I'  # Add format specifier for price if present
                        unpack_format += '2s'  # Format specifier for the discount field

                    # Discount and price in different locations
                    elif hex(record_flag) == '0xb001' or hex(record_flag == '0xb401'):
                        unpack_format = '<4xx{}sI2s'.format(name_length)

                    # Discount not present
                    elif hex(record_flag) == '0xa001':
                        if record_flag & 0x2000:
                            unpack_format = '<4xx{}sI2s'.format(name_length)
                        else:
                            unpack_format = '<4xx{}s4x2s'.format(name_length)

                    logger.debug('unpack_format: ' + unpack_format)

                    # Unpack the current record according to the constructed format
                    record_data = unpack_from(unpack_format, binary_data, current_offset)

                    logger.debug('record_data: {}'.format(record_data))

                    # Name field is the first element of the unpacked record data
                    cleaned_name = record_data[0].decode(errors='replace')

                    # Clean the discount field by removing newline characters and decoding
                    cleaned_discount = record_data[-1].decode(errors='ignore').replace('\n', '').replace('\r', '').replace(' ', '')

                    # Format the price field to two decimal places
                    price_formatted = "{:.2f}".format(record_data[1] / 100)

                    # Prepare the output record for the CSV
                    record_output = {'name': cleaned_name,
                                     'discount': cleaned_discount,
                                     'price': price_formatted}

                    logger.info('record_flag: {:x}: {}'.format(record_flag, record_output))

                    # Write the processed record to the CSV file
                    csv_writer.writerow(record_output)

                    logger.debug('Current offset: {}, Total length: {}'.format(current_offset, len(binary_data)))

                else:
                    # Add the unmatched flag to the list
                    unmatched_flags.add(record_flag)

                    logger.info('Unmatched flags: {}'.format(unmatched_flags))

                # Move to the next record in the binary data
                current_offset += (record_length + 2)

            except Exception as e:
                logger.error(f"Unexpected error processing record at offset {current_offset}: {e}")
                continue

except FileNotFoundError:
    logger.critical(f"File {input_file} not found.")
except PermissionError:
    logger.critical(f"Permission denied when accessing {input_file} or {output_file}.")
except Exception as e:
    logger.critical(f"An unexpected error occurred: {e}")
finally:
    if unmatched_flags:
        logger.info(f'All unmatched flags: {unmatched_flags}')
