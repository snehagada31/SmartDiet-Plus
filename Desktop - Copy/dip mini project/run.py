# run.py

from cartoonizer import cartoonize_image
import matplotlib.pyplot as plt

# Path to your image
img_path = "small.jpg"

# Cartoonize
original, cartoon = cartoonize_image(img_path)

# Show the results
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(original)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(cartoon)
plt.title("Cartoonized Image")
plt.axis("off")

plt.tight_layout()
plt.show()
