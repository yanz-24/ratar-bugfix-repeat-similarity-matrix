"""
core.py

Read-across the targetome -
An integrated structure- and ligand-based workbench for computational target prediction and novel tool compound design

Handles the CLI functions for processing the encoding of multiple binding sites.
"""

import argparse
import datetime
import logging
import logging.config
from pathlib import Path

from .auxiliary import create_directory
from .encoding import process_encoding


def parse_arguments():
    """
    Parse the arguments given when calling this script.

    Returns
    -------
    Tuple of str
        Input molecule structure file path and output directory.
    """

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_mol_path', help='Path to molecule structure file(s).', required=True)
    parser.add_argument('-o', '--output_dir', help='Path to output directory.', required=True)

    # Set as variables
    args = parser.parse_args()
    input_mol_path = args.input_mol_path
    output_dir = args.output_dir

    return input_mol_path, output_dir


def main():
    """
    Main ratar function to process one or multiple binding sites.
    """

    # Get start time of script
    encoding_start = datetime.datetime.now()

    # Parse arguments
    input_mol_path, output_dir = parse_arguments()

    # Create output folder
    create_directory(output_dir)

    # Create custom logger
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)

    # Create handlers
    f_handler = logging.FileHandler(Path(output_dir) / 'ratar.log', mode='w')

    # Add handler to logger
    logger.addHandler(f_handler)

    # Log IO
    logger.info('IO...')
    logger.info(f'Input: {input_mol_path}')
    logger.info(f'Output: {output_dir}')

    # Process encoding
    logger.info(f'PROCESS ENCODING...')
    process_encoding(input_mol_path, output_dir, logger)

    # Get end time of encoding step and runtime
    encoding_end = datetime.datetime.now()
    encoding_runtime = encoding_end - encoding_start

    # Log runtime
    logger.info(f'RUNTIME')
    logger.info(f'Encoding step: {encoding_runtime}')


if __name__ == '__main__':
    main()
