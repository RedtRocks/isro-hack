import streamlit as st
import folium
from streamlit_folium import st_folium
from workflow_generator import generate_workflow
from executor import run_workflow

st.set_page_config(layout="wide")
        
st.title("🗺️ Geospatial Chatbot with CoT Reasoning")

query = st.text_input("Describe your geospatial task:")
if st.button("Generate Workflow"):
    try:
        wf = generate_workflow(query)
        st.subheader("Chain-of-Thought Reasoning")
        for line in wf['reasoning']:
            st.write(line)

        st.subheader("Generated Workflow JSON")
        st.json(wf['workflow'])

        st.subheader("Executing Workflow…")
        results = run_workflow(wf)

        # Visualize last GeoDataFrame or raster
        last = list(results.values())[-1]
        if hasattr(last, 'plot'):
            m = folium.Map(location=[0, 0], zoom_start=2)
            if hasattr(last, 'geometry'):
                # vector
                folium.GeoJson(last).add_to(m)
            else:
                # raster: show bounds
                bounds = last.open().bounds
                folium.Rectangle(bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]]).add_to(m)
            st_folium(m, width=700)
        else:
            st.write("Last output is not mappable.")

    except Exception as e:
        st.error(f"Error: {e}")