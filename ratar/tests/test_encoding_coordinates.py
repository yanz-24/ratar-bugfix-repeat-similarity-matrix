"""
Unit and regression test for the Coordinates class in the ratar.encoding module of the ratar package.
"""

import sys

import pytest
from pathlib import Path

from ratar.auxiliary import MoleculeLoader
from ratar.encoding import Coordinates


@pytest.mark.parametrize('filename, column_names, n_atoms, centroid', [
    (
        'AAK1_4wsq_altA_chainA_reduced.mol2',
        'x y z'.split(),
        dict(
            zip(
                'ca pca pc'.split(),
                [8, 34, 29]
            )
        ),
        dict(
            zip(
                'ca pca pc'.split(),
                [
                    [6.2681, 11.9717, 42.4514],
                    [5.6836, 12.9039, 43.9326],
                    [5.8840, 12.5871, 43.3804]
                ]
            )
        )

    )
])
def test_get_coordinates(filename, column_names, n_atoms, centroid):
    """
    Test if coordinates are correctly extracted from representatives of a molecule.

    Parameters
    ----------
    filename : str
        Name of molecule file.
    column_names : list of str
        List of molecule DataFrame columns.
    n_atoms : dict of int
        Number of atoms for each representatives type.
    centroid : dict of list of float
        3D coordinates of molecule centroid for each representatives type.
    """

    # Load molecule
    molecule_path = Path(sys.path[0]) / 'ratar' / 'tests' / 'data' / filename
    molecule_loader = MoleculeLoader()
    molecule_loader.load_molecule(molecule_path)
    pmol = molecule_loader.get_first_molecule()

    # Set coordinates
    coordinates = Coordinates()
    coordinates.get_coordinates_from_pmol(pmol)

    for key, value in coordinates.data.items():
        assert all(value.columns == column_names)
        assert value.shape[0] == n_atoms[key]
        assert abs(value['x'].mean() - centroid[key][0]) < 0.0001
        assert abs(value['y'].mean() - centroid[key][1]) < 0.0001
        assert abs(value['z'].mean() - centroid[key][2]) < 0.0001
