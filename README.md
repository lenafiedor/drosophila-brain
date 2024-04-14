# drosophila-brain

## About
A simple simulation of a synaptic network of *Drosophila melanogaster* (fruit fly).
Allows to fetch a skeleton of a selected neuron and link the segments with no child to its closest neighbours.

## Usage

```
cd drosophila-brain
python3 main.py <bodyId>
```

The `bodyId` is the ID of neuron to be healed; it can be passed through the command line. Otherwise the program will use a default value.
