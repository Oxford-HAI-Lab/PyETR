from .generate_case_all import main as main_case_all
from .generate_case_index import main as main_case_index
from .generate_case_list import main as main_case_list
from .generate_inference_page import main as main_infer_page
from .generate_view_methods import main as main_view_methods


def main():
    main_case_all()
    main_case_list()
    main_case_index()
    main_infer_page()
    main_view_methods()
