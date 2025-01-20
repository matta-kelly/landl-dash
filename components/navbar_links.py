import dash_mantine_components as dmc

def generate_navbar(pathname):
    """
    Generates a dynamic list of navigation links based on the current pathname.

    Args:
        pathname (str): The current URL pathname.

    Returns:
        list: A list of `dmc.NavLink` components.
    """
    if pathname.startswith("/wholesale"):
        return [
            dmc.NavLink(label="Home", href="/", childrenOffset=28),
            dmc.NavLink(
                label="Wholesale",
                href="/wholesale",
                opened=True,
                children=[
                    dmc.NavLink(label="Home", href="/wholesale"),
                    dmc.NavLink(label="Shipping Fulfillment", href="/wholesale/shipping"),
                    dmc.NavLink(label="Rep View", href="/wholesale/rep-view"),
                    dmc.NavLink(label="Customer Evaluation", href="/wholesale/customer-eval"),
                    dmc.NavLink(label="Product Analysis", href="/wholesale/product"),
                ],
            ),
            dmc.NavLink(label="Ecom", href="/ecom", childrenOffset=28),
        ]
    elif pathname.startswith("/ecom"):
        return [
            dmc.NavLink(label="Home", href="/", childrenOffset=28),
            dmc.NavLink(label="Wholesale", href="/wholesale", childrenOffset=28),
            dmc.NavLink(
                label="Ecom",
                href="/ecom",
                opened=True,
                children=[
                    dmc.NavLink(label="Home", href="/ecom"),
                ],
            ),
        ]
    else:
        return [
            dmc.NavLink(label="Wholesale", href="/wholesale", childrenOffset=28),
            dmc.NavLink(label="Ecom", href="/ecom", childrenOffset=28),
        ]
