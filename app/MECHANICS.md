# SketchUp Mechanics and Constants

Extracted constants, formulas, and parameters from SketchUp configuration and templates:

## 1. Sandbox Defaults & Units
Source: `resources/pt-br/sandboxdefaults.ini`
- `Units`: 0.0 (Standard default)
- `StampOffset`: 12.0 inches (0.3048 m)
- `GridSpacingX`: 120.0 inches (3.048 m)
- `GridSpacingY`: 120.0 inches (3.048 m)
- `SmooveRadius`: 360.0 inches (9.144 m)

## 2. Camera & View Defaults
Source: `resources/pt-br/Templates/Temp01a - Simple.skp`
- Camera Field of View (FOV): 35.0 degrees
- Initial Camera Distance: ~8.5 meters
- Camera Orbit Center: (0.0, 0.0, 1.0)
- Horizon Line: Perspective projection with sky above and ground below
- Sky Color: `#BFE3FA` (Soft sky blue)
- Ground Color: `#D2D2D2` (Subtle warm gray)

## 3. World Coordinate System
Source: SketchUp Core Modeling Engine
- Axis X (Red): Positive = Right/Forward `[1.0, 0.0, 0.0]`, Color: `#D40000`, Negative = dotted
- Axis Y (Green): Positive = Back/Depth `[0.0, 1.0, 0.0]`, Color: `#00A600`, Negative = dotted
- Axis Z (Blue): Positive = Up `[0.0, 0.0, 1.0]`, Color: `#0000E0`, Negative = dotted

## 4. Default 2D Billboard Scale Figure
Source: `resources/pt-br/Templates/Temp01a - Simple.skp`
- Height: 1.68 m
- Position: Standing near origin `[-0.6, 0.2, 0.0]`
- Orientation: Billboard facing camera view

## 5. Command Reference
Source: `resources/pt-br/commands.json`
- `Texto 3D` (3D Text): ID `21940`
- `Alinhar a visualização` (Align View): ID `21035`
- `Oclusão ambiental` (Ambient Occlusion): ID `10600`
- `Área` (Area selection): ID `21233`
