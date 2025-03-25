DEFAULT_TEMPLATES = [
    {
        "name": "简约模板",
        "description": "清新简约的排版风格",
        "css_styles": {
            "article": {
                "max-width": "800px",
                "margin": "0 auto",
                "padding": "20px",
                "font-family": "'PingFang SC', 'Helvetica Neue', Arial, sans-serif",
                "line-height": "1.8",
                "color": "#333"
            },
            "h1": {
                "font-size": "28px",
                "font-weight": "bold",
                "margin": "20px 0",
                "text-align": "center",
                "color": "#222"
            },
            "h2": {
                "font-size": "24px",
                "font-weight": "bold",
                "margin": "18px 0",
                "color": "#333"
            },
            "p": {
                "margin": "16px 0",
                "text-align": "justify"
            },
            "img": {
                "max-width": "100%",
                "height": "auto",
                "display": "block",
                "margin": "20px auto"
            },
            "blockquote": {
                "margin": "20px 0",
                "padding": "10px 20px",
                "border-left": "4px solid #ddd",
                "background": "#f9f9f9",
                "font-style": "italic"
            }
        },
        "html_structure": """
        <article class="wechat-article">
            {content}
        </article>
        """,
        "is_default": True
    },
    {
        "name": "商务风格",
        "description": "适合商业内容的专业排版",
        "css_styles": {
            "article": {
                "max-width": "800px",
                "margin": "0 auto",
                "padding": "20px",
                "font-family": "'PingFang SC', 'Helvetica Neue', Arial, sans-serif",
                "line-height": "1.6",
                "color": "#2c3e50"
            },
            "h1": {
                "font-size": "32px",
                "font-weight": "600",
                "margin": "24px 0",
                "text-align": "center",
                "color": "#1a365d"
            },
            "h2": {
                "font-size": "26px",
                "font-weight": "600",
                "margin": "20px 0",
                "color": "#2c5282"
            },
            "p": {
                "margin": "18px 0",
                "text-align": "justify",
                "letter-spacing": "0.5px"
            },
            "img": {
                "max-width": "100%",
                "height": "auto",
                "display": "block",
                "margin": "24px auto",
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
            },
            "blockquote": {
                "margin": "24px 0",
                "padding": "15px 25px",
                "border-left": "4px solid #2c5282",
                "background": "#ebf8ff",
                "font-style": "normal",
                "color": "#2a4365"
            }
        },
        "html_structure": """
        <article class="wechat-article business">
            {content}
        </article>
        """,
        "is_default": False
    }
] 