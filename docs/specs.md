# Some Logo - Specifications

## Overview

`some_logo` is a Python application that generates stylized SVG logos from a given text input. The application maps characters in the text to geometric shapes and generates colors based on the ASCII values of the characters.

## Features & Requirements

### 1. Basic Generation

- **Input**: A text string from the user (e.g., "stop").
- **Output**: An SVG file containing geometric shapes that visually represent the provided text.

### 2. Geometry Modes

The application supports different geometric modes for representing each letter in the input string:

- **Square Mode**:
  - Represents each letter as a square.
  - The sequence of squares is aligned sequentially.
- **Circle Mode**:
  - Represents each letter as a circle instead of a square.
  - The inner circles are placed inside a larger, encompassing outer circle boundary.

### 3. Coloring Generation

- Each geometric shape gets a specific fill color.
- The color is derived from the **ASCII code** of the character it represents, transformed into an RGB value.

### 4. Optional Decorators & Overlays

- **Squared Frame**: The user can optionally select to enclose the generated sequence of inner shapes with a squared frame.
- **Inner Letter Inclusion**: The user has the option to render the actual letter character, adding the text inside its corresponding square or circle.

## Example Scenario

- **Input text**: `"stop"`
- **Selected options**: Square Mode, Squared Frame enabled, Letter inclusion enabled.
- **Result**: Generates an SVG with a main outer square frame, containing four inner squares. The colors of the four squares are synthesized from the ASCII values of 's', 't', 'o', and 'p'. Inside each colored square, the characters 's', 't', 'o', and 'p' are rendered.
