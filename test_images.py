import json
import streamlit as st

st.set_page_config(page_title="Test Images", page_icon="🧪")

st.title("Test Food Images")

# Load data
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Show first 5 foods with images
for food in data['foods'][:5]:
    st.subheader(food['name'])

    if food.get('image_data'):
        # Display image from base64
        st.image(
            f"data:image/jpeg;base64,{food['image_data']}",
            caption=food['name'],
            width=200
        )
        st.success(f"✓ {food['name']} has image data ({len(food['image_data'])} chars)")
    else:
        st.warning(f"✗ {food['name']} missing image data")

    st.divider()

st.info("กลับไป app.py หากรูปขึ้นได้")
