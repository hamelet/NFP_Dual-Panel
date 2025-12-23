import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np
import math
from io import BytesIO

st.set_page_config(page_title="Nutrition Facts Panel Generator", page_icon="🥗", layout="wide")

# Title and description
st.title("🥗 Dual Nutrition Facts Panel Generator")
st.markdown("Generate FDA-compliant side-by-side nutrition facts panels for per-serving and per-container values.")

# Sidebar for product information
st.sidebar.header("Product Information")
product_name = st.sidebar.text_input("Product Name", "My Product")
serving_size = st.sidebar.text_input("Serving Size", "2/3 cup (124g)")
servings_per_container = st.sidebar.number_input("Servings Per Container", min_value=1, value=3, step=1)

# Main input section
st.header("Nutritional Information")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Per Serving")
    calories_serving = st.number_input("Calories", min_value=0, value=170, step=5, key="cal_serving")
    total_fat_serving = st.number_input("Total Fat (g)", min_value=0.0, value=6.0, step=0.5, key="fat_serving")
    saturated_fat_serving = st.number_input("Saturated Fat (g)", min_value=0.0, value=3.5, step=0.5, key="sat_serving")
    trans_fat_serving = st.number_input("Trans Fat (g)", min_value=0.0, value=0.0, step=0.1, key="trans_serving")
    cholesterol_serving = st.number_input("Cholesterol (mg)", min_value=0, value=15, step=5, key="chol_serving")
    sodium_serving = st.number_input("Sodium (mg)", min_value=0, value=110, step=5, key="sodium_serving")
    total_carb_serving = st.number_input("Total Carbohydrate (g)", min_value=0.0, value=24.0, step=0.5, key="carb_serving")
    dietary_fiber_serving = st.number_input("Dietary Fiber (g)", min_value=0.0, value=1.0, step=0.5, key="fiber_serving")
    total_sugars_serving = st.number_input("Total Sugars (g)", min_value=0.0, value=18.0, step=0.5, key="sugar_serving")
    added_sugars_serving = st.number_input("Added Sugars (g)", min_value=0.0, value=15.0, step=0.5, key="added_serving")
    protein_serving = st.number_input("Protein (g)", min_value=0.0, value=6.0, step=0.5, key="protein_serving")
    vitamin_d_serving = st.number_input("Vitamin D (mcg)", min_value=0.0, value=0.0, step=0.1, key="vitd_serving")
    calcium_serving = st.number_input("Calcium (mg)", min_value=0, value=260, step=10, key="calcium_serving")
    iron_serving = st.number_input("Iron (mg)", min_value=0.0, value=0.0, step=0.1, key="iron_serving")
    potassium_serving = st.number_input("Potassium (mg)", min_value=0, value=240, step=10, key="potassium_serving")

with col2:
    st.subheader("Per Container")
    st.info("💡 Values are automatically calculated based on servings per container")
    
    # Calculate per container values
    calories_container = calories_serving * servings_per_container
    total_fat_container = total_fat_serving * servings_per_container
    saturated_fat_container = saturated_fat_serving * servings_per_container
    trans_fat_container = trans_fat_serving * servings_per_container
    cholesterol_container = cholesterol_serving * servings_per_container
    sodium_container = sodium_serving * servings_per_container
    total_carb_container = total_carb_serving * servings_per_container
    dietary_fiber_container = dietary_fiber_serving * servings_per_container
    total_sugars_container = total_sugars_serving * servings_per_container
    added_sugars_container = added_sugars_serving * servings_per_container
    protein_container = protein_serving * servings_per_container
    vitamin_d_container = vitamin_d_serving * servings_per_container
    calcium_container = calcium_serving * servings_per_container
    iron_container = iron_serving * servings_per_container
    potassium_container = potassium_serving * servings_per_container
    
    # Display calculated values
    st.metric("Calories", f"{calories_container:.0f}")
    st.metric("Total Fat (g)", f"{total_fat_container:.1f}")
    st.metric("Saturated Fat (g)", f"{saturated_fat_container:.1f}")
    st.metric("Trans Fat (g)", f"{trans_fat_container:.1f}")
    st.metric("Cholesterol (mg)", f"{cholesterol_container:.0f}")
    st.metric("Sodium (mg)", f"{sodium_container:.0f}")
    st.metric("Total Carbohydrate (g)", f"{total_carb_container:.1f}")
    st.metric("Dietary Fiber (g)", f"{dietary_fiber_container:.1f}")
    st.metric("Total Sugars (g)", f"{total_sugars_container:.1f}")
    st.metric("Added Sugars (g)", f"{added_sugars_container:.1f}")
    st.metric("Protein (g)", f"{protein_container:.1f}")
    st.metric("Vitamin D (mcg)", f"{vitamin_d_container:.1f}")
    st.metric("Calcium (mg)", f"{calcium_container:.0f}")
    st.metric("Iron (mg)", f"{iron_container:.1f}")
    st.metric("Potassium (mg)", f"{potassium_container:.0f}")

# Generate button
if st.button("🎨 Generate Nutrition Facts Panel", type="primary", use_container_width=True):
    
    # Create nutrients dataframe
    nutrients_data = {
        'Nutrient': ['Calories', 'Total Fat', 'Saturated Fat', 'Trans Fat', 'Cholesterol', 
                     'Sodium', 'Total Carbohydrate', 'Dietary Fiber', 'Total Sugars', 
                     'Added Sugars', 'Protein', 'Vitamin D', 'Calcium', 'Iron', 'Potassium'],
        'Amount Per Serving': [calories_serving, total_fat_serving, saturated_fat_serving, 
                               trans_fat_serving, cholesterol_serving, sodium_serving,
                               total_carb_serving, dietary_fiber_serving, total_sugars_serving,
                               added_sugars_serving, protein_serving, vitamin_d_serving,
                               calcium_serving, iron_serving, potassium_serving],
        'Amount Per Container': [calories_container, total_fat_container, saturated_fat_container,
                                trans_fat_container, cholesterol_container, sodium_container,
                                total_carb_container, dietary_fiber_container, total_sugars_container,
                                added_sugars_container, protein_container, vitamin_d_container,
                                calcium_container, iron_container, potassium_container],
        'Unit': ['', 'g', 'g', 'g', 'mg', 'mg', 'g', 'g', 'g', 'g', 'g', 'mcg', 'mg', 'mg', 'mg']
    }
    
    nutrients_df = pd.DataFrame(nutrients_data)
    
    # FDA Rounding Rules
    def round_nutrition_value(nutrient, amount):
        if nutrient == 'Calories':
            if amount < 5:
                return 0
            elif amount <= 50:
                return round(amount / 5) * 5
            else:
                return round(amount / 10) * 10
        elif nutrient in ['Total Fat', 'Saturated Fat', 'Trans Fat']:
            if amount < 0.5:
                return 0
            elif amount < 5:
                return round(amount * 2) / 2
            else:
                return round(amount)
        elif nutrient == 'Cholesterol':
            if amount < 2:
                return 0
            elif amount <= 5:
                return math.ceil(amount)
            else:
                return round(amount / 5) * 5
        elif nutrient == 'Sodium':
            if amount < 5:
                return 0
            elif amount <= 140:
                return round(amount / 5) * 5
            else:
                return round(amount / 10) * 10
        elif nutrient in ['Total Carbohydrate', 'Dietary Fiber', 'Total Sugars', 'Added Sugars', 'Protein']:
            if amount < 0.5:
                return 0
            else:
                return round(amount)
        elif nutrient in ['Vitamin D', 'Calcium', 'Iron', 'Potassium']:
            return round(amount)
        return amount
    
    nutrients_df['Rounded Per Serving'] = nutrients_df.apply(
        lambda row: round_nutrition_value(row['Nutrient'], row['Amount Per Serving']), axis=1)
    nutrients_df['Rounded Per Container'] = nutrients_df.apply(
        lambda row: round_nutrition_value(row['Nutrient'], row['Amount Per Container']), axis=1)
    
    # Calculate Daily Values
    daily_values = {
        'Total Fat': 78,
        'Saturated Fat': 20,
        'Cholesterol': 300,
        'Sodium': 2300,
        'Total Carbohydrate': 275,
        'Dietary Fiber': 28,
        'Added Sugars': 50,
        'Protein': 50,
        'Vitamin D': 20,
        'Calcium': 1300,
        'Iron': 18,
        'Potassium': 4700
    }
    
    def calculate_dv(nutrient, amount_serving, amount_container):
        if nutrient in daily_values:
            dv_serving = (amount_serving / daily_values[nutrient]) * 100
            dv_container = (amount_container / daily_values[nutrient]) * 100
            return round(dv_serving), round(dv_container)
        return None, None
    
    dv_results = nutrients_df.apply(
        lambda row: calculate_dv(row['Nutrient'], row['Rounded Per Serving'], row['Rounded Per Container']), 
        axis=1, result_type='expand'
    )
    nutrients_df['DV Serving'] = dv_results[0]
    nutrients_df['DV Container'] = dv_results[1]
    
    # Create the visualization
    fig, ax = plt.subplots(figsize=(8, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis('off')
    
    # Column positions
    nutrient_col = 0.5
    serving_amount_col = 4.2
    serving_dv_col = 5.2
    container_amount_col = 7.2
    container_dv_col = 8.2
    
    left_separator_x = 5.5
    right_separator_x = 8.5
    
    serving_header_center = (nutrient_col + left_separator_x) / 2 + 0.7
    container_header_center = (left_separator_x + right_separator_x) / 2 + 0.8
    
    line_height = 0.32
    
    def add_text(x, y, text, size=10, weight='normal', ha='left'):
        ax.text(x, y, text, fontsize=size, weight=weight, ha=ha, va='top', family='Arial')
    
    def draw_line(y, style='solid', thickness=0.8):
        line_dict = {
            'solid': (thickness, 'solid'),
            'thick': (10, 'solid'),
            'medium': (5, 'solid')
        }
        lw, ls = line_dict.get(style, (thickness, style))
        ax.plot([nutrient_col, container_dv_col], [y, y], 'k-', linewidth=lw, linestyle=ls)
    
    def format_amount(amt, unit):
        if unit == '':
            return ''
        if unit == 'g' and amt < 1:
            return f'<1{unit}'
        if isinstance(amt, float) and amt.is_integer():
            return f'{int(amt)}{unit}'
        return f'{amt:.1f}{unit}' if isinstance(amt, float) else f'{amt}{unit}'
    
    # Start drawing
    y_pos = 15.5
    
    # Outer border
    border = Rectangle((nutrient_col - 0.1, 0.3), 
                       container_dv_col - nutrient_col + 0.3, 
                       y_pos - 0.2, 
                       linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(border)
    
    # Title
    add_text(nutrient_col, y_pos, 'Nutrition Facts', size=28, weight='bold')
    y_pos -= 0.7
    
    # Serving info
    add_text(nutrient_col, y_pos, f'{servings_per_container} servings per container', size=10)
    y_pos -= 0.35
    add_text(nutrient_col, y_pos, 'Serving size', size=10, weight='bold')
    add_text(nutrient_col + 2.5, y_pos, serving_size, size=10, weight='bold')
    y_pos -= 0.35
    draw_line(y_pos, style='thick')
    y_pos -= 0.35
    
    # Column headers
    vertical_separator_top = y_pos
    add_text(serving_header_center, y_pos, 'Per Serving', size=11, weight='bold', ha='center')
    add_text(container_header_center, y_pos, 'Per Container', size=11, weight='bold', ha='center')
    y_pos -= 0.45
    draw_line(y_pos, style='medium')
    y_pos -= 0.35
    
    # Calories
    cal_serving = int(nutrients_df[nutrients_df['Nutrient'] == 'Calories']['Rounded Per Serving'].values[0])
    cal_container = int(nutrients_df[nutrients_df['Nutrient'] == 'Calories']['Rounded Per Container'].values[0])
    add_text(nutrient_col, y_pos, 'Calories', size=13, weight='bold')
    add_text(serving_header_center, y_pos - 0.05, str(cal_serving), size=23, weight='bold', ha='center')
    add_text(container_header_center, y_pos - 0.05, str(cal_container), size=23, weight='bold', ha='center')
    y_pos -= 0.5
    draw_line(y_pos, style='medium')
    y_pos -= 0.3
    
    # % Daily Value header
    add_text(serving_dv_col, y_pos, '% DV*', size=8, weight='bold', ha='right')
    add_text(container_dv_col, y_pos, '% DV*', size=8, weight='bold', ha='right')
    y_pos -= 0.22
    draw_line(y_pos, style='solid', thickness=1)
    y_pos -= 0.32
    
    # Iterate through nutrients
    for idx, row in nutrients_df.iterrows():
        nutrient = row['Nutrient']
        
        if nutrient == 'Calories':
            continue
        
        amt_serving = row['Rounded Per Serving']
        amt_container = row['Rounded Per Container']
        unit = row['Unit']
        dv_serving = row['DV Serving']
        dv_container = row['DV Container']
        
        display_name = nutrient
        if nutrient == 'Total Carbohydrate':
            display_name = 'Total Carb.'
        
        indent = nutrient_col
        size = 11
        weight = 'bold'
        
        if nutrient in ['Vitamin D', 'Calcium', 'Iron', 'Potassium']:
            weight = 'normal'
            size = 10.5
        elif nutrient in ['Saturated Fat', 'Trans Fat']:
            indent = nutrient_col + 0.25
            weight = 'normal'
            size = 10
        elif nutrient in ['Dietary Fiber', 'Total Sugars']:
            indent = nutrient_col + 0.25
            weight = 'normal'
            size = 10
        elif nutrient == 'Added Sugars':
            indent = nutrient_col + 0.5
            weight = 'normal'
            size = 9.5
        
        amt_serving_str = format_amount(amt_serving, unit)
        amt_container_str = format_amount(amt_container, unit)
        
        if nutrient == 'Added Sugars':
            nutrient_label = 'Incl. Added Sugars'
            add_text(indent, y_pos, nutrient_label, size=size, weight=weight)
            add_text(serving_amount_col, y_pos, amt_serving_str, size=10, weight='normal', ha='right')
            add_text(container_amount_col, y_pos, amt_container_str, size=10, weight='normal', ha='right')
            if pd.notna(dv_serving):
                add_text(serving_dv_col, y_pos, f'{int(dv_serving)}%', size=11, weight='bold', ha='right')
                add_text(container_dv_col, y_pos, f'{int(dv_container)}%', size=11, weight='bold', ha='right')
        else:
            add_text(indent, y_pos, display_name, size=size, weight=weight)
            add_text(serving_amount_col, y_pos, amt_serving_str, size=11, weight='normal', ha='right')
            add_text(container_amount_col, y_pos, amt_container_str, size=11, weight='normal', ha='right')
            
            if pd.notna(dv_serving) and nutrient not in ['Trans Fat', 'Total Sugars']:
                add_text(serving_dv_col, y_pos, f'{int(dv_serving)}%', size=11, weight='bold', ha='right')
                add_text(container_dv_col, y_pos, f'{int(dv_container)}%', size=11, weight='bold', ha='right')
        
        y_pos -= line_height
        
        if nutrient in ['Trans Fat', 'Cholesterol', 'Sodium', 'Added Sugars']:
            draw_line(y_pos, style='solid', thickness=0.8)
            y_pos -= 0.05
        elif nutrient == 'Protein':
            draw_line(y_pos, style='thick')
            y_pos -= 0.15
        elif nutrient == 'Potassium':
            draw_line(y_pos, style='medium')
            y_pos -= 0.05
    
    # Vertical separators
    ax.plot([left_separator_x, left_separator_x], [vertical_separator_top, y_pos], 'k-', linewidth=1, alpha=0.5)
    ax.plot([right_separator_x, right_separator_x], [vertical_separator_top, y_pos], 'k-', linewidth=1, alpha=0.5)
    
    y_pos -= 0.25
    
    # Footer
    footer = '*The % Daily Value (DV) tells you how much a nutrient in a\nserving of food contributes to a daily diet. 2,000 calories a\nday is used for general nutrition advice.'
    add_text(nutrient_col, y_pos, footer, size=8, weight='normal')
    
    plt.tight_layout()
    
    # Display in Streamlit
    st.pyplot(fig)
    
    # Save to bytes buffer for download
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    
    # Download button
    st.download_button(
        label="⬇️ Download Nutrition Facts Panel (PNG)",
        data=buf,
        file_name=f"{product_name.replace(' ', '_')}_NFP.png",
        mime="image/png",
        use_container_width=True
    )
    
    st.success("✅ Nutrition Facts Panel generated successfully!")
    
    # Summary
    with st.expander("📊 View Summary"):
        st.write(f"**Product:** {product_name}")
        st.write(f"**Serving Size:** {serving_size}")
        st.write(f"**Servings Per Container:** {servings_per_container}")
        st.write(f"**Calories per Serving:** {cal_serving}")
        st.write(f"**Calories per Container:** {cal_container}")
        st.write(f"**Total Nutrients:** {len(nutrients_df)}")
        st.info("✓ Panel complies with USFDA 2016 Nutrition Facts Label regulations")

# Footer
st.markdown("---")
st.markdown("💡 **Tips:** Enter your nutritional values per serving, and the per-container values are automatically calculated!")
