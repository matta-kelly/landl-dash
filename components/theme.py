from dash_mantine_components import DEFAULT_THEME

# Define the custom theme object
theme = {
    **DEFAULT_THEME,
    "fontFamily": "'Roboto', sans-serif",
    "fontFamilyMonospace": "'Courier New', monospace",
    "primaryColor": "indigo",
    "colors": {
        "indigo": [
            "#eef2ff", "#e0e7ff", "#c7d2fe", "#a5b4fc", "#818cf8", "#6366f1", "#4f46e5", "#4338ca", "#3730a3", "#312e81",
        ],
        "blue": [
            "#eff6ff", "#dbeafe", "#bfdbfe", "#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8", "#1e40af", "#1e3a8a",
        ],
        "green": [
            "#f0fdf4", "#dcfce7", "#bbf7d0", "#86efac", "#4ade80", "#22c55e", "#16a34a", "#15803d", "#166534", "#14532d",
        ],
        "red": [
            "#fef2f2", "#fee2e2", "#fecaca", "#fca5a5", "#f87171", "#ef4444", "#dc2626", "#b91c1c", "#991b1b", "#7f1d1d",
        ],
    },
    "headings": {
        "fontFamily": "'Roboto', sans-serif",
        "sizes": {
            "h1": {"fontSize": "3rem", "fontWeight": 700, "lineHeight": 1.2},
            "h2": {"fontSize": "2.25rem", "fontWeight": 600, "lineHeight": 1.3},
            "h3": {"fontSize": "1.875rem", "fontWeight": 500, "lineHeight": 1.4},
            "h4": {"fontSize": "1.5rem", "fontWeight": 500, "lineHeight": 1.5},
            "h5": {"fontSize": "1.25rem", "fontWeight": 500, "lineHeight": 1.6},
            "h6": {"fontSize": "1rem", "fontWeight": 500, "lineHeight": 1.7},
        },
    },
    "shadows": {
        "sm": "0 1px 3px rgba(0, 0, 0, 0.1)",
        "md": "0 4px 6px rgba(0, 0, 0, 0.1)",
        "lg": "0 10px 15px rgba(0, 0, 0, 0.15)",
        "xl": "0 20px 25px rgba(0, 0, 0, 0.25)",
    },
    "defaultRadius": "10px",
    "spacing": {
        "xs": "8px",
        "sm": "12px",
        "md": "16px",
        "lg": "24px",
        "xl": "32px",
    },
    "buttons": {
        "default": {
            "backgroundColor": "var(--indigo-5)",
            "color": "white",
            "border": "none",
            "padding": "10px 20px",
            "borderRadius": "5px",
            "fontWeight": 500,
            "hover": {
                "backgroundColor": "var(--indigo-6)",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.2)",
            },
        },
        "outline": {
            "backgroundColor": "transparent",
            "border": "2px solid var(--indigo-5)",
            "color": "var(--indigo-5)",
            "hover": {
                "backgroundColor": "var(--indigo-0)",
                "borderColor": "var(--indigo-6)",
            },
        },
    },
    "dark": {
        "primaryColor": "indigo",
        "backgroundColor": "#1a202c",
        "colorScheme": "dark",
        "fontFamily": "'Roboto', sans-serif",
        "colors": {
            "background": "#2d3748",
            "text": "#e2e8f0",
            "indigo": [
                "#c3dafe", "#a3bffa", "#7f9cf5", "#667eea", "#5a67d8", "#4c51bf", "#434190", "#3c366b", "#2a2f58", "#1a202c",
            ],
        },
    },
    "styles": {
        "body": {
            "margin": 0,
            "padding": 0,
            "boxSizing": "border-box",
            "backgroundColor": "var(--background)",
            "color": "var(--text)",
            "fontFamily": "'Roboto', sans-serif",
        },
        "a": {
            "color": "var(--indigo-5)",
            "textDecoration": "none",
            "hover": {"textDecoration": "underline"},
        },
        "table": {
        "width": "100%",
        "borderCollapse": "collapse",
        "margin": "20px auto",
        "border": "1px solid #dee2e6",
        },
        "th": {
            "textAlign": "center",
            "padding": "10px",
            "fontSize": "16px",
            "borderBottom": "2px solid #dee2e6",
            "backgroundColor": "#f8f9fa",
        },
        "td": {
            "textAlign": "center",
            "padding": "10px",
            "fontSize": "14px",
            "borderBottom": "1px solid #dee2e6",
        },
        "tr": {
            "borderBottom": "1px solid #dee2e6",
            "hover": {"backgroundColor": "#f1f3f5"},
        },
        },
        "animations": {
            "fadeIn": "fade-in 0.5s ease-in-out",
            "hoverGrow": "transform 0.2s ease-in-out",
        },
}

# Optional: Export the default theme for fallback
#default_theme = DEFAULT_THEME
