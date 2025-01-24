import dash_mantine_components as dmc

def generate_navbar(pathname):
    """
    Generates a dynamic list of navigation links based on the current pathname.

    Args:
        pathname (str): The current URL pathname.

    Returns:
        list: A list of `dmc.NavLink` components.
    """

    def get_overview_links():
        return dmc.NavLink(
            label="Overview",
            href="/overview",
            opened=pathname.startswith("/overview") or pathname == "/",
            children=[
                dmc.NavLink(label="Home", href="/overview"),
                dmc.NavLink(label="Sales Channel Comparison", href="/overview/channel-comparison"),
            ],
        )

    def get_wholesale_links():
        return dmc.NavLink(
            label="Wholesale",
            href="/wholesale",
            opened=pathname.startswith("/wholesale"),
            children=[
                dmc.NavLink(label="Home", href="/wholesale"),
                dmc.NavLink(label="Shipping Fulfillment", href="/wholesale/shipping"),
                dmc.NavLink(label="Rep View", href="/wholesale/rep-view"),
                dmc.NavLink(label="Customer Evaluation", href="/wholesale/customer-eval"),
                dmc.NavLink(label="Product Analysis", href="/wholesale/product"),
                dmc.NavLink(label="Surf Expo", href="/wholesale/se"),
            ],
        )

    def get_ecom_links():
        return dmc.NavLink(
            label="Ecom",
            href="/ecom",
            opened=pathname.startswith("/ecom"),
            children=[
                dmc.NavLink(label="Home", href="/ecom"),
                dmc.NavLink(label="Collection", href="/ecom/collection"),
            ],
        )

    def get_faire_links():
        return dmc.NavLink(
            label="Faire",
            href="/faire",
            opened=pathname.startswith("/faire"),
            children=[
                dmc.NavLink(label="Home", href="/faire"),
                dmc.NavLink(label="Winter Market", href="/faire/winter-market"),
            ],
        )

    # Always include all top-level links to display the full navigation menu
    nav_links = [
        get_overview_links(),
        get_wholesale_links(),
        get_ecom_links(),
        get_faire_links(),
    ]

    return nav_links
