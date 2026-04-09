# This file is for loading the trained model and printing out the names of the layers (or "rooms" in the brain).

"""import torch

# Load the file
model_data = torch.load("human_detector.pth", map_location="cpu")

# This shows the names of every "room" (layer) inside the brain
print(model_data.keys())
"""

# Visualizing the "Inside" (Filters) of the "Brain" (Model)
"""
import torch
import matplotlib.pyplot as plt
import numpy as np

# 1. Load the data
model_data = torch.load("human_detector.pth", map_location="cpu")

# 2. Access the first layer (conv1.weight) mentioned in your file snippet
# This layer usually contains the initial 'filters'
weights = model_data["conv1.weight"]


# 3. Prepare the data for a 2D view
# We'll take the first 64 filters and arrange them in a grid
# Weights shape is usually [out_channels, in_channels, kernel_height, kernel_width]
# We'll simplify this to a 2D grid for visualization
def visualize_weights(tensor, num_cols=8):
    num_kernels = tensor.shape[0]
    num_rows = 1 + num_kernels // num_cols
    fig = plt.figure(figsize=(num_cols, num_rows))

    for i in range(num_kernels):
        ax1 = fig.add_subplot(num_rows, num_cols, i + 1)
        # Normalize weights to 0-1 range for display
        w = tensor[i][0].numpy()
        w = (w - w.min()) / (w.max() - w.min())
        ax1.imshow(w, cmap="gray")
        ax1.axis("off")
        ax1.set_xticklabels([])
        ax1.set_yticklabels([])

    plt.tight_layout()
    plt.show()
    # 4. Save the image
    fig.savefig("model_internal_weights.png")
    print(
        "The 2D view of the model's internal filters has been saved as 'model_internal_weights.png'"
    )


visualize_weights(weights)
"""

# Seeing the Architecture (2D Flowchart)
# To see the 2D map of the layers themselves:
"""
from torchview import draw_graph
import torchvision.models as models

# Assuming your file is a ResNet based on the 'layer1.0' names in your snippet
model = models.resnet18()
model_graph = draw_graph(model, input_size=(1, 3, 224, 224), expand_nested=True)
model_graph.visual_graph.render("model_architecture_map", format="png")

"""
# pip install torchview graphviz
# To see the 2D map of the layers themselves:
"""
import torch
import torchvision.models as models
from torchview import draw_graph
import os

# 1. Setup the model structure (ResNet18 matches your file snippet)
model = models.resnet18()

# 2. Try to load your specific file weights into the model
try:
    state_dict = torch.load("human_detector.pth", map_location="cpu")
    model.load_state_dict(state_dict)
    print("Successfully loaded weights from human_detector.pth")
except Exception as e:
    print(
        f"Note: Could not load specific weights, showing generic architecture. Error: {e}"
    )

# 3. Create the 2D Flowchart
# We ensure the 'bin' path is recognized if Graphviz was just installed
os.environ["PATH"] += os.pathsep + "C:/Program Files/Graphviz/bin"

try:
    model_graph = draw_graph(model, input_size=(1, 3, 224, 224), expand_nested=True)
    model_graph.visual_graph.render("model_architecture_map", format="png")
    print("Success! The 2D flowchart has been saved as 'model_architecture_map.png'")
except Exception as e:
    print(
        f"Failed to render image. Ensure Graphviz is installed on your Windows OS. Error: {e}"
    )
"""
# This final version combines loading the model, attempting to apply the weights, and visualizing the architecture in one script. It also includes error handling for both loading weights and rendering the graph, which should help you troubleshoot any issues that arise during these steps.

import os
import torch
import torchvision.models as models
from torchview import draw_graph

# This tells Python exactly where the 'dot.exe' lives if the PATH failed
# Adjust the version number if you installed a different one
graphviz_path = r"C:\Program Files\Graphviz\bin"
os.environ["PATH"] += os.pathsep + graphviz_path

# Load your human detector model
model = models.resnet18()

try:
    # Generate the 2D diagram
    model_graph = draw_graph(model, input_size=(1, 3, 224, 224), expand_nested=True)
    model_graph.visual_graph.render("human_detector_map", format="png")
    print("Success! Open 'human_detector_map.png' to see your model inside.")
except Exception as e:
    print(f"Error: {e}")
