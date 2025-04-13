import matplotlib.pyplot as plt
import matplotlib.patches as patches
import yaml

def generate_request_and_response_diagrams(yaml_file, request_diagram_path, response_diagram_path, markdown_path):
    """
    Generates byte-level diagrams for ECB request and response packet structures
    from a YAML file, and outputs a Markdown file with their descriptions.
    """

    try:
        with open(yaml_file, 'r') as f:
            yaml_data = yaml.safe_load(f)
        print("YAML file loaded successfully.")
    except Exception as e:
        print(f"Error loading YAML file: {e}")
        return

    if not isinstance(yaml_data, dict) or 'Request' not in yaml_data or 'Response' not in yaml_data:
        print("Invalid YAML format.")
        return

    markdown_content = "# ECB Packet Structure Documentation\n\n"

    def generate_packet_table(packet_type, fields):
        table = f"## {packet_type} Packet Structure\n\n"
        table += f"![{packet_type} Diagram]({packet_type.lower()}_packet_structure.png)\n\n"
        table += "| Name | Size | Bit Offsets | Description |\n"
        table += "|------|------|--------------|-------------|\n"
        for field in fields:
            table += f"| {field.get('name','')} | {field.get('size','')} | {field.get('bit_offset','')} | {field.get('description','')} |\n"
        return table

    for packet_type in ['Request', 'Response']:
        fields = yaml_data.get(packet_type, [])
        if not fields:
            print(f"No fields for {packet_type}")
            continue

        print(f"Generating diagram for {packet_type}")

        # Step 1: Preprocess total bit width
        total_bits = 0
        bit_lengths = []
        for field in fields:
            size = field.get("size", "8 bits")
            try:
                if "bit" in size:
                    bits = int(size.split()[0])
                elif "byte" in size:
                    bits = int(size.split()[0]) * 8
                else:
                    bits = 8
            except:
                bits = 8
            total_bits += bits
            bit_lengths.append(bits)

        scale = 0.05  # How wide each bit appears
        min_width = 0.3  # Ensure very narrow fields are still visible
        fig_width = max(8, total_bits * scale)

        fig, ax = plt.subplots(figsize=(fig_width, 2))
        ax.set_xlim(0, total_bits * scale)
        ax.set_ylim(0, 1)
        ax.axis("off")

        current_x = 0

        for field, bits in zip(fields, bit_lengths):
            name = field.get("name", "N/A")
            draw_width = max(bits * scale, min_width)

            # Draw rectangle
            ax.add_patch(patches.Rectangle(
                (current_x, 0.2), draw_width, 0.6,
                facecolor="lightblue", edgecolor="black", lw=1.2
            ))

            # Center label
            ax.text(current_x + draw_width / 2, 0.5, f"{name}\n{bits} bits",
                    ha="center", va="center", fontsize=10, fontweight="bold")

            current_x += draw_width

        # Save diagram
        out_path = request_diagram_path if packet_type == "Request" else response_diagram_path
        plt.savefig(out_path, bbox_inches="tight", pad_inches=0.1, dpi=300)
        plt.close(fig)

        markdown_content += generate_packet_table(packet_type, fields)

    # Save markdown
    try:
        with open(markdown_path, "w") as f:
            f.write(markdown_content)
        print(f"Markdown file saved to {markdown_path}.")
    except Exception as e:
        print(f"Error writing markdown file: {e}")


# Example YAML file path (you should create a YAML file with the required structure)
yaml_file_path = 'ECB.yaml'

# File paths to save the diagrams and markdown file
request_diagram_path = 'ECB_request_packet_structure.png'
response_diagram_path = 'ECB_response_packet_structure.png'
markdown_path = 'ECB_packet_structure.md'

# Generate the diagrams and Markdown
generate_request_and_response_diagrams(yaml_file_path, request_diagram_path, response_diagram_path, markdown_path)

print("Diagrams and Markdown file generated successfully!")

#generate_request_and_response_diagrams("ECB.yaml", "request_packet.png", "response_packet.png", "example.md")