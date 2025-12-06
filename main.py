import tkinter as tk
import json

ELEMENT_HEIGHT = 80
ELEMENT_WIDTH = 70
X_MARGIN = 10
Y_MARGIN = 24
CARD_HEIGHT = 140
CARD_WIDTH = 160
CARD_TABLE_SEPARATION = 20
SELECTION_COLOR = "#FFFF00"
ELEMENTS_GAP = 6

theme_colors = {
    "light": {
        "text": "#1E1E1E",
        "background": "#FAFAFA",
        "button_bg": "#E9E9E9",
        "button_border": "#C7C7C7",
        "selection_border": "#FFD700",
        "element_border": "#2E2E2E",
    },
    "dark": {
        "text": "#DDDDDD",
        "background": "#1E1E1E",
        "button_bg": "#2A2A2A",
        "button_border": "#3A3A3A",
        "selection_border": "#FFD700",
        "element_border": "#505050",
    },
}

group_names = {
    "alkali": "Alcalinos",
    "alkali_earth": "Alcalinotérreos",
    "transition_metals": "Metales de transición",
    "lanthanides": "Lantánidos",
    "actinoids": "Actínidos",
    "post-transition_metals": "Metales post transición",
    "metalloids": "Metalóides",
    "nonmetals": "No metales",
    "halogens": "Halógenos",
    "noble_gases": "Gases nobles",
    "hydrogen": "Hidrógeno",
    "unknown": "Desconocido",
}

strings = {"light": "Claro", "dark": "Oscuro"}


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


def draw_element(canvas: tk.Canvas, symbol, data, meta, theme):
    row = data["coords"]["row"]
    col = data["coords"]["col"]
    text_color = theme_colors[theme]["text"]
    text_ids: list[int] = list()

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

    container_id = canvas.create_rectangle(
        x,
        y,
        x_delta,
        y_delta,
        fill=meta["group_colors"][theme][data["group"]],
        outline=theme_colors[theme]["element_border"],
        width=2,
    )

    padding_top = 6
    padding_left = 6
    vertical_gap = 2

    accumulative_height = padding_top + vertical_gap

    # Draw atomic number
    atomic_number_id = canvas.create_text(
        x + padding_left,
        y + padding_top,
        text=str(data["atomic_number"]),
        font=("Arial", 10),
        fill=text_color,
        anchor="nw",
    )

    atomic_number_height = get_item_height(canvas, atomic_number_id)
    accumulative_height += atomic_number_height

    # Draw symbol
    symbol_id = canvas.create_text(
        x + ELEMENT_WIDTH / 2,
        y + ELEMENT_HEIGHT / 2 - 10,
        text=symbol,
        font=("Arial", 20),
        fill=text_color,
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
        fill=text_color,
        anchor="s",
    )

    atomic_weight_height = get_item_height(canvas, atomic_weight_id)

    # Draw element's name
    element_name_id = canvas.create_text(
        x + ELEMENT_WIDTH / 2,
        y + ELEMENT_HEIGHT - padding_top - atomic_weight_height,
        text=data["name"],
        font=("Arial", 8),
        fill=text_color,
        anchor="s",
    )

    text_ids.extend([atomic_number_id, symbol_id, atomic_weight_id, element_name_id])

    return container_id, text_ids


def draw_element_details(canvas: tk.Canvas, symbol, data, meta, theme):
    dynamic_elements_ids: list[int] = list()
    text_ids: list[int] = list()
    canvas_width = int(canvas["width"])
    text_color = theme_colors[theme]["text"]

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
    card_id = canvas.create_rectangle(
        card_x,
        card_y,
        card_x + CARD_WIDTH,
        card_y + CARD_HEIGHT,
        fill=str(meta["group_colors"][theme][data["group"]]),
        outline=theme_colors[theme]["element_border"],
        width=2,
    )

    level_height = 0

    for i in range(len(data["energy_levels"])):
        level = data["energy_levels"][i]
        level_id = canvas.create_text(
            card_x + CARD_WIDTH - card_padding,
            card_y + card_padding + level_height * i,
            text=str(level),
            fill=text_color,
            anchor="ne",
        )

        level_height = get_item_height(canvas, level_id)

        dynamic_elements_ids.append(level_id)
        text_ids.append(level_id)

    atomic_number_id = canvas.create_text(
        card_x + card_padding,
        card_y + card_padding,
        anchor="nw",
        fill=text_color,
        text=str(data["atomic_number"]),
    )

    symbol_id = canvas.create_text(
        centered_card_x,
        card_y + CARD_HEIGHT / 2 - 20,
        text=str(symbol),
        font=("Arial", 32),
        fill=text_color,
        anchor="center",
    )

    name_id = canvas.create_text(
        centered_card_x,
        card_y + CARD_HEIGHT / 2 + 20,
        text=data["name"],
        font=("Arial", 12),
        fill=text_color,
        anchor="center",
    )

    atomic_weight_id = canvas.create_text(
        centered_card_x,
        card_y + CARD_HEIGHT - card_padding,
        text=data["atomic_weight"],
        fill=text_color,
        anchor="s",
    )

    # Draw extra info elements
    accumulative_height = 0

    discovery_id = canvas.create_text(
        info_x,
        info_y,
        text=f"Descubierto el año: {extra_info['discovery_date']} en {extra_info['discovery_place']}",
        font=("Arial", 14),
        fill=text_color,
        anchor="nw",
    )

    accumulative_height += get_item_height(canvas, discovery_id)

    group_name_id = canvas.create_text(
        info_x,
        info_y + accumulative_height,
        text=f"Grupo {group_names[data['group']]}",
        font=("Arial", 14),
        fill=text_color,
        anchor="nw",
    )

    accumulative_height += get_item_height(canvas, group_name_id)

    usage_label_id = canvas.create_text(
        info_x,
        info_y + accumulative_height,
        text="Se usa en:",
        font=("Arial", 14),
        fill=text_color,
        anchor="nw",
    )

    accumulative_height += get_item_height(canvas, usage_label_id)

    for usage in extra_info["common_uses"]:
        usage_id = canvas.create_text(
            info_x + 16,
            info_y + accumulative_height,
            text=f"• {usage}",
            font=("Arial", 14),
            fill=text_color,
            anchor="nw",
        )

        dynamic_elements_ids.append(usage_id)
        text_ids.append(usage_id)
        accumulative_height += get_item_height(canvas, usage_id)

    """
    Añadir ids a lista de ids de elementos dinámicos.
    Se usa para cambiar el elemento que se muestra en la tarjeta
    """
    dynamic_elements_ids.extend(
        [
            card_id,
            name_id,
            symbol_id,
            atomic_number_id,
            atomic_weight_id,
            discovery_id,
            usage_label_id,
            group_name_id,
        ]
    )

    text_ids.extend(
        [
            atomic_number_id,
            symbol_id,
            name_id,
            atomic_weight_id,
            discovery_id,
            group_name_id,
            usage_label_id,
        ]
    )

    return dynamic_elements_ids, text_ids, card_id


def highlight_element(canvas: tk.Canvas, item_id, color, width=1):
    canvas.itemconfig(item_id, width=width, outline=color)


def main():
    root = tk.Tk()
    root.title("Periodically")

    elements_document = load_elements()
    elements = elements_document["elements"]
    meta = elements_document["meta"]
    default_theme = "dark"

    canvas_width = meta["cols"] * (ELEMENT_WIDTH + ELEMENTS_GAP) + X_MARGIN * 2
    canvas_height = (
        meta["rows"] * ELEMENT_HEIGHT
        + Y_MARGIN * 2
        + CARD_HEIGHT
        + CARD_TABLE_SEPARATION
        + ELEMENTS_GAP * meta["rows"]
    )

    canvas = tk.Canvas(
        root,
        width=canvas_width,
        height=canvas_height,
        bg=theme_colors[default_theme]["background"],
    )

    canvas.pack()

    draw_table(canvas, elements, meta, default_theme)

    root.mainloop()


def draw_table(canvas: tk.Canvas, elements, meta, default_theme):
    dynamic_ids = None
    selected_element = "H"
    selected_element_container = None
    selected_text_ids: list[int] = list()
    element_container_ids: dict[str, int] = {}
    text_ids: list[int] = list()
    theme = default_theme
    dynamic_elements_ids, details_text_ids, details_container_id = draw_element_details(
        canvas, selected_element, elements[selected_element], meta, theme
    )
    dynamic_ids = dynamic_elements_ids
    text_ids.extend(details_text_ids)
    selected_text_ids.extend(details_text_ids)

    selected_element_container = details_container_id

    theme_button_width = 100
    theme_button_height = 50
    theme_button_x = int(canvas["width"]) - X_MARGIN - theme_button_width
    theme_button_y = Y_MARGIN
    theme_button_delta_x = theme_button_x + theme_button_width
    theme_button_delta_y = theme_button_y + theme_button_height

    theme_button_id, theme_button_text_id = draw_button(
        canvas,
        theme,
        theme_colors[theme]["text"],
        theme_button_x,
        theme_button_y,
        theme_button_delta_x,
        theme_button_delta_y,
        fill=theme_colors[theme]["button_bg"],
        outline=theme_colors[theme]["button_border"],
    )

    def on_click(event):
        nonlocal theme
        nonlocal selected_element
        nonlocal selected_element_container
        x_click, y_click = event.x, event.y

        if (
            theme_button_x <= x_click <= theme_button_delta_x
            and theme_button_y <= y_click <= theme_button_delta_y
        ):
            if theme == "light":
                theme = "dark"
            else:
                theme = "light"

            update_theme(
                canvas,
                theme,
                elements,
                meta,
                selected_element,
                selected_element_container,
                text_ids,
                element_container_ids,
                theme_button_id,
                theme_button_text_id
            )

        for symbol, data in elements.items():
            container_id = element_container_ids[symbol]

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

                new_dynamic_ids, new_text_ids, new_container_id = draw_element_details(
                    canvas, symbol, data, meta, theme
                )

                selected_element_container = new_container_id

                filtered_text_ids = [
                    id for id in text_ids if id not in selected_text_ids
                ]
                selected_text_ids.clear()
                selected_text_ids.extend(new_text_ids)

                text_ids.clear()
                text_ids.extend(filtered_text_ids)
                text_ids.extend(new_text_ids)
                dynamic_ids.extend(new_dynamic_ids)

                # Remove highlight from previous selected element
                highlight_element(
                    canvas,
                    element_container_ids[selected_element],
                    theme_colors[theme]["element_border"],
                    2,
                )

                # Highlight newly selected element
                highlight_element(
                    canvas, container_id, theme_colors[theme]["selection_border"], 2
                )

                # Update selected element
                selected_element = symbol

    for symbol, data in elements.items():
        container_id, element_text_ids = draw_element(canvas, symbol, data, meta, theme)
        element_container_ids[symbol] = container_id
        text_ids.extend(element_text_ids)

    if element_container_ids[selected_element] is not None:
        highlight_element(
            canvas,
            element_container_ids[selected_element],
            theme_colors[theme]["selection_border"],
        )

    canvas.bind("<Button-1>", on_click)

    return dynamic_ids, element_container_ids


def draw_button(canvas: tk.Canvas, text, text_color, x1, y1, x2, y2, **options):
    button_height = y2 - y1
    button_width = x2 - x1
    
    container_id = canvas.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        **options,
    )
    
    theme_text_id = canvas.create_text(
        x1 + button_width / 2,
        y1 + button_height / 2,
        text=text,
        fill=text_color,
        anchor="center",
        font=("Arial", 14)
    )

    return container_id, theme_text_id


def update_theme(
    canvas: tk.Canvas,
    theme,
    elements,
    meta,
    selected_element,
    selected_container_id,
    text_ids,
    element_container_ids,
    theme_button_id,
    theme_button_text_id
):
    canvas.config(bg=theme_colors[theme]["background"])

    for id in text_ids:
        canvas.itemconfig(id, fill=theme_colors[theme]["text"])

    for symbol, id in element_container_ids.items():
        element_group = get_group(elements, symbol)
        element_color = get_group_color(meta, theme, element_group)
        canvas.itemconfig(
            id, fill=element_color, outline=theme_colors[theme]["element_border"]
        )

        if symbol == selected_element:
            canvas.itemconfig(id, outline=theme_colors[theme]["selection_border"])

    if selected_element:
        selected_group = get_group(elements, selected_element)
        selected_color = get_group_color(meta, theme, selected_group)
        canvas.itemconfig(
            selected_container_id,
            fill=selected_color,
            outline=theme_colors[theme]["element_border"],
        )
    
    if theme_button_id and theme_button_text_id:
        canvas.itemconfig(
            theme_button_id,
            fill=theme_colors[theme]["button_bg"],
            outline=theme_colors[theme]["button_border"]
        )
        
        canvas.itemconfig(
            theme_button_text_id,
            text=theme,
            fill=theme_colors[theme]["text"]
        )


def get_group_color(meta, theme, group):
    return meta["group_colors"][theme][group]


def get_group(elements, symbol):
    return elements[symbol]["group"]


if __name__ == "__main__":
    main()
