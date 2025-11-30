import tkinter as tk
import json

ELEMENT_HEIGHT = 100
ELEMENT_WIDTH = 90
X_MARGIN = 10
Y_MARGIN = 24
CARD_HEIGHT = 200
CARD_WIDTH = 200
CARD_TABLE_SEPARATION = 20
SELECTION_COLOR = "#FFFF00"
ELEMENTS_GAP = 6


group_names = {
    "alkali": "Alcalinos",
    "alkali_earth": "Alcalinotérreos",
    "transition_metals": "Metales de transición",
    "lantanoids": "Lantánidos",
    "actinoids": "Actínidos",
    "post-transition_metals": "Metales post transición",
    "metalloids": "Metalóides",
    "nonmetals": "No metales",
    "halogens": "Halógenos",
    "noble_gases": "Gases nobles",
    "hydrogen": "Hidrógeno"
}


def load_elements():
    with open("elements.json", "r") as file_reader:
        return json.load(file_reader)


def get_element_dimensions(
    row,
    col,
    element_width,
    element_height,
    x_margin,
    y_margin,
    card_height,
    card_table_separation,
    gap=0,
):
    dimensions = {}

    x = x_margin + (element_width + gap) * (col - 1)
    y = (
        y_margin
        + card_height
        + card_table_separation
        + (element_height + gap) * (row - 1)
    )

    dimensions["x"] = x
    dimensions["y"] = y
    dimensions["x_delta"] = x + element_width
    dimensions["y_delta"] = y + element_height

    return dimensions


def get_item_height(canvas: tk.Canvas, item_id):
    # This waits for the rendering tasks to finish so I can get the actual item's height
    canvas.update_idletasks()

    bbox = canvas.bbox(item_id)

    if bbox is None:
        return 0

    x1, y1, x2, y2 = bbox
    return y2 - y1


def draw_element(canvas: tk.Canvas, symbol, data, meta):
    row = data["coords"]["row"]
    col = data["coords"]["col"]

    dim = get_element_dimensions(
        row,
        col,
        ELEMENT_WIDTH,
        ELEMENT_HEIGHT,
        X_MARGIN,
        Y_MARGIN,
        CARD_HEIGHT,
        CARD_TABLE_SEPARATION,
        gap=ELEMENTS_GAP,
    )

    x = dim["x"]
    y = dim["y"]
    x_delta = dim["x_delta"]
    y_delta = dim["y_delta"]

    contenedor_id = canvas.create_rectangle(
        x,
        y,
        x_delta,
        y_delta,
        fill=meta["group_colors"][data["group"]],
        outline="black",
        width=2,
    )

    padding_top = 8
    padding_left = 8
    vertical_gap = 2

    accumulative_height = padding_top + vertical_gap

    # Draw atomic number
    atomic_number_id = canvas.create_text(
        x + padding_left,
        y + padding_top,
        text=str(data["atomic_number"]),
        font=("Arial", 12),
        anchor="nw",
    )

    atomic_number_height = get_item_height(canvas, atomic_number_id)
    accumulative_height += atomic_number_height

    # Draw symbol
    symbol_id = canvas.create_text(
        x + ELEMENT_WIDTH / 2,
        y + ELEMENT_HEIGHT / 2 - 10,
        text=symbol,
        font=("Arial", 24),
        anchor="center",
    )

    symbol_height = get_item_height(canvas, symbol_id)
    accumulative_height += symbol_height

    # Draw atomic weight
    atomic_weight_id = canvas.create_text(
        x + ELEMENT_WIDTH / 2,
        y + ELEMENT_HEIGHT - padding_top,
        text=data["atomic_weight"],
        font=("Arial", 8),
        anchor="s",
    )

    atomic_weight_height = get_item_height(canvas, atomic_weight_id)

    # Draw element's name
    canvas.create_text(
        x + ELEMENT_WIDTH / 2,
        y + ELEMENT_HEIGHT - padding_top - atomic_weight_height,
        text=data["name"],
        font=("Arial", 12),
        anchor="s",
    )

    return contenedor_id


def draw_element_details(canvas: tk.Canvas, symbol, data, meta):
    dynamic_elements_ids = []
    canvas_width = int(canvas["width"])

    # Card related variables
    card_x = canvas_width / 3
    card_y = Y_MARGIN
    centered_card_x = card_x + CARD_WIDTH / 2
    card_padding = 10

    # Extra information related variables
    extra_info = data["extra_info"]
    info_x = canvas_width / 2
    info_y = Y_MARGIN

    # Draw details card elements
    canvas.create_rectangle(
        card_x,
        card_y,
        card_x + CARD_WIDTH,
        card_y + CARD_HEIGHT,
        fill=str(meta["group_colors"][data["group"]]),
        outline="black",
        width=2,
    )

    level_height = 0

    for i in range(len(data["energy_levels"])):
        level = data["energy_levels"][i]
        level_id = canvas.create_text(
            card_x + CARD_WIDTH - card_padding,
            card_y + card_padding + level_height * i,
            text=str(level),
        )

        level_height = get_item_height(canvas, level_id)

        dynamic_elements_ids.append(level_id)

    atomic_number_id = canvas.create_text(
        card_x + card_padding,
        card_y + card_padding,
        text=str(data["atomic_number"]),
    )

    symbol_id = canvas.create_text(
        centered_card_x,
        card_y + CARD_HEIGHT / 2 - 20,
        text=str(symbol),
        font=("Arial", 40),
        anchor="center",
    )

    name_id = canvas.create_text(
        centered_card_x,
        card_y + CARD_HEIGHT / 2 + 20,
        text=data["name"],
        font=("Arial", 16),
        anchor="center",
    )

    atomic_weight_id = canvas.create_text(
        centered_card_x, card_y + CARD_HEIGHT - card_padding,
        text=data["atomic_weight"],
        anchor="s"
    )

    # Draw extra info elements
    accumulative_height = 0

    discovery_id = canvas.create_text(
        info_x,
        info_y,
        text=f"Descubierto el año: {extra_info['discovery_date']} en {extra_info['discovery_place']}",
        font=("Arial", 16),
        anchor="nw",
    )

    accumulative_height += get_item_height(canvas, discovery_id)

    group_name_id = canvas.create_text(
        info_x,
        info_y + accumulative_height,
        text=f"Grupo {group_names[data["group"]]}",
        font=("Arial", 16),
        anchor="nw"
    )
    
    accumulative_height += get_item_height(canvas, group_name_id)

    usage_label_id = canvas.create_text(
        info_x,
        info_y + accumulative_height,
        text="Se usa en:",
        font=("Arial", 16),
        anchor="nw",
    )

    accumulative_height += get_item_height(canvas, usage_label_id)

    for usage in extra_info["common_uses"]:
        usage_id = canvas.create_text(
            info_x + 16,
            info_y + accumulative_height,
            text=f"• {usage}",
            font=("Arial", 16),
            anchor="nw",
        )

        dynamic_elements_ids.append(usage_id)
        accumulative_height += get_item_height(canvas, usage_id)

    """
    Añadir ids a lista de ids de elementos dinámicos.
    Se usa para cambiar el elemento que se muestra en la tarjeta
    """
    dynamic_elements_ids.append(name_id)
    dynamic_elements_ids.append(symbol_id)
    dynamic_elements_ids.append(atomic_number_id)
    dynamic_elements_ids.append(atomic_weight_id)
    dynamic_elements_ids.append(discovery_id)
    dynamic_elements_ids.append(usage_label_id)
    dynamic_elements_ids.append(group_name_id)

    return dynamic_elements_ids


def highlight_element(canvas: tk.Canvas, item_id, color, width=1):
    canvas.itemconfig(item_id, width=width, outline=color)


def main():
    root = tk.Tk()
    root.title("Periodically")

    elements_document = load_elements()
    elements = elements_document["elements"]
    meta = elements_document["meta"]
    dynamic_ids = None
    containers_ids = {}
    selected_element = "H"

    def on_click(event):
        nonlocal selected_element
        x_click, y_click = event.x, event.y

        for symbol, data in elements.items():
            container_id = containers_ids[symbol]

            bbox = canvas.bbox(container_id)
            if bbox is None:
                continue
            x1, y1, x2, y2 = bbox

            if x1 <= x_click <= x2 and y1 <= y_click <= y2:
                # Ignore same element
                if symbol == selected_element:
                    continue

                if dynamic_ids:
                    for item_id in dynamic_ids:
                        canvas.delete(item_id)
                    dynamic_ids.clear()

                new_ids = draw_element_details(canvas, symbol, data, meta)
                dynamic_ids.extend(new_ids)

                # Remove highlight from previous selected element
                highlight_element(canvas, containers_ids[selected_element], "black", 2)

                # Highlight newly selected element
                highlight_element(canvas, container_id, SELECTION_COLOR, 2)

                # Update selected element
                selected_element = symbol

    canvas_width = meta["cols"] * (ELEMENT_WIDTH + ELEMENTS_GAP) + X_MARGIN * 2
    canvas_height = (
        meta["rows"] * ELEMENT_HEIGHT
        + Y_MARGIN * 2
        + CARD_HEIGHT
        + CARD_TABLE_SEPARATION
        + ELEMENTS_GAP * meta["rows"]
    )

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")

    canvas.bind("<Button-1>", on_click)

    canvas.pack()

    dynamic_ids = draw_element_details(
        canvas, selected_element, elements[selected_element], meta
    )

    for symbol, data in elements.items():
        container_id = draw_element(canvas, symbol, data, meta)
        containers_ids[symbol] = container_id

    if containers_ids[selected_element] is not None:
        highlight_element(canvas, containers_ids[selected_element], SELECTION_COLOR)

    root.mainloop()


if __name__ == "__main__":
    main()
