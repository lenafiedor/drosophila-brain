# drosophila-brain

## About
A simple simulation of a synaptic network of *Drosophila melanogaster* (fruit fly).  
Allows to:
- fetch a skeleton of a selected neuron
- link the segments with no child to their closest neighbours (`heal_skeleton.py`)
- link the synapses of a given neuron to their closest fragments (`link_synapses.py`)
- link synapses to a new point, determined by the intersection of the line connecting two nearest segments and the straight line tangent to it, passing through the given synapse (`link_synapses_upgraded.py`)

## Requirements
* Python 3.10 or newer
* Poetry

## Usage

### Install Requirements

```bash
cd drosophila-brain
python3 - m venv ./.drosophila-brain
source ./.drosophila-brain/bin/activate
poetry install
```

### Run the Healing Script

```bash
python3 src/main.py <bodyId>
```

The `bodyId` is the optional argument containing the ID of neuron to be healed; it can be passed through the command line. Otherwise the program will use a default, exemplary ID value.
