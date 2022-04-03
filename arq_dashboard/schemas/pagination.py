from .api_model import APIModel


class Pagination(APIModel):
    total: int
    page_size: int
    current_page: int
