import onnx
import numpy as np
import argparse
import os
from pathlib import Path


def parse():
    parser = argparse.ArgumentParser(
        prog="convconst",
        description="Extract constants from convolutional neural networks.")
    parser.add_argument("model", help="the onnx model file")
    parser.add_argument("dest", help="destination directory")
    return parser.parse_args()


def extract_conv_weights(model):
    input = [node.input[1]
             for node in model.graph.node if node.op_type == "Conv"]

    conv_initializer = [
        init for init in model.graph.initializer if init.name in input]

    conv_initializer = sorted(
        conv_initializer, key=lambda init: input.index(init.name))

    weight = [onnx.numpy_helper.to_array(init) for init in conv_initializer]

    return weight


def main():
    args = parse()
    model = onnx.load(args.model)
    weight = extract_conv_weights(model)
    dest = Path(args.dest)
    os.makedirs(dest, exist_ok=True)
    for w in weight:
        file = dest / ("x".join(str(d) for d in w.shape) + ".npy")
        np.save(file, w)
