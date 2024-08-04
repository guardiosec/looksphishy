from src.use_cases.use_case_add_brand import UseCaseAddBrand


def test_run():
    my_path = UseCaseAddBrand().get_path_to_keep('amazon')
    a = 1