import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import pandas as pd
import numpy as np
import laspy
import io

st.set_page_config(page_title="LAZ Converter", page_icon="📡")

st.title("📡 LAZ Converter – Convert .laz to CSV or XYZ")
st.write("Upload a `.laz` LiDAR file and download it as `.csv` or `.xyz`.")

uploaded_file = st.file_uploader("Select a LAZ file", type=["laz"])
output_format = st.radio("Choose output format:", ["CSV", "XYZ"])

if uploaded_file is not None:
    try:
        las = laspy.read(uploaded_file)
        x, y, z = las.x, las.y, las.z
        st.success(f"Loaded {len(x):,} points successfully ✅")

        if output_format == "CSV":
            df = pd.DataFrame({"X": x, "Y": y, "Z": z})
            csv_bytes = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download CSV file",
                data=csv_bytes,
                file_name=uploaded_file.name.replace(".laz", ".csv"),
                mime="text/csv",
            )
        else:
            xyz = np.column_stack((x, y, z))
            xyz_str = "\n".join([f"{a:.3f} {b:.3f} {c:.3f}" for a, b, c in xyz])
            xyz_bytes = xyz_str.encode("utf-8")

            st.download_button(
                label="📥 Download XYZ file",
                data=xyz_bytes,
                file_name=uploaded_file.name.replace(".laz", ".xyz"),
                mime="text/plain",
            )

    except Exception as e:
        st.error(f"Error converting file: {e}")
else:
    st.info("Please upload a .laz file to start.")
