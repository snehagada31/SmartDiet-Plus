# cartoonizer.py

import cv2
import numpy as np
import matplotlib.pyplot as plt


def load_image(path, size=(800, 800)):
    img = cv2.imread(path)
    img = cv2.resize(img, size)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb


def apply_bilateral_filter(img):
    return cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)


def color_quantization(img, k=8):
    img_data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(
        img_data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    quantized = centers[labels.flatten()].reshape(img.shape)
    return quantized


def detect_edges(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blurred = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(blurred, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 10)
    return edges


def combine_effects(color_img, edges):
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    cartoon = cv2.bitwise_and(color_img, edges_colored)
    return cartoon


def cartoonize_image(image_path):
    original = load_image(image_path)
    smoothed = apply_bilateral_filter(original)
    quantized = color_quantization(smoothed)
    edges = detect_edges(original)
    cartoon = combine_effects(quantized, edges)

    return original, cartoon
