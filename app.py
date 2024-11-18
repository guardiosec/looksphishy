import os
import streamlit as st

import conf
from src.use_cases.use_case_embedding import UseCaseEmbedding
from src.use_cases.use_case_logo import UseCaseLogo
from src.use_cases.use_case_llm import UseCaseLLM
from utils import url_to_folder_name, domain_to_url
from utils import create_directory
from src.crawler.crawler import Crawler
from src.use_cases.use_case_add_brand import UseCaseAddBrand
from src.use_cases.use_case_prepare_embedding import UseCasePrepareEmbedding
from logger_code import init_logger

create_directory(conf.URLS_SCANNED)

st.set_page_config(
    page_title="Looksphishy",
    page_icon=conf.LOGO,
)


def save_after_upload(uploaded_file, path_to_save):
    if not os.path.exists(path_to_save):
        bytes_data = uploaded_file.getvalue()
        with open(path_to_save, 'wb') as f:
            f.write(bytes_data)
            logger.info(f"{path_to_save} saved !")


if 'page' not in st.session_state:
    st.session_state.page = 'Looksphishy'


@st.cache_resource
def create_log_once():
    return init_logger(conf.LOGGER_NAME)

@st.cache_resource
def get_crawler():
    return Crawler(use_cache=False,
                   max_retries=3,  # Will retry 3 times before failing
                   page_load_timeout=30  # 30 seconds timeout
                   )


logger = create_log_once()

run_scan = False
default_url = 'http://instagram.com'
if 'text' not in st.session_state:
    st.session_state.text = default_url

st.markdown(conf.UI_DESIGN, unsafe_allow_html=True)
page = st.sidebar.radio("Select Page", ["Looksphishy", "Add Your Own Brand"])

if page == "Looksphishy":
    uploaded_file = None
    url_input = None
    crawler_object = get_crawler()

    col1, col2 = st.columns([20, 1])

    with col1:
        st.markdown('<h2>Looksphishy</h2>', unsafe_allow_html=True)

    with col2:
        st.image(os.path.join(conf.STATIC_FOLDER, "bh_usa_2024.png"), width=200)

    st.markdown('<div class="step-title">Step 1 - Select Input Method (Link/Image)</div>', unsafe_allow_html=True)
    input_method = st.radio("Select Input Method", ("Enter URL", "Upload Image"))
    if input_method == "Enter URL":
        url_input = domain_to_url(st.text_input("Enter URL:", value=default_url, label_visibility="visible"))
    else:
        uploaded_file = st.file_uploader("Upload an image (screenshot of a website for example)", type="png")

    st.markdown('<div class="step-title">Step 2 - Find similarity with known brands</div>', unsafe_allow_html=True)
    embedding_model_selected = st.radio(
        "Choose an embedding model that will convert the image into vector for comparison",
        UseCaseEmbedding.get_all_embedding_model_names(),
        captions=[None, "Open source", "Open source", "Open source"])
    check_category_model = st.toggle(
        "Step 3 (optional) - Get category of the website (with LLM) - **only when crawling URL**")
    llm_model_selected = None
    if check_category_model:
        llm_model_selected = st.radio(
            "Choose an LLM that extracts the category of the website using several parts of the HTML",
            UseCaseLLM.get_all_llm_model_names(),
            captions=[None, None, "Open source"])

    check_logo_model = st.toggle("Step 4 (optional) - Extract the logo")
    logo_model_selected = None
    if check_logo_model:
        logo_model_selected = st.radio(
            "Choose a model that focuses on identifying logo only",
            UseCaseLogo.get_all_logo_model_names(),
            captions=["Open source"])

    if st.button("Does it look phishy?"):
        run_scan = True
        if run_scan:
            if input_method == "Enter URL":
                st.session_state.text = url_input
                url = st.session_state.text
                default_url = url
                conf.current_url = url
                scan_id = url_to_folder_name(url)
                with st.spinner(f'Scanning {url} ...'):
                    logger.info(f'Scanning {url}', extra={"domain_scanned": url})
                    os.makedirs(os.path.join(conf.URLS_SCANNED, scan_id), exist_ok=True)
                    path_to_save = os.path.join(conf.URLS_SCANNED, scan_id, "screenshot.png")
                    if llm_model_selected:
                        html_content = crawler_object.run(url, path_to_save, get_html=True)
                    else:
                        crawler_object.run(url, path_to_save, get_html=False)
                    run_scan = False
                    path_analyze = path_to_save
                    st.image(path_analyze, width=500)  # Adjust width as needed

            else:
                if uploaded_file is not None:
                    os.makedirs(os.path.join(conf.URLS_SCANNED, uploaded_file.name.split(".")[0]), exist_ok=True)
                    save_after_upload(uploaded_file, os.path.join(conf.URLS_SCANNED, uploaded_file.name.split(".")[0], 'screenshot.jpg'))
                    path_analyze = os.path.join(conf.URLS_SCANNED, uploaded_file.name)
                    st.image(path_analyze, width=500)

            use_case = UseCaseEmbedding(embedding_model_name=embedding_model_selected.split(" ")[0], use_cache=True)
            df = use_case.run_embedding(path_analyze)
            if len(df) > 0:
                phishing_brand = df.iloc[0].brand_image
                phishing_brand_file = df.iloc[0].file
                st.markdown(
                    f"<h2 style='color: #ff4d4d;'>Looks phishy! - {phishing_brand}</h2> <b>The image you checked found similar in: {round((df['distance'].to_list()[0]) * 100, 3)} % to {phishing_brand} page found in our DB ({phishing_brand_file}):</b>",
                    unsafe_allow_html=True)
                st.image(os.path.join(conf.BRAND_FOLDER, phishing_brand, phishing_brand_file), width=500)
                if len(df) > 1:
                    with st.expander('Other similar brands - Details'):
                        st.dataframe(df)
            else:
                st.markdown("## The image does not match any of the brands in the database")

            if llm_model_selected:
                use_case_llm = UseCaseLLM(llm_model_name=llm_model_selected)

                category = use_case_llm.run(html_content)
                st.markdown(f"**CATEGORY** : {category}")

            if check_logo_model:
                use_case_logo = UseCaseLogo(logo_model_name=logo_model_selected)
                logo_text = use_case_logo.run(path_analyze).replace(' ', "")
                if logo_text:
                    st.markdown(f"**LOGO** : {logo_text}")

                else:
                    st.markdown(f"**No recognizable logo identified**")


elif page == "Add Your Own Brand":
    st.markdown('<div class="step-title">Add Your Own Brand</div>', unsafe_allow_html=True)
    brand_added = st.text_input("Enter brand name:")
    uploaded_brand = st.file_uploader("Upload your brand image (screenshot of a website for example)", type="png")
    embedding_model_preprocess = st.radio(
        "Choose an embedding model that will convert the image into vector for comparison",
        UseCaseEmbedding.get_all_embedding_model_names(),
        captions=[None, "Open source", "Open source", "Open source"])
    if st.button("Upload Brand"):
        if not brand_added:
            st.error("Write a brand before uploading!")
        if not uploaded_brand:
            st.error("Upload a file first!")
        else:
            if uploaded_brand is not None:
                if not brand_added:
                    st.error("Upload a file first!")
                with st.spinner("Uploading..."):

                    path_to_keep_brand = UseCaseAddBrand.get_path_to_keep(brand_added)
                    save_after_upload(uploaded_brand, path_to_keep_brand)
                    st.success(f"Upload successfully at {path_to_keep_brand}!")
                    st.image(uploaded_brand, width=500)
                with st.spinner(f"Computing embedding for {brand_added} only..."):
                    UseCasePrepareEmbedding().run(embedding_model_preprocess, one_brand=brand_added)
                    st.success(f"Embedding computed successfully for {brand_added} with {embedding_model_preprocess}!")
                    st.text("You are now able to catch any images/websites looking like this brand")
