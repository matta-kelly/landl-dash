# theme.py
from dash_mantine_components import DEFAULT_THEME

# Define the custom theme object
theme = {
    "fontFamily": "'Roboto', sans-serif",
    "fontFamilyMonospace": "'Courier New', monospace",
    "primaryColor": "indigo",
    "colors": {
        "indigo": [
            "#eef2ff", "#e0e7ff", "#c7d2fe", "#a5b4fc", "#818cf8", "#6366f1", "#4f46e5", "#4338ca", "#3730a3", "#312e81"
        ],
    },
    "headings": {
        "fontFamily": "'Roboto', sans-serif",
        "sizes": {
            "h1": {"fontSize": "2.5rem", "fontWeight": 600},
            "h2": {"fontSize": "2rem", "fontWeight": 500},
        },
    },
    "shadows": {
        "sm": "0 1px 3px rgba(0, 0, 0, 0.1)",
        "md": "0 4px 6px rgba(0, 0, 0, 0.1)",
        "lg": "0 10px 15px rgba(0, 0, 0, 0.15)",
    },
    "defaultRadius": "10px",
    "spacing": {
        "xs": "8px",
        "sm": "12px",
        "md": "16px",
        "lg": "24px",
        "xl": "32px",
    },
}

# Optional: Export the default theme for fallback
default_theme = DEFAULT_THEME
