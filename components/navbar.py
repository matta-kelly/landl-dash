import dash_mantine_components as dmc

def generate_navbar(pathname):
    if pathname.startswith("/wholesale"):
        return [
            dmc.NavLink(label="Home", href="/", childrenOffset=28),
            dmc.NavLink(
                label="Wholesale",
                href="/wholesale",
                opened=True,
                children=[
                    dmc.NavLink(label="Shipping Fulfillment", href="/wholesale/shipping"),
                    dmc.NavLink(label="Rep View", href="/wholesale/rep-view"),
                    dmc.NavLink(label="Customer Evaluation", href="/wholesale/customer-eval"),
                    dmc.NavLink(label="Product Analysis", href="/wholesale/product"),
                    dmc.NavLink(
                        label="Surf Expo",
                        href="/wholesale/surf-expo",
                        opened=True,
                        children=[
                            dmc.NavLink(label="Home", href="/wholesale/surf-expo"),
                            dmc.NavLink(label="Customer Evaluation", href="/wholesale/surf-expo/customer-eval"),
                            dmc.NavLink(label="Rep View", href="/wholesale/surf-expo/rep-view"),
                            dmc.NavLink(label="Shipping Fulfillment", href="/wholesale/surf-expo/shipping"),
                        ],
                    ),
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
