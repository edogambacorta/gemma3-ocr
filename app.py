import streamlit as st
# import ollama  # Commented out for troubleshooting
from PIL import Image
import io
import base64
import traceback

# Import PDF processing functions
try:
    from pdf_processor import process_pdf, combine_text
except Exception as e:
    st.error(f"Error importing pdf_processor: {str(e)}")
    process_pdf, combine_text = None, None

# Placeholder variables for vector store (still commented out)
add_pdf_to_vector_store, search_vector_store = None, None

# Page configuration
st.set_page_config(
    page_title="Gemma-3 OCR",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
st.markdown("""
    # <img src="data:image/png;base64,{}" width="50" style="vertical-align: -12px;"> Gemma-3 OCR
""".format(base64.b64encode(open("./assets/gemma3.png", "rb").read()).decode()), unsafe_allow_html=True)

# Add clear button to top right
col1, col2 = st.columns([6,1])
with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Gemma-3 Vision!</p>', unsafe_allow_html=True)
st.markdown("---")

# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose a file...", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    if uploaded_file is not None:
        file_type = uploaded_file.type
        if file_type in ['image/png', 'image/jpeg', 'image/jpg']:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image")
        elif file_type == 'application/pdf':
            st.success("PDF file uploaded successfully")
        
        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing file..."):
                try:
                    if file_type in ['image/png', 'image/jpeg', 'image/jpg']:
                        # Placeholder for image processing
                        extracted_text = "Image processing is currently disabled for troubleshooting."
                    elif file_type == 'application/pdf':
                        if process_pdf and combine_text:
                            pdf_text, image_text = process_pdf(uploaded_file)
                            extracted_text = combine_text(pdf_text, image_text)
                        else:
                            st.error("PDF processing is not available due to import errors.")
                            extracted_text = None
                    
                    if extracted_text:
                        st.session_state['ocr_result'] = extracted_text
                        st.success("Text extraction successful.")
                    else:
                        st.error("Failed to extract text from the file.")
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
                    st.error(f"Traceback: {traceback.format_exc()}")

# Main content area for results
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
    
    # Add search functionality
    st.markdown("---")
    st.subheader("Search Extracted Content")
    search_query = st.text_input("Enter your search query:")
    if search_query:
        if search_vector_store:
            try:
                search_results = search_vector_store(search_query)
                st.write("Search Results:")
                for i, result in enumerate(search_results['documents'][0], 1):
                    st.markdown(f"**Result {i}:**\n{result}")
            except Exception as e:
                st.error(f"Error during search: {str(e)}")
                st.error(f"Traceback: {traceback.format_exc()}")
        else:
            st.warning("Search functionality is not available due to import errors.")
else:
    st.info("Upload an image or PDF and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Gemma-3 Vision Model | [Report an Issue](https://github.com/patchy631/ai-engineering-hub/issues)")
