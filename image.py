import streamlit as st
from PIL import Image
from rembg import remove
from io import BytesIO

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="Passport Image Resizer",
    page_icon="🖼️",
    layout="centered"
)

# ---------------- Header ----------------
st.title("🖼️ Passport Image Resizer")
st.write(
    "Upload your image, remove the background, resize to **600 × 800 pixels**, "
    "and compress it below **25 KB**."
)

# ---------------- Upload ----------------
uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

# White background option
white_bg = st.checkbox("Remove Background & Use White Background", value=True)

# ---------------- Image Processing ----------------
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    # Remove background using AI
    if white_bg:
        input_bytes = BytesIO()
        image.save(input_bytes, format="PNG")

        with st.spinner("Removing background..."):
            output_bytes = remove(input_bytes.getvalue())

        image = Image.open(BytesIO(output_bytes)).convert("RGBA")

        # Create white background
        white = Image.new("RGB", image.size, (255, 255, 255))
        white.paste(image, mask=image.split()[3])
        image = white

    else:
        image = image.convert("RGB")

    # Resize image
    image = image.resize((600, 800), Image.LANCZOS)

    # Compress image below 25KB
    target_size = 25 * 1024
    quality = 95

    while quality >= 5:
        buffer = BytesIO()
        image.save(
            buffer,
            format="JPEG",
            quality=quality,
            optimize=True
        )

        if buffer.tell() <= target_size:
            break

        quality -= 5

    final_size = buffer.tell() / 1024

    # ---------------- Preview ----------------
    st.subheader("Preview")
    st.image(image, width=250)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Resolution", "600 × 800")

    with col2:
        st.metric("File Size", f"{final_size:.2f} KB")

    if final_size <= 25:
        st.success("✅ Image processed successfully!")
    else:
        st.warning(
            f"Image size is {final_size:.2f} KB. "
            "Try uploading a smaller image for better compression."
        )

    # ---------------- Download ----------------
    st.download_button(
        label="⬇ Download Processed Image",
        data=buffer.getvalue(),
        file_name="passport_image.jpg",
        mime="image/jpeg"
    )
# ---------------- Footer ----------------
st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        padding:15px;
        border-radius:10px;
        background-color:#f0f2f6;
        color:#333333;
        font-size:18px;
        margin-top:20px;
    ">
        <h4 style="margin-bottom:5px;">🖼️ Passport Image Resizer</h4>
        <p style="margin:0;">
            ⭐ <b>Special Credit</b>
        </p>
        <p style="margin:5px 0;">
            👨‍💻 <span style="color:#1f77b4;"><b>Usman Goraya</b></span>
        </p>
        <p style="margin:0;">
            <i>Developer</i>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)