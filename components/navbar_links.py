import dash_mantine_components as dmc

def generate_navbar(pathname):
    """
    Generates a dynamic list of navigation links based on the current pathname.

    Args:
        pathname (str): The current URL pathname.

    Returns:
        list: A list of `dmc.NavLink` components.
    """

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

    nav_links = [
        dmc.NavLink(label="Home", href="/", childrenOffset=28),
    ]

    # Add Wholesale links if pathname starts with /wholesale
    if pathname.startswith("/wholesale"):
        nav_links.append(get_wholesale_links())
        nav_links.append(get_ecom_links())
        nav_links.append(get_faire_links())

    # Add Ecom links if pathname starts with /ecom
    elif pathname.startswith("/ecom"):
        nav_links.append(get_wholesale_links())
        nav_links.append(get_ecom_links())
        nav_links.append(get_faire_links())

    # Add Faire links if pathname starts with /faire
    elif pathname.startswith("/faire"):
        nav_links.append(get_wholesale_links())
        nav_links.append(get_ecom_links())
        nav_links.append(get_faire_links())

    # Default: Add Wholesale, Ecom, and Faire links
    else:
        nav_links.append(get_wholesale_links())
        nav_links.append(get_ecom_links())
        nav_links.append(get_faire_links())

    return nav_links
