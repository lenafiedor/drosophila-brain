# drosophila-brain

## About
A simple simulation of a synaptic network of *Drosophila melanogaster* (fruit fly).<br>
Allows to:
- fetch a skeleton of a selected neuron
- link the segments with no child to their closest neighbours (`heal_skeleton.py`)
- link the synapses of a given neuron to their closest fragments (`link_synapses.py`)

## Usage

```
cd drosophila-brain
python3 main.py <bodyId>
```

The `bodyId` is the optional argument containing the ID of neuron to be healed; it can be passed through the command line. Otherwise the program will use a default, exemplary ID value.
